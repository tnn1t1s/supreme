# Run 01: IEEPA Basic

**Query:** Does IEEPA authorize the President to impose tariffs?

**Date:** 2026-02-21

First run of the pipeline. Single query, full 6-agent pass.

## Files

| File | Agent | What it contains |
|------|-------|-----------------|
| [query.md](query.md) | user | The input query |
| [retriever.md](retriever.md) | retriever | Manifest summary + 10 retrieved blocks with scores |
| [join_analysis.md](join_analysis.md) | join_analysis | Vote structure: 6-3 judgment, 3-3 reasoning split |
| [holding_candidate.md](holding_candidate.md) | holding_candidate | 4 candidate holdings ranked by majority support |
| [fracture_classifier.md](fracture_classifier.md) | fracture_classifier | 6 typed fractures across doctrinal, scope, factual, methodological |
| [marks_evaluator.md](marks_evaluator.md) | marks_evaluator | Marks analysis: Kagan's statutory interpretation as narrowest ground |
| [synthesis.md](synthesis.md) | synthesis | Full 8-section report with citations |

## Key Finding

Six justices agreed IEEPA does not authorize tariffs. The reasoning split 3-3: plurality added the Major Questions Doctrine, concurrence relied on statutory interpretation alone. Under Marks, the statutory interpretation ground controls.
