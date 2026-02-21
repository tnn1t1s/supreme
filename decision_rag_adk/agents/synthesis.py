from google.adk.agents import LlmAgent

from ..prompts import SYNTHESIS_INSTRUCTION

synthesis_agent = LlmAgent(
    name="synthesis",
    model="gemini-2.5-pro",
    instruction=SYNTHESIS_INSTRUCTION,
    tools=[],
    description="Produces a comprehensive 8-section human-readable analysis from all upstream state.",
)
