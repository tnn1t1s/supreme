from abc import ABC, abstractmethod


class BasePlanner(ABC):
    @abstractmethod
    def analyze(self, query_text, manifests=None, catalog=None):
        """Return query_features dict with intents, triggered_rules, planner_type.

        Schema:
            intents: dict[str, bool]  — precedent, marks, compliance,
                                        commentary_assessment, factual_summary
            keywords: list[str]
            triggered_rules: list[dict]  — {intent, type, match}
            planner_type: "heuristic" | "llm"
            corpus_scope_override: list[str] | None  (LLM only)
            llm_reasoning: str | None  (LLM only)
        """
