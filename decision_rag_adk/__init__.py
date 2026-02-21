from google.adk.agents import SequentialAgent

from .agents import (
    retriever_agent,
    join_analysis_agent,
    holding_agent,
    fracture_agent,
    marks_agent,
    synthesis_agent,
)

root_agent = SequentialAgent(
    name="decision_rag",
    description=(
        "Institutional analysis pipeline for Supreme Court decision corpus. "
        "Retrieves blocks, maps joins, identifies holdings, classifies fractures, "
        "applies Marks v. United States analysis, and synthesizes a grounded report."
    ),
    sub_agents=[
        retriever_agent,
        join_analysis_agent,
        holding_agent,
        fracture_agent,
        marks_agent,
        synthesis_agent,
    ],
)
