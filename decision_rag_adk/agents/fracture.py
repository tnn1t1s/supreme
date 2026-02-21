from google.adk.agents import LlmAgent

from ..prompts import FRACTURE_INSTRUCTION
from ..tools.corpus import read_block, list_blocks

fracture_agent = LlmAgent(
    name="fracture_classifier",
    model="gemini-2.5-pro",
    instruction=FRACTURE_INSTRUCTION,
    tools=[read_block, list_blocks],
    output_key="fractures",
    description="Classifies typed divergences between opinions across 5 fracture categories.",
)
