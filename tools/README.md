# tools/

CLI tools for corpus ingestion, retrieval, analysis, and debugging.

## tools/bin/

| Tool | Purpose |
|------|---------|
| `decision-rag` | LlamaIndex vector search over decision blocks with metadata filtering (-j, -t, -d, -c, -a, --doc-type) |
| `decision-adk` | Launcher for the 8-agent ADK analysis pipeline (CLI and web UI) |
| `extract-decision` | Converts slip opinion PDF into segmented markdown blocks with doctrine tagging |
| `extract-section122` | Converts Section 122 source HTML into segmented markdown blocks |
| `nr-ingest` | Converts National Review JSON artifacts into markdown blocks + rebuilds index |
| `dap-trace` | Execution trace analyzer: plans, timelines, validation, session comparison |
| `adk-sessions` | Retrieves prompt/response pairs from ADK session history database |
| `podcast-rag` | Podcast transcript RAG (legacy, unrelated to decision analysis) |

## ADK Tools (decision_rag_adk/tools/)

Python functions exposed as ADK tools to the pipeline agents.

| File | Functions | How it works |
|------|-----------|--------------|
| `retrieval.py` | `query_decision_rag` | Shells out to `tools/bin/decision-rag query --json` using venv Python. Supports justice, opinion_type, doctrine, corpus, author filters. |
| `corpus.py` | `load_manifest`, `read_block`, `list_blocks` | Direct filesystem reads against `docs/decision/`. Parses YAML frontmatter from block files. |

Agents receive these as plain functions in their `tools=[]` list. ADK auto-wraps them as `FunctionTool`.

## dap-trace Commands

| Command | Purpose |
|---------|---------|
| `dap-trace list` | List sessions with DAP plan summaries |
| `dap-trace plan SESSION_ID` | Show compiled plan for a session |
| `dap-trace timeline SESSION_ID` | Agent timing waterfall |
| `dap-trace validate SESSION_ID` | Check plan vs actual execution |
| `dap-trace compare SESSION_A SESSION_B` | Side-by-side plan comparison |
| `dap-trace features "query"` | Dry-run: show detected intents |
| `dap-trace compile "query"` | Dry-run: show compiled plan |

All commands support `--json` for machine-readable output and `--llm` for LLM-based planning (features/compile only).
