# Contributing

## Adding a New Case

### 1. Extract the decision

Place the slip opinion PDF at:

```
docs/decision/{date}_{case-name}_{docket}/source/{docket}_slip_opinion.pdf
```

Edit `tools/bin/extract-decision` to add the new case's opinion structure (justices, types, page ranges). Then run:

```bash
.venv/bin/python tools/bin/extract-decision
```

This produces segmented markdown blocks with YAML frontmatter and a `manifest.json`.

### 2. Rebuild the index

```bash
just decision-ingest
```

### 3. Add a case README

Create `docs/decision/{date}_{case-name}_{docket}/README.md` with the opinion table, block counts, and any case-specific notes.

## Tuning Agent Prompts

All prompts live in `decision_rag_adk/prompts/`. Changes take effect on the next query without restarting the web server.

### Invariants (`invariants.py`)

The 7 global rules injected into every agent. Edit with extreme care — these are the system's primary quality controls.

### Agent instructions

Each agent has its own prompt file. The key tuning surfaces are:

| File | What to tune |
|------|-------------|
| `holding.py` | Width classification rules, holding vs reasoning criteria |
| `fracture.py` | Fracture type definitions, measurable fields |
| `marks.py` | Marks v. United States application rules, skepticism thresholds |
| `synthesis.py` | Voice rules, section structure, citation format |
| `retriever.py` | Search strategy, filter logic |
| `join_analysis.py` | Join verification rules |

### Testing a prompt change

1. Start the web UI: `just decision-adk-web`
2. Run the same query before and after the change
3. Compare the agent-level outputs (visible in the UI)
4. Check that all 7 invariants still hold in the synthesis

## Adding a New Agent

1. Create `decision_rag_adk/agents/{name}.py` with an `LlmAgent`
2. Create `decision_rag_adk/prompts/{name}.py` with the instruction
3. Add the import to `decision_rag_adk/agents/__init__.py` and `prompts/__init__.py`
4. Insert the agent into the `sub_agents` list in `decision_rag_adk/__init__.py`
5. Set `output_key` so downstream agents can reference the output via `{key_name}`

## Adding a New Tool

1. Add the function to `decision_rag_adk/tools/retrieval.py` or `corpus.py`
2. Export it from `decision_rag_adk/tools/__init__.py`
3. Add it to the relevant agent's `tools=[]` list

Tool functions are plain Python. If a parameter is named `tool_context`, ADK injects a `ToolContext` for session state access.

## Code Standards

- No comments in code unless the logic is non-obvious
- Tools return dicts or lists, not JSON strings
- Prompts use `{state_key?}` (with `?`) for optional state references
- Agent names must be valid Python identifiers
- All claims in prompts must be verifiable against the corpus

## Commit Messages

Follow the existing pattern:

```
Short summary of what changed

Longer description if needed. Reference specific files
or design decisions.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```
