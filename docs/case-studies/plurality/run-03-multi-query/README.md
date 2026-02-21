# Run 03: Multi-Query Session

**Date:** 2026-02-21

A six-query session that stress-tests the pipeline across different analytical modes: structural analysis, hypothetical reasoning, misapplication detection, public communication, adversarial response, and partisan perspective analysis.

## Queries

### Query 1: Narrowest Controlling Principle
> What is the narrowest controlling principle that explains the judgment, and where do the concurrences and dissents explicitly reject or resist that principle?

The core analytical question. Files: `query-1-*.md`

### Query 2: Hypothetical IEEPA Amendment
> Assume a future case in which Congress amends IEEPA to authorize the President to "regulate importation, including through duties or tariffs, during a declared national emergency." Based solely on the reasoning in this decision, which doctrinal fractures would persist, which would dissolve, and what new fractures might emerge?

Tests whether the pipeline can reason counterfactually while staying grounded. Files: `query-2-*.md`

### Query 3: Misapplication Risk
> How could a lower court plausibly misapply Learning Resources, Inc. v. Trump while claiming fidelity to it, and which specific blocks in the decision would reveal that misapplication?

The most practically useful query — identifies the dominant failure mode (treating three-justice MQ reasoning as binding holding). Files: `query-3-*.md`

### Query 4: Populist Blog Response
> Respond to a populist blog post with a structured, non-partisan breakdown.

Tests the pipeline's ability to produce clerical institutional prose in response to a political framing. The agents produced a formal memorandum format. Files: `query-4-*.md`

### Query 5: Non-Partisan Memorandum (Adversarial Critique)
> Produce a structured, non-partisan memorandum responding to the critique: "The Supreme Court substituted its own economic policy preferences for the elected President's judgment during a national emergency..."

Tests adversarial response: pipeline must rebut a political critique using only grounded reasoning, distinguishing statutory interpretation from policy disagreement. Files: `query-5-*.md`

### Query 6: Left-Leaning Institutional Perspective
> From a left-leaning institutional perspective that views Learning Resources, Inc. v. Trump as a rebuke of Trumpism, identify where that interpretation is strongest, and where it is weakest.

Tests partisan-perspective analysis: pipeline must identify both the strongest and weakest grounds for a left-leaning reading, while remaining grounded in the opinions. Files: `query-6-*.md`

## File Pattern

Each query produces 7 files:

```
query-{N}-query.md                 # the input
query-{N}-retriever.md             # retrieved blocks
query-{N}-join_analysis.md         # vote structure
query-{N}-holding_candidate.md     # candidate holdings
query-{N}-fracture_classifier.md   # typed fractures
query-{N}-marks_evaluator.md       # narrowest-ground analysis
query-{N}-synthesis.md             # final report
```

## What to Read

- **Start with** `query-1-synthesis.md` — the most complete structural analysis
- **Then read** `query-3-synthesis.md` — the misapplication risk analysis is the most practically valuable output
- **Compare** `query-2-synthesis.md` to see how the pipeline handles hypotheticals
- **Read** `query-4-synthesis.md` to see the clerical voice constraint under pressure
- **Read** `query-5-synthesis.md` for the adversarial critique response
- **Read** `query-6-synthesis.md` for the partisan perspective stress-test
