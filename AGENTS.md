# AGENTS.md — ADK Pipeline Agent Reference

The decision analysis pipeline is a Google ADK `SequentialAgent` containing 6 `LlmAgent` sub-agents. Each agent receives state from upstream agents via `output_key` → shared session state, executes tools against the corpus, and produces structured JSON output consumed by downstream agents. The final agent (Synthesis) renders a human-readable report.

**Entry point:** `decision_rag_adk/__init__.py` → exports `root_agent`
**Runner:** `tools/bin/decision-adk` (wraps `adk run` / `adk web`)

---

## Pipeline Architecture

```
User Query
  │
  ▼
┌─────────────────────────────────────────────────────┐
│  SequentialAgent: decision_rag                       │
│                                                      │
│  ┌──────────────┐    ┌──────────────────┐           │
│  │ 1. Retriever  │───▶│ 2. Join Analysis  │          │
│  │   (flash)     │    │    (pro)          │          │
│  └──────────────┘    └──────────────────┘           │
│         │                     │                      │
│         ▼                     ▼                      │
│  ┌──────────────┐    ┌──────────────────┐           │
│  │ 3. Holding    │───▶│ 4. Fracture      │          │
│  │   (pro)       │    │    (pro)          │          │
│  └──────────────┘    └──────────────────┘           │
│         │                     │                      │
│         ▼                     ▼                      │
│  ┌──────────────┐    ┌──────────────────┐           │
│  │ 5. Marks      │───▶│ 6. Synthesis     │          │
│  │   (pro)       │    │    (pro)          │          │
│  └──────────────┘    └──────────────────┘           │
│                                                      │
└─────────────────────────────────────────────────────┘
  │
  ▼
Final Report (8-section markdown)
```

All agents execute sequentially. Each agent's `output_key` writes to shared session state; downstream agents access it via `{state_key?}` template variables in their prompts.

---

## Global Invariants

Every agent's system prompt begins with the same 7 invariants, injected from `decision_rag_adk/prompts/invariants.py`. These are non-negotiable constraints that govern all agent output.

### 1. GROUNDING
Every factual claim about the decision must cite a specific `block_id` and page range. No unsupported assertions. If a claim cannot be grounded, the agent must say so explicitly.

**Why it matters:** Without grounding, LLM outputs about legal decisions can hallucinate holdings, misattribute positions to justices, or fabricate doctrinal analysis. Grounding forces every claim to be traceable to a specific passage in the corpus.

### 2. HOLDING DISCIPLINE
Strictly distinguish between three categories:
- **(a) HOLDING** — the binding legal principle that commands a majority of justices
- **(b) REASONING** — the analytical steps that support the holding
- **(c) RHETORIC/DICTA** — persuasive language or observations not necessary to the decision

Each proposition must be labeled accordingly. Reasoning or dicta must never be presented as holding.

**Why it matters:** The distinction between holding and dicta is the most consequential classification in legal analysis. Conflating them leads to overbroad precedent claims — the dominant failure mode this pipeline is designed to prevent.

### 3. NO NARRATIVE COLLAPSE
Never merge distinct opinions into composite narratives. Each justice's position must be attributed individually. The phrase "The dissenters argued X" is only valid when all dissenters joined the same section making that specific argument.

**Why it matters:** Supreme Court opinions are authored individually. When a 6-3 decision has 8 separate opinions, each justice's reasoning is distinct. Collapsing them into group narratives (e.g., "the conservatives held") obscures the actual fracture structure.

### 4. MINIMALITY BIAS
When identifying holdings, prefer the narrowest reading supported by the join structure. A proposition is only a holding if it commands a majority of justices (5+ in a 9-justice court). When the majority is fractured, identify which propositions actually have majority support.

**Why it matters:** Courts prefer narrow holdings. A proposition joined by 3 of 6 majority justices is not a holding — it is a plurality view. The Learning Resources case specifically fractures 3-3 within the 6-justice majority, making this invariant critical.

### 5. DOCTRINE PRECISION
Use exact doctrinal labels from a fixed vocabulary: `major questions doctrine`, `nondelegation doctrine`, `clear statement rule`, `separation of powers`, `taxing power`, `statutory interpretation`, `foreign affairs power`, `emergency powers`, `congressional delegation`. Never conflate distinct doctrines.

**Why it matters:** Doctrinal labels are terms of art with precise legal meanings. Conflating "major questions doctrine" with "nondelegation doctrine" (they are related but distinct) would mischaracterize the decision's doctrinal reach.

### 6. NO MOTIVE INFERENCE
Do not speculate on why a justice took a particular position. Report what the text says, not what it might "really mean" or what strategic considerations might have driven the opinion's structure.

**Why it matters:** Motive attribution is inherently speculative and politically charged. The pipeline's value depends on analyzing what the text says, not on political commentary about judicial strategy.

### 7. MARKS SKEPTICISM
When applying *Marks v. United States* (narrowest-ground analysis), acknowledge that Marks is contested and its application is often ambiguous. Flag uncertainty rather than asserting a single "correct" Marks analysis.

**Why it matters:** The Marks doctrine (how to identify the controlling opinion when no single opinion commands a majority) is one of the most disputed analytical frameworks in constitutional law. The Supreme Court itself has acknowledged difficulty applying it. Presenting a Marks analysis as definitive when reasonable analysts disagree would undermine the pipeline's credibility.

---

## Agent 1: Retriever

| Property | Value |
|----------|-------|
| **Name** | `retriever` |
| **Model** | `gemini-2.5-flash` |
| **Module** | `decision_rag_adk/agents/retriever.py` |
| **Prompt** | `decision_rag_adk/prompts/retriever.py` |
| **Output key** | `retrieved_blocks` |
| **Tools** | `query_decision_rag`, `load_manifest` |

### Role

The retriever is the pipeline's entry point. It translates the user's natural-language query into corpus searches and returns a ranked set of relevant blocks with metadata.

### Procedure

1. Calls `load_manifest()` to get the full corpus structure — all 8 opinions, their justices, block counts, and page ranges.
2. Analyzes the user's query to determine search terms and appropriate filters (justice, opinion type, doctrine).
3. Calls `query_decision_rag()` with the query. May make multiple calls with different terms or filters for comprehensive coverage.
4. Returns structured JSON containing the query, search terms used, manifest summary, and an array of retrieved blocks with their `block_id`, metadata, similarity score, and text preview.

### Why Flash

The retriever uses `gemini-2.5-flash` because it performs mechanical work — translating queries into search parameters and formatting results. It does not perform legal analysis. Flash is faster and cheaper, and the quality bar for retrieval dispatch is lower than for analytical reasoning.

### Output Schema

```json
{
  "query": "original user query",
  "search_terms": ["terms", "used"],
  "manifest_summary": {
    "case": "Learning Resources, Inc. v. Trump",
    "total_blocks": 53,
    "opinions": [{"justice": "Roberts", "type": "majority", "block_count": 7}]
  },
  "retrieved_blocks": [
    {
      "block_id": "24-1287_roberts_majority_0005",
      "justice": "Roberts",
      "opinion_type": "majority",
      "title": "II-A",
      "page_start": 12,
      "page_end": 18,
      "score": 0.8234,
      "doctrines_primary": "statutory_interpretation,emergency_powers",
      "text_preview": "first 500 chars..."
    }
  ]
}
```

---

## Agent 2: Join Analysis

| Property | Value |
|----------|-------|
| **Name** | `join_analysis` |
| **Model** | `gemini-2.5-pro` |
| **Module** | `decision_rag_adk/agents/join_analysis.py` |
| **Prompt** | `decision_rag_adk/prompts/join_analysis.py` |
| **Output key** | `join_structure` |
| **Tools** | `read_block`, `list_blocks` |
| **Reads state** | `{retrieved_blocks?}` |

### Role

Maps which justices join which sections of each opinion. This is the structural foundation for every downstream agent — without an accurate join map, holding identification, fracture classification, and Marks analysis are all unreliable.

### Procedure

1. Reads the syllabus blocks (which describe join structure) using `read_block()`.
2. Uses `list_blocks()` to enumerate all blocks, then reads key blocks from each opinion to verify joins against opinion headers.
3. For each opinion, identifies: the author, full joiners, partial joiners (which specific sections they join and which they don't), and judgment-only concurrences.
4. Computes the "effective majority" — which sections command 5+ justices and which are fractured.

### Critical Distinctions

The prompt enforces precise join terminology:
- **"Concurring in part"** = the justice joins some but not all sections. The agent must identify exactly which parts.
- **"Concurring in the judgment"** = the justice agrees with the result but not the reasoning. This is a weaker form of agreement.
- Partial joins create the pipeline's central analytical challenge: the same "opinion of the Court" can contain both majority holdings (sections with 6 justices) and plurality reasoning (sections with only 3 justices).

### Output Schema

```json
{
  "case": "Learning Resources, Inc. v. Trump",
  "total_justices": 9,
  "majority_author": "Roberts",
  "join_map": {
    "Roberts_majority": {
      "author": "Roberts",
      "opinion_type": "majority",
      "full_joiners": ["Gorsuch", "Barrett"],
      "partial_joiners": {
        "Kagan": {
          "sections_joined": ["I", "II-A-1", "II-B"],
          "sections_not_joined": ["II-A-2", "III"]
        }
      },
      "judgment_only": []
    }
  },
  "effective_majority": {
    "description": "6-3 on judgment; 3-3 on MQ reasoning",
    "sections_with_full_majority": ["I", "II-A-1", "II-B"],
    "fractured_sections": ["II-A-2", "III"]
  },
  "source_blocks": ["24-1287_syllabus_syllabus_0001", "..."]
}
```

### Why This Agent Is Critical

The Learning Resources decision is a 6-3 judgment with a 3-3 reasoning split within the majority. Without the join map, a reader would not know that Parts II-A-2 and III of the "opinion of the Court" are actually plurality reasoning (3 justices) rather than majority holding (6 justices). This is the single most important structural fact about the decision, and every downstream agent depends on it.

---

## Agent 3: Holding Candidate

| Property | Value |
|----------|-------|
| **Name** | `holding_candidate` |
| **Model** | `gemini-2.5-pro` |
| **Module** | `decision_rag_adk/agents/holding.py` |
| **Prompt** | `decision_rag_adk/prompts/holding.py` |
| **Output key** | `holding_candidates` |
| **Tools** | `read_block` |
| **Reads state** | `{join_structure?}` |

### Role

Extracts candidate holdings from the majority opinion, classifies each as holding/reasoning/dicta, and ranks them by strength of majority support.

### Procedure

1. Reads majority opinion blocks identified in the join structure.
2. For each section, extracts core legal propositions.
3. Classifies each proposition:
   - **HOLDING**: Necessary to the disposition, supported by 5+ justices, stated as a rule or principle.
   - **REASONING**: Analytical steps supporting a holding, not themselves the rule of decision.
   - **DICTA**: Observations, historical discussions, or hypotheticals not necessary to the outcome.
4. Ranks candidates by majority support count.

### Holding Width

Every candidate holding must be classified by width:

| Width | Meaning | Example |
|-------|---------|---------|
| `case_specific` | Limited to IEEPA or this statutory context | "'regulate...importation' in IEEPA does not include tariffs" |
| `general_principle` | Extends beyond this case | "a statutory grant of power to 'regulate' does not include the power to tax" |

When the text supports both readings, the agent lists both and notes which the text more directly states. This is where MINIMALITY BIAS (Invariant 4) applies most forcefully: the agent prefers the narrow reading as the candidate holding and presents the broader reading as an alternative interpretation.

### Output Schema

```json
{
  "holding_candidates": [
    {
      "id": "H1",
      "proposition": "IEEPA does not authorize the President to impose tariffs",
      "classification": "holding",
      "width": "case_specific",
      "width_note": "operative language: 'regulate...importation' in IEEPA",
      "majority_support": 6,
      "supporting_justices": ["Roberts", "Gorsuch", "Barrett", "Sotomayor", "Kagan", "Jackson"],
      "source_blocks": ["24-1287_roberts_majority_0007"],
      "page_range": "25-27",
      "doctrines": ["statutory_interpretation", "emergency_powers"],
      "narrow_reading": "IEEPA's 'regulate...importation' does not include tariffs",
      "broad_reading": "emergency powers statutes do not authorize taxation",
      "confidence": "high",
      "notes": ""
    }
  ],
  "disposition": "Affirmed in part, vacated in part",
  "disposition_vote": "6-3"
}
```

---

## Agent 4: Fracture Classifier

| Property | Value |
|----------|-------|
| **Name** | `fracture_classifier` |
| **Model** | `gemini-2.5-pro` |
| **Module** | `decision_rag_adk/agents/fracture.py` |
| **Prompt** | `decision_rag_adk/prompts/fracture.py` |
| **Output key** | `fractures` |
| **Tools** | `read_block`, `list_blocks` |
| **Reads state** | `{holding_candidates?}` |

### Role

Identifies and classifies every point of disagreement between opinions. Each fracture is typed, grounded in citations from both sides, and linked to affected holdings.

### Fracture Taxonomy

The classifier uses exactly 5 fracture types:

| Type | Definition | Example from this case |
|------|------------|----------------------|
| **DOCTRINAL** | Disagreement about which legal doctrine applies or how it should be formulated | Majority uses statutory interpretation; dissent argues nondelegation doctrine controls |
| **FACTUAL** | Disagreement about characterization of facts or the record | Majority says tariffs are a tax; dissent says they are a regulatory penalty |
| **METHODOLOGICAL** | Disagreement about interpretive method (textualism vs. purposivism, originalism, etc.) | Majority reads plain text; concurrence emphasizes legislative history |
| **SCOPE** | Agreement on the rule but disagreement about how broadly it applies | Both agree IEEPA grants emergency powers but disagree on whether tariffs fall within that grant |
| **REMEDIAL** | Agreement on the principle but disagreement about remedy or disposition | Both find a violation but disagree on whether to strike down entirely or sever |

### Grounding Requirement

Each fracture must cite specific `block_id`s from both sides of the disagreement. The agent cannot infer fractures not explicitly stated in the text (Invariant 6: no motive inference).

### Output Schema

```json
{
  "fractures": [
    {
      "id": "F1",
      "type": "doctrinal",
      "description": "Whether MQ doctrine is necessary to resolve IEEPA tariff question",
      "side_a": {
        "position": "Major questions doctrine required for clear resolution",
        "justices": ["Roberts", "Gorsuch", "Barrett"],
        "source_blocks": ["24-1287_roberts_majority_0005"],
        "page_range": "18-22"
      },
      "side_b": {
        "position": "Ordinary statutory interpretation sufficient",
        "justices": ["Kagan", "Sotomayor", "Jackson"],
        "source_blocks": ["24-1287_kagan_concurrence_in_part_0001"],
        "page_range": "78-82"
      },
      "related_holdings": ["H1"],
      "doctrines_at_issue": ["major_questions", "statutory_interpretation"],
      "vote_split": "3-3",
      "majority_required": false,
      "affects_outcome": false,
      "notes": "Split is within the 6-justice majority; does not affect the judgment"
    }
  ],
  "fracture_summary": {
    "total": 6,
    "by_type": {"doctrinal": 3, "factual": 1, "methodological": 1, "scope": 1, "remedial": 0},
    "most_fractured_doctrine": "major_questions",
    "outcome_affecting_count": 0
  }
}
```

### Key Fields

- **`vote_split`**: The actual numeric split on this fracture point (e.g., `6-3`, `3-3`).
- **`majority_required`**: Whether this fracture affects whether a holding commands a majority.
- **`affects_outcome`**: Whether this fracture changes the judgment (disposition). In this case, no fracture affects the 6-3 outcome — they all concern reasoning, not result.

---

## Agent 5: Marks Evaluator

| Property | Value |
|----------|-------|
| **Name** | `marks_evaluator` |
| **Model** | `gemini-2.5-pro` |
| **Module** | `decision_rag_adk/agents/marks.py` |
| **Prompt** | `decision_rag_adk/prompts/marks.py` |
| **Output key** | `marks_analysis` |
| **Tools** | `read_block` |
| **Reads state** | `{holding_candidates?}`, `{join_structure?}`, `{fractures?}` |

### Role

Applies the *Marks v. United States*, 430 U.S. 188 (1977), narrowest-ground analysis. When no single opinion commands a majority on a given proposition, Marks holds that the controlling opinion is the one that concurred in the judgment on the narrowest grounds.

### Procedure

1. Determines whether the decision has a clear majority on all points or is fractured.
2. For propositions without clear majority support, identifies which concurrence rests on the "narrowest grounds."
3. Evaluates whether the narrowest-ground analysis yields a clear answer or is ambiguous.
4. Cross-references with the fracture classification to locate where the narrowest ground lies.

### Marks Skepticism (Invariant 7)

The agent is explicitly instructed to never present a single "correct" Marks answer. Instead it:
- Presents the strongest candidate(s) for narrowest ground
- Notes where reasonable analysts would disagree
- States ambiguity factors explicitly
- If Marks analysis is genuinely indeterminate, says so without forcing resolution

### "Narrowest Grounds" Definition

The prompt clarifies: "narrowest grounds" means the position that is a **logical subset** of the broader positions — not merely the shortest or most cautious opinion. In this case, Kagan's statutory interpretation reasoning (IEEPA plain text doesn't cover tariffs) is a logical subset of the plurality's reasoning (statutory interpretation + major questions doctrine), making Kagan's the narrowest ground.

### Output Schema

```json
{
  "marks_applicable": true,
  "marks_rationale": "Parts II-A-2 and III command only 3 justices...",
  "majority_holdings": [
    {
      "holding_ref": "H1",
      "proposition": "IEEPA does not authorize tariffs",
      "majority_count": 6,
      "status": "clear_majority"
    }
  ],
  "narrowest_ground_analysis": {
    "candidates": [
      {
        "justice": "Kagan",
        "position": "Ordinary statutory interpretation resolves the question",
        "source_blocks": ["24-1287_kagan_concurrence_in_part_0001"],
        "why_narrowest": "Statutory interpretation is a logical subset of statutory interpretation + MQ doctrine",
        "counterargument": "Kagan's reasoning might not address all applications of the MQ holding",
        "strength": "strong"
      }
    ],
    "assessment": "Kagan's concurrence is likely the narrowest ground...",
    "ambiguity_factors": ["MQ doctrine sections have no Marks candidate..."]
  },
  "practical_impact": "Lower courts should treat the statutory interpretation holding as binding..."
}
```

---

## Agent 6: Synthesis

| Property | Value |
|----------|-------|
| **Name** | `synthesis` |
| **Model** | `gemini-2.5-pro` |
| **Module** | `decision_rag_adk/agents/synthesis.py` |
| **Prompt** | `decision_rag_adk/prompts/synthesis.py` |
| **Output key** | (none — final output) |
| **Tools** | (none) |
| **Reads state** | `{retrieved_blocks?}`, `{join_structure?}`, `{holding_candidates?}`, `{fractures?}`, `{marks_analysis?}` |

### Role

Produces a comprehensive, human-readable report integrating all upstream analysis. The synthesis agent does not make new claims — it organizes, summarizes, and presents findings from the previous 5 agents.

### Report Structure (8 sections)

| # | Section | Content |
|---|---------|---------|
| 1 | **Query & Scope** | What was asked, what blocks were retrieved, what the corpus covers |
| 2 | **Vote Structure & Joins** | Who wrote what, who joined what, where partial joins create complexity. Cites `block_id`s. |
| 3 | **Candidate Holdings** | Ranked list with classification (holding/reasoning/dicta), width (case-specific or general), majority support count, and doctrinal grounding. Narrow and broad readings for each. |
| 4 | **Fracture Map** | Typed fractures organized by doctrine. Both sides cited. Reports `vote_split`, `majority_required`, `affects_outcome`. |
| 5 | **Marks v. United States Analysis** | Whether Marks applies, candidate narrowest grounds, ambiguity factors, practical assessment. Preserves all uncertainty flags. |
| 6 | **Doctrinal Implications** | Which doctrines this decision advances, narrows, or leaves open. Grounded in specific blocks. |
| 7 | **Open Questions** | What the decision does not resolve. What lower courts will need to work out. Where fractures leave genuine ambiguity. |
| 8 | **Citation Index** | Compact reference table: `block_id` | justice | opinion_type | pages | doctrines — for every block cited. |

### Voice Rules

The synthesis agent operates under strict voice constraints:

- **Clerical, not interpretive**: The subject is always the justices or the opinion, never "the decision" as an abstract actor. Write "A six-justice majority held..." not "The decision establishes..."
- **No evaluative framing**: The words "importantly," "notably," "significantly," and "crucially" are prohibited.
- **No forward-looking language**: No "this will shape..." or "future courts must..."
- **No severity labels for fractures**: Report `vote_split`, `majority_required`, and `affects_outcome` numerically. Do not use "fundamental," "significant," or "minor."
- **Preserve ambiguity**: If upstream analysis flagged uncertainty, the synthesis preserves it. It does not resolve what the analysts left open.
- **Cite everything**: Every factual claim includes a `(block_id, pp. X-Y)` citation.

### Why No Tools

The synthesis agent has no tools. It reads exclusively from session state populated by agents 1–5. This ensures it cannot introduce new information — it can only reorganize what has already been retrieved and analyzed.

---

## Tools Available to Agents

The pipeline provides 4 tool functions across 2 modules.

### `decision_rag_adk/tools/retrieval.py`

#### `query_decision_rag(query, justice?, opinion_type?, doctrine?, top_k?)`

Shells out to `tools/bin/decision-rag query --json` via subprocess. This keeps the LlamaIndex retrieval implementation independent of ADK.

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | str | Search query text |
| `justice` | str | Comma-separated justice names (e.g., `"Roberts,Gorsuch"`) |
| `opinion_type` | str | Comma-separated types (e.g., `"majority,concurrence"`) |
| `doctrine` | str | Comma-separated doctrine tags |
| `top_k` | int | Number of results (default 10) |

Returns JSON array of matching blocks with scores, metadata, and text previews.

**Used by:** Retriever agent only.

### `decision_rag_adk/tools/corpus.py`

#### `load_manifest()`

Reads `docs/decision/.../manifest.json` and returns the full corpus metadata: case name, docket numbers, date, opinions list, and blocks list.

**Used by:** Retriever agent.

#### `read_block(block_id)`

Reads a specific block by its `block_id` (e.g., `"24-1287_roberts_majority_0005"`). Parses YAML frontmatter and returns metadata + full text content.

**Used by:** Join Analysis, Holding Candidate, Fracture Classifier, Marks Evaluator.

#### `list_blocks(justice?, opinion_type?)`

Lists all available blocks with metadata. Optionally filters by justice name and/or opinion type. Returns an array of block metadata dicts.

**Used by:** Join Analysis, Fracture Classifier.

---

## State Flow

```
Session State Key         Written By           Read By
─────────────────         ──────────           ───────
retrieved_blocks          Retriever            Join Analysis, Synthesis
join_structure            Join Analysis        Holding, Marks, Synthesis
holding_candidates        Holding              Fracture, Marks, Synthesis
fractures                 Fracture             Marks, Synthesis
marks_analysis            Marks                Synthesis
```

Each agent writes exactly one state key. The synthesis agent reads all five.

---

## Model Selection

| Agent | Model | Rationale |
|-------|-------|-----------|
| Retriever | `gemini-2.5-flash` | Mechanical work (query → search params → format results). Speed over reasoning. |
| Join Analysis | `gemini-2.5-pro` | Requires careful reading of opinion headers and cross-referencing join structure. |
| Holding Candidate | `gemini-2.5-pro` | Legal classification (holding vs. reasoning vs. dicta) demands precision. |
| Fracture Classifier | `gemini-2.5-pro` | Cross-opinion comparison with typed taxonomy. Reads the most blocks. |
| Marks Evaluator | `gemini-2.5-pro` | Most analytically demanding: applies a contested legal framework to a fractured decision. |
| Synthesis | `gemini-2.5-pro` | Long-form writing with strict voice constraints and comprehensive citation requirements. |

---

## Session Persistence

ADK persists all sessions to `decision_rag_adk/.adk/session.db` (SQLite). Every event — user queries, agent text responses, tool calls, and tool responses — is stored as a JSON blob in the `events` table with timestamps and invocation IDs.

Use `tools/bin/adk-sessions` to retrieve prompt/response pairs from the session database. See [TOOLS.md](TOOLS.md) for full documentation of the retrieval tool.

---

## Prompt Files

All prompts live in `decision_rag_adk/prompts/`:

| File | Exports | Length | Used By |
|------|---------|--------|---------|
| `invariants.py` | `INVARIANTS_PREAMBLE` | 1,382 chars | All 6 agents (prepended) |
| `retriever.py` | `RETRIEVER_INSTRUCTION` | 3,580 chars | Agent 1 |
| `join_analysis.py` | `JOIN_ANALYSIS_INSTRUCTION` | 4,231 chars | Agent 2 |
| `holding.py` | `HOLDING_INSTRUCTION` | 4,982 chars | Agent 3 |
| `fracture.py` | `FRACTURE_INSTRUCTION` | 5,273 chars | Agent 4 |
| `marks.py` | `MARKS_INSTRUCTION` | 5,130 chars | Agent 5 |
| `synthesis.py` | `SYNTHESIS_INSTRUCTION` | 5,399 chars | Agent 6 |

Each prompt = invariants preamble + agent-specific instruction with JSON output schema. Prompt changes take effect on the next query (no restart needed for `adk web`).

To view any agent's full prompt: `just adk-prompt <agent_name>`
