# decision_rag_adk/

Google ADK agent package. 8-agent pipeline for institutional analysis of Supreme Court decisions with a Deterministic Affordance Planner (DAP).

## Architecture

The pipeline is not a fixed chain. A query planner analyzes intent and compiles an execution DAG from `config/affordances.yaml`. Only relevant agents run.

### Full Agent Chain (all intents active)

```
retrieval (flash)
  -> vote_structure (pro)      justice-to-section vote mapping
  -> holdings (pro)            candidate holdings with width classification
  -> fractures (pro)           typed cross-opinion divergences
  -> marks (pro)               narrowest-ground analysis
  -> claim_assessment (pro)    structured claim extraction + classification
  -> impact_analysis (pro)     downstream impact of misapplied claims
  -> synthesis (pro)           multi-section grounded report (terminal)
```

### Planner

The DAP planner lives in `planner/`:

1. **Query Analyzer** (`query_analyzer.py`) detects intents: `precedent`, `marks`, `commentary_assessment`, `compliance`, `factual_summary`
2. **Compiler** (`compiler.py`) reads `config/affordances.yaml`, selects affordances matching active intents, resolves dependencies, and builds a DAG
3. **Executor** (`executor.py`) runs agents in DAG order, passing state between them

Two planner backends:
- **Heuristic** (`heuristic.py`) — regex/keyword rules, default
- **LLM** (`llm_planner.py`) — Gemini-based intent detection, set `DAP_PLANNER=llm`

### Affordance Catalog

Each affordance in `config/affordances.yaml` declares:
- `triggers_any` — which intents activate it
- `requires` — preconditions (state keys, corpus presence)
- `inputs` / `outputs` — state keys consumed and produced
- `cost` — `small | medium | large`
- `phase: terminal` — only synthesis has this

The compiler resolves the dependency closure automatically. If `impact_analysis` requires `claim_assessments`, and `claim_assessment` requires `retrieved_blocks`, the compiler pulls both into the plan.

## Subdirectories

| Dir | Contents |
|-----|----------|
| `agents/` | 8 LlmAgent definitions |
| `prompts/` | Shared invariants + per-agent instructions |
| `tools/` | Tool functions exposed to agents |
| `planner/` | DAP: query analysis, compilation, execution |

## Entry Point

`__init__.py` exports `root_agent` (a `DAPAgent`). Run with:

```bash
just decision-adk           # CLI
just decision-adk-web       # web UI at http://127.0.0.1:8000
```

## Configuration

`.env` must contain `GOOGLE_API_KEY`. Not committed to git.
