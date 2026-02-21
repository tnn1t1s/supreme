from google.adk.agents import LlmAgent

from ..prompts import MARKS_INSTRUCTION
from ..tools.corpus import read_block

marks_agent = LlmAgent(
    name="marks_evaluator",
    model="gemini-2.5-pro",
    instruction=MARKS_INSTRUCTION,
    tools=[read_block],
    output_key="marks_analysis",
    description="Applies Marks v. United States narrowest-ground analysis to identify the controlling principle.",
)
