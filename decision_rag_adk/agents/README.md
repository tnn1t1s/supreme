# agents/

One `LlmAgent` per pipeline stage. Each agent:

- Receives upstream state via `{state_key}` template interpolation
- Has access to corpus tools (`read_block`, `list_blocks`, `query_decision_rag`)
- Outputs structured JSON stored in session state via `output_key`

| File | Agent | Model | output_key | Tools |
|------|-------|-------|------------|-------|
| `retriever.py` | retriever | gemini-2.5-flash | `retrieved_blocks` | query_decision_rag, load_manifest |
| `join_analysis.py` | join_analysis | gemini-2.5-pro | `join_structure` | read_block, list_blocks |
| `holding.py` | holding_candidate | gemini-2.5-pro | `holding_candidates` | read_block |
| `fracture.py` | fracture_classifier | gemini-2.5-pro | `fractures` | read_block, list_blocks |
| `marks.py` | marks_evaluator | gemini-2.5-pro | `marks_analysis` | read_block |
| `synthesis.py` | synthesis | gemini-2.5-pro | *(final output)* | none |
