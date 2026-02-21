# tools/

Python functions exposed as ADK tools to the pipeline agents.

| File | Functions | How it works |
|------|-----------|--------------|
| `retrieval.py` | `query_decision_rag` | Shells out to `tools/bin/decision-rag query --json` using the venv Python |
| `corpus.py` | `load_manifest`, `read_block`, `list_blocks` | Direct filesystem reads against `docs/decision/` |

Agents receive these as plain functions in their `tools=[]` list. ADK auto-wraps them as `FunctionTool`.
