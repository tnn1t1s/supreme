from google.adk.agents import LlmAgent

from ..prompts import CLAIM_ASSESSMENT_INSTRUCTION
from ..tools.corpus import read_block

claim_assessment_agent = LlmAgent(
    name="claim_assessor",
    model="gemini-2.5-pro",
    instruction=CLAIM_ASSESSMENT_INSTRUCTION,
    tools=[read_block],
    output_key="claim_assessments",
    description="Extracts and classifies claims from external commentary against primary corpus.",
)
