from google.adk.agents import LlmAgent

from ..prompts import JOIN_ANALYSIS_INSTRUCTION
from ..tools.corpus import read_block, list_blocks

join_analysis_agent = LlmAgent(
    name="join_analysis",
    model="gemini-2.5-pro",
    instruction=JOIN_ANALYSIS_INSTRUCTION,
    tools=[read_block, list_blocks],
    output_key="join_structure",
    description="Maps which justices join which sections of each opinion.",
)
