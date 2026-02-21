from google.adk.agents import LlmAgent

from ..prompts import RETRIEVER_INSTRUCTION
from ..tools.retrieval import query_decision_rag
from ..tools.corpus import load_manifest

retriever_agent = LlmAgent(
    name="retriever",
    model="gemini-2.5-flash",
    instruction=RETRIEVER_INSTRUCTION,
    tools=[query_decision_rag, load_manifest],
    output_key="retrieved_blocks",
    description="Searches the decision corpus and returns relevant blocks for the user's query.",
)
