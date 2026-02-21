# decision_rag_adk/

Google ADK agent package. 6-agent sequential pipeline for institutional analysis of Supreme Court decisions.

## Pipeline

```
User query
  -> retriever (flash)           vector search + manifest load
  -> join_analysis (pro)         justice-to-section vote mapping
  -> holding_candidate (pro)     candidate holdings with width classification
  -> fracture_classifier (pro)   typed cross-opinion divergences
  -> marks_evaluator (pro)       narrowest-ground analysis
  -> synthesis (pro)             8-section grounded report
```

## Subdirectories

| Dir | Contents |
|-----|----------|
| `agents/` | 6 LlmAgent definitions, one per pipeline stage |
| `prompts/` | System prompt modules: shared invariants + per-agent instructions |
| `tools/` | Tool functions exposed to agents: corpus reads and RAG queries |

## Entry Point

`__init__.py` exports `root_agent` (a `SequentialAgent`). Run with:

```bash
adk run decision_rag_adk    # CLI
adk web .                   # web UI (run from project root)
```

## Configuration

`.env` must contain `GOOGLE_API_KEY`. Not committed to git.
