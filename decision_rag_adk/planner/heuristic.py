from .base import BasePlanner
from .query_analyzer import analyze_query


class HeuristicPlanner(BasePlanner):
    def analyze(self, query_text, manifests=None, catalog=None):
        features = analyze_query(query_text)
        features["planner_type"] = "heuristic"
        features["corpus_scope_override"] = None
        features["llm_reasoning"] = None
        return features
