# agents/

One `LlmAgent` per pipeline stage. Each agent:

- Receives upstream state via `{state_key?}` template interpolation
- Has access to corpus tools (`read_block`, `list_blocks`, `query_decision_rag`)
- Outputs structured JSON stored in session state via `output_key`

## Agent Registry

| File | Agent Name | Model | output_key | Tools | Triggers |
|------|------------|-------|------------|-------|----------|
| `retriever.py` | retriever | gemini-2.5-flash | `retrieved_blocks` | query_decision_rag, load_manifest | precedent, compliance, commentary_assessment, factual_summary |
| `join_analysis.py` | join_analysis | gemini-2.5-pro | `join_structure` | read_block, list_blocks | precedent |
| `holding.py` | holding_candidate | gemini-2.5-pro | `holding_candidates` | read_block | precedent |
| `fracture.py` | fracture_classifier | gemini-2.5-pro | `fractures` | read_block, list_blocks | precedent |
| `marks.py` | marks_evaluator | gemini-2.5-pro | `marks_analysis` | read_block | marks |
| `claim_assessment.py` | claim_assessor | gemini-2.5-pro | `claim_assessments` | read_block | commentary_assessment |
| `impact.py` | impact_analyst | gemini-2.5-pro | `impact_notes` | none | commentary_assessment |
| `synthesis.py` | synthesis | gemini-2.5-pro | *(terminal)* | none | all intents |

## Dependency Chain

The DAP compiler determines execution order from `config/affordances.yaml`. Typical chains:

```
precedent only:
  retrieval -> vote_structure -> holdings -> fractures -> synthesis

commentary_assessment only:
  retrieval -> claim_assessment -> impact_analysis -> synthesis

all intents:
  retrieval -> vote_structure -> holdings -> fractures -> marks
           -> claim_assessment -> impact_analysis -> synthesis
```

## Claim Assessment Output Schema

The `claim_assessor` produces structured JSON:

```json
{
  "source_article": {"author": "...", "publication": "...", "date": "...", "title": "..."},
  "claims": [
    {
      "claim_id": "C1",
      "claim_text": "...",
      "category": "vote_structure|holding|statutory_interpretation|doctrinal|factual|framing",
      "status": "SUPPORTED|CONTRADICTED|MISAPPLICATION|OMISSION|OUTSIDE_CORPUS",
      "status_detail": "...",
      "evidence": [{"block_id": "...", "page_range": "...", "relevance": "..."}],
      "severity": "high|medium|low"
    }
  ],
  "summary": {"total_claims": 5, "supported": 2, "contradicted": 1, "misapplication": 1, "omission": 1, "outside_corpus": 0}
}
```

## Impact Analysis Output Schema

The `impact_analyst` produces:

```json
{
  "impacts": [
    {
      "claim_ref": "C1",
      "mechanism": "what readers/courts would do based on the error",
      "error_mode": "Scope inflation|Vote count error|Doctrinal conflation|...",
      "downstream_sites": ["lower_courts", "agencies", "legal_commentary"],
      "confidence": "high|medium|low",
      "scope": "systemic|case_specific|rhetorical"
    }
  ],
  "empty": false
}
```

When no actionable claims exist: `{"impacts": [], "empty": true}`
