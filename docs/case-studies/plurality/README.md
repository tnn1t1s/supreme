# Plurality Analysis: Learning Resources, Inc. v. Trump

This directory contains the output of three pipeline runs analyzing the plurality structure in *Learning Resources, Inc. v. Trump* (24-1287).

## Why This Case Has a Plurality Problem

The judgment is 6-3, but the reasoning fractures 3-3 within the majority:

- **Roberts, Gorsuch, Barrett** joined the full opinion, including the Major Questions Doctrine analysis (Parts II-A-2, III)
- **Kagan, Sotomayor, Jackson** joined only the statutory interpretation sections (Parts I, II-A-1, II-B), explicitly rejecting the Major Questions Doctrine as unnecessary

This means the Major Questions Doctrine reasoning is **plurality, not holding** — despite appearing inside the "opinion of the Court."

## What to Read

### If you want the core analysis
Read [run-01-ieepa-basic/synthesis.md](run-01-ieepa-basic/synthesis.md). This is a clean, single-query pass through the full pipeline answering "Does IEEPA authorize the President to impose tariffs?"

### If you want to verify consistency
Compare [run-01](run-01-ieepa-basic/) and [run-02](run-02-ieepa-rerun/). Same query, independent runs. The structural conclusions are stable; prose varies.

### If you want the deepest analysis
Read [run-03-multi-query/](run-03-multi-query/). Four queries in one session:

1. **[Narrowest controlling principle](run-03-multi-query/query-1-synthesis.md)** — the structural heart of the analysis
2. **[Hypothetical IEEPA amendment](run-03-multi-query/query-2-synthesis.md)** — which fractures survive if Congress fixes the statute
3. **[Misapplication risk](run-03-multi-query/query-3-synthesis.md)** — how lower courts could get this wrong (the most practically useful output)
4. **[Populist blog response](run-03-multi-query/query-4-synthesis.md)** — clerical voice under political pressure
5. **[Adversarial critique response](run-03-multi-query/query-5-synthesis.md)** — non-partisan memorandum rebutting a political critique
6. **[Left-leaning perspective analysis](run-03-multi-query/query-6-synthesis.md)** — where the "rebuke of Trumpism" reading is strongest and weakest

### If you want to see inside the pipeline
Each run directory contains the raw output of every agent stage. Read them in order:

1. `retriever.md` — what blocks were found
2. `join_analysis.md` — the vote structure (JSON)
3. `holding_candidate.md` — candidate holdings ranked by support (JSON)
4. `fracture_classifier.md` — typed disagreements with vote splits (JSON)
5. `marks_evaluator.md` — narrowest-ground analysis (JSON)
6. `synthesis.md` — the final human-readable report

## Runs

| Run | Query | Reports | Files |
|-----|-------|---------|-------|
| [run-01-ieepa-basic](run-01-ieepa-basic/) | Does IEEPA authorize tariffs? | 1 | 7 |
| [run-02-ieepa-rerun](run-02-ieepa-rerun/) | Does IEEPA authorize tariffs? (rerun) | 1 | 7 |
| [run-03-multi-query](run-03-multi-query/) | Narrowest principle, hypothetical, misapplication, blog response, adversarial critique, left-leaning perspective | 6 | 42 |

## Key Findings Across All Runs

1. **Binding holding**: IEEPA does not authorize tariffs — grounded in ordinary statutory interpretation, supported by 6 justices
2. **Plurality reasoning**: Major Questions Doctrine analysis commands only 3 justices — not binding precedent
3. **Marks analysis**: Kagan's concurrence (statutory interpretation only) is the narrowest ground, a logical subset of the plurality's reasoning
4. **Primary misapplication risk**: Lower courts treating the plurality's MQ reasoning as holding, enabled by its placement inside the "opinion of the Court"
