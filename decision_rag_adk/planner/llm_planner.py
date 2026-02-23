import json
import os
import re

from google import genai
from google.genai import types

from .base import BasePlanner

DEFAULT_MODEL = "gemini-3.1-pro-preview"

SYSTEM_PROMPT = """\
You are a query intent classifier for a Supreme Court decision analysis system.
Given a user query, corpus manifests, and an affordance catalog, determine which
analysis intents should be activated.

Return ONLY a JSON object with this exact schema:
{
  "intents": {
    "precedent": bool,
    "marks": bool,
    "compliance": bool,
    "commentary_assessment": bool,
    "factual_summary": bool
  },
  "corpus_scope_override": null or ["corpus_key", ...],
  "reasoning": "1-3 sentences explaining your classification"
}

## Intent Definitions

1. precedent — Set true when:
   - Query asks about holdings, majority opinion, vote structure
   - Query asks about which justices joined which opinion
   - Query asks about concurrences, dissents, coalitions
   - Query asks about what the Court decided or ruled

2. marks — Set true when:
   - Query asks about "controlling opinion" in a fractured decision
   - Query asks about "binding" or "narrowest" principle
   - Query implies plurality situation even without saying "Marks"
   - Corpus manifests show partial joins (concurrence_in_part) or multiple concurrences
   STRUCTURAL SIGNAL: If the manifest shows concurrence_in_part opinions,
   the decision is fractured. Questions about "binding rule" or "controlling
   precedent" in a fractured decision require Marks analysis.
   IMPORTANT: "which parts are not controlling precedent" = Marks analysis.

3. compliance — Set true when:
   - Query asks whether an action satisfies statutory requirements
   - Query asks about legal authority, predicate, or prerequisites
   - Query asks if something is "authorized" or "lawful"

4. commentary_assessment — Set true when:
   - Query specifically asks about media commentary or external analysis
   - Query mentions National Review, specific commentators, or bench memos
   - Query asks to assess or evaluate claims from outside sources

5. factual_summary — Set true when:
   - Query asks for a summary, overview, or explanation of what happened
   - Query is a general "what did X decide" question
   - No other intents apply (this is the fallback)

## corpus_scope_override

Set to a list of corpus keys ONLY if the query clearly targets specific corpora.
Otherwise set to null and let the default scoping apply.

## Rules
- Multiple intents can be true simultaneously
- At least one intent must be true
- If no other intent clearly applies, set factual_summary to true
- marks almost always co-occurs with precedent (Marks analysis requires vote structure)
"""


def _summarize_manifests(manifests):
    lines = []
    for key, manifest in manifests.items():
        opinions = manifest.get("opinions", [])
        blocks = manifest.get("blocks", [])
        block_count = len(blocks) if blocks else manifest.get("block_count", "?")
        types = set()
        justices = set()
        for op in opinions:
            if op.get("opinion_type"):
                types.add(op["opinion_type"])
            if op.get("justice"):
                justices.add(op["justice"])
        for b in blocks:
            if b.get("opinion_type"):
                types.add(b["opinion_type"])
            if b.get("justice"):
                justices.add(b["justice"])
        parts = [f"corpus={key}", f"blocks={block_count}"]
        if types:
            parts.append(f"opinion_types={sorted(types)}")
        if justices:
            parts.append(f"justices={sorted(justices)}")
        lines.append("  " + " | ".join(parts))
    return "\n".join(lines) if lines else "  (no manifests loaded)"


def _summarize_catalog(catalog):
    lines = []
    for aff_id, aff in catalog.items():
        triggers = aff.get("triggers_any", [])
        inputs = aff.get("inputs", [])
        outputs = aff.get("outputs", [])
        requires = aff.get("requires", [])
        parts = [
            f"triggers={triggers}",
            f"inputs={inputs}",
            f"outputs={outputs}",
        ]
        if requires:
            parts.append(f"requires={requires}")
        lines.append(f"  {aff_id}: {' | '.join(parts)}")
    return "\n".join(lines)


def _parse_json_response(text):
    m = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    return json.loads(text)


class LLMPlanner(BasePlanner):
    def __init__(self, model=None):
        self.model = model or os.environ.get("DAP_PLANNER_MODEL", DEFAULT_MODEL)
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
            if os.path.exists(env_path):
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GOOGLE_API_KEY="):
                            api_key = line.split("=", 1)[1]
                            break
        self.client = genai.Client(api_key=api_key)

    def analyze(self, query_text, manifests=None, catalog=None):
        manifests = manifests or {}
        catalog = catalog or {}

        user_prompt = self._build_user_prompt(query_text, manifests, catalog)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.0,
                    max_output_tokens=2048,
                    thinking_config=types.ThinkingConfig(thinking_budget=512),
                ),
            )
            result = _parse_json_response(response.text)
        except Exception:
            return self._fallback(query_text)

        return self._normalize(result, query_text)

    def _build_user_prompt(self, query_text, manifests, catalog):
        manifest_summary = _summarize_manifests(manifests)
        catalog_summary = _summarize_catalog(catalog)
        return (
            f"## Corpus Manifests\n{manifest_summary}\n\n"
            f"## Affordance Catalog\n{catalog_summary}\n\n"
            f"## Query\n{query_text}"
        )

    def _normalize(self, result, query_text):
        intents = result.get("intents", {})
        for key in ("precedent", "marks", "compliance",
                     "commentary_assessment", "factual_summary"):
            intents.setdefault(key, False)

        if not any(intents.values()):
            intents["factual_summary"] = True

        keywords = []
        triggered_rules = []
        for intent_name, active in intents.items():
            if active:
                triggered_rules.append({
                    "intent": intent_name,
                    "type": "llm",
                    "match": f"LLM classified as {intent_name}",
                })

        return {
            "intents": intents,
            "keywords": keywords,
            "triggered_rules": triggered_rules,
            "planner_type": "llm",
            "corpus_scope_override": result.get("corpus_scope_override"),
            "llm_reasoning": result.get("reasoning"),
        }

    def _fallback(self, query_text):
        return {
            "intents": {
                "precedent": False,
                "marks": False,
                "compliance": False,
                "commentary_assessment": False,
                "factual_summary": True,
            },
            "keywords": [],
            "triggered_rules": [
                {"intent": "factual_summary", "type": "llm_fallback",
                 "match": "LLM parse failure — conservative degradation"}
            ],
            "planner_type": "llm",
            "corpus_scope_override": None,
            "llm_reasoning": "Fallback: LLM response could not be parsed",
        }
