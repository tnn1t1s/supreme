import os

from .agents import (
    retriever_agent,
    join_analysis_agent,
    holding_agent,
    fracture_agent,
    marks_agent,
    claim_assessment_agent,
    impact_agent,
    synthesis_agent,
)
from .planner.executor import DAPAgent
from .planner.heuristic import HeuristicPlanner
from .planner.llm_planner import LLMPlanner


def _create_planner():
    mode = os.environ.get("DAP_PLANNER", "heuristic").lower()
    if mode == "llm":
        model = os.environ.get("DAP_PLANNER_MODEL")
        return LLMPlanner(model=model)
    return HeuristicPlanner()


root_agent = DAPAgent(
    name="decision_rag",
    description=(
        "Institutional analysis pipeline for Supreme Court decision corpus. "
        "Deterministic affordance planner selects which agents run based on "
        "query intent, corpus availability, and declared preconditions."
    ),
    sub_agents=[
        retriever_agent,
        join_analysis_agent,
        holding_agent,
        fracture_agent,
        marks_agent,
        claim_assessment_agent,
        impact_agent,
        synthesis_agent,
    ],
    agent_registry={
        "retrieval": retriever_agent,
        "vote_structure": join_analysis_agent,
        "holdings": holding_agent,
        "fractures": fracture_agent,
        "marks": marks_agent,
        "claim_assessment": claim_assessment_agent,
        "impact_analysis": impact_agent,
        "synthesis": synthesis_agent,
    },
    planner=_create_planner(),
    catalog_path="config/affordances.yaml",
    docs_root="docs/decision",
)
