from google.adk.agents import LlmAgent

from ..prompts import HOLDING_INSTRUCTION
from ..tools.corpus import read_block

holding_agent = LlmAgent(
    name="holding_candidate",
    model="gemini-2.5-pro",
    instruction=HOLDING_INSTRUCTION,
    tools=[read_block],
    output_key="holding_candidates",
    description="Identifies candidate holdings from the majority opinion ranked by majority support.",
)
