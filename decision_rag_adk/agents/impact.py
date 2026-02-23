from google.adk.agents import LlmAgent

from ..prompts import IMPACT_INSTRUCTION

impact_agent = LlmAgent(
    name="impact_analyst",
    model="gemini-2.5-pro",
    instruction=IMPACT_INSTRUCTION,
    tools=[],
    output_key="impact_notes",
    description="Assesses downstream impact of misapplied, contradicted, or omitted claims.",
)
