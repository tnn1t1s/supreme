# Institutional Decision Analysis Engine
## Case Study: *Learning Resources, Inc. v. Trump* (2026)

---

## Purpose

This repository documents a case study in building a **transparent, stateful, institutional-grade analysis agent** for Supreme Court decisions.

The core question motivating this work is:

> Can an AI system reason like an institutional legal analyst—tracking holdings, pluralities, fractures, and doctrinal consequences over time—without collapsing into narrative, persuasion, or "LLM slop"?

Using *Learning Resources, Inc. v. Trump* as a test case, this project demonstrates that **system design, not model capability**, is the primary determinant of analytical quality in legal reasoning tasks.

---

## What This System Is

This system is:

- A **long-lived analytical agent**, not a one-shot Q&A tool
- Built around a **block-level decision corpus**
- Designed for **internal institutional analysis**, not public commentary
- Fully **observable**, with traceable reasoning steps
- Constrained to produce **clerical, non-performative outputs**

It behaves like a junior institutional analyst who:
- tracks joins precisely
- distinguishes holdings from reasoning
- applies *Marks v. United States* correctly
- anticipates misapplication by downstream courts

---

## What This System Is Not

This system is not:

- A chatbot
- A summarization engine
- A political narrative generator
- A persuasion or advocacy tool
- A black-box "legal AI"

It does not optimize for eloquence, confidence, or speed at the expense of correctness.

---

## Why This Case

*Learning Resources, Inc. v. Trump* is a particularly strong stress test because:

- The judgment (6–3) masks **fractured reasoning**
- A **three-justice plurality** appears inside an "opinion of the Court"
- The binding holding rests on **narrow statutory interpretation**
- Media narratives diverged sharply from institutional reality

This makes the case ideal for testing:
- plurality detection
- holding identification
- *Marks* analysis
- downstream misapplication risk

---

## Decision Corpus Design

The decision is ingested as **53 discrete blocks** extracted from:

- Syllabus
- Majority opinion
- Concurrences
- Concurrences in part
- Dissents

Each block is stored with YAML frontmatter metadata, including:

```yaml
justice: Roberts
opinion_type: majority
title: "II-B"
case: "Learning Resources, Inc. v. Trump"
docket: "24-1287"
page_start: 20
page_end: 22
doctrines:
  - statutory_interpretation
  - taxing_power
holding_width: case_specific
width_note: "'regulate' in IEEPA does not include tariff authority"
```

Block-level granularity is the foundation of the system's accuracy.
Doctrines, holdings, and fractures are never inferred at the opinion level.

---

## Sequential Reasoning Pipeline

The agent operates as a multi-stage, inspectable pipeline:

### Retriever

- Loads decision manifest
- Queries blocks by doctrine, justice, section, or role

### Join Analysis

- Determines which justices joined which sections
- Explicitly identifies plurality vs majority joins

### Holding Candidate Generator

- Enumerates candidate holdings
- Requires explicit declaration of holding width:
  - `case_specific`
  - `general_principle`

### Fracture Classifier

- Records doctrinal fractures using cold fields only:
  - `vote_split`
  - `majority_required`
  - `affects_outcome`

### Marks Evaluator

- Applies *Marks v. United States* when no single rationale commands five votes
- Identifies the narrowest controlling ground

### Synthesis

- Produces clerical, institutional prose
- Justices and opinions are always the actors
- No evaluative adverbs
- No forward-looking claims unless explicitly requested

All stages are fully observable via trace and span logging.

---

## Key Design Decisions (and Why They Matter)

### 1. Block-Level Doctrine Tagging

Doctrines are attached per block, not per opinion.

This prevents:
- treating an entire opinion as doctrinally uniform
- accidental elevation of plurality reasoning
- loss of precision in fractured cases

### 2. Holding Width Enforcement

Every candidate holding must declare its scope:

```yaml
holding_width: case_specific | general_principle
width_note: "operative statutory language"
```

This eliminates silent over-generalization, the most common failure mode in legal analysis.

### 3. Cold Fracture Fields

Fractures are never labeled "minor" or "major."

Instead, they are described factually:

```yaml
vote_split: "3-3"
majority_required: false
affects_outcome: false
```

Interpretation is left to the reader, not the system.

### 4. Clerical Voice Constraint

The system enforces:
- No rhetorical framing
- No narrative conclusions
- No "the Court rebuked" language
- No implied intent or motive

This single constraint is the primary reason the output does not read like LLM-generated prose.

---

## Case Study Findings

### Binding Holding

A majority of six justices held that, under ordinary statutory interpretation, the authority to "regulate...importation" in the International Emergency Economic Powers Act does not include the power to impose tariffs. Taxing authority is distinct and must be delegated explicitly.

This holding is found in Part II-B of the Chief Justice's opinion and was joined by all six justices in the majority.

### Plurality Reasoning

Only three justices (Roberts, Gorsuch, Barrett) joined the Major Questions Doctrine analysis in Parts II-A-2 and III.

Because this reasoning did not command five votes, it is plurality reasoning, not a holding.

### Correct Marks Analysis

Applying *Marks v. United States*:

- The narrowest ground explaining the judgment is the statutory interpretation rationale.
- Justice Kagan's concurrence (joined by Sotomayor and Jackson) explicitly rested on that ground alone.
- The Major Questions Doctrine analysis is non-binding.

### Primary Misapplication Risk

The system identified the dominant failure mode for lower courts:

**Treating the three-justice Major Questions analysis as a binding holding.**

This misapplication is made plausible by:
- the placement of the plurality reasoning inside the "opinion of the Court"
- superficial reading that ignores join instructions
- failure to apply *Marks*

The blocks that reveal this error are:
- `roberts_majority_0001` (explicit join limitation)
- `kagan_concurrence_in_part_0001` (rejection of MQ necessity)
- `roberts_majority_0006` (actual holding)

---

## Why This Matters

This case study demonstrates that:

- Modern frontier models are already sufficient for institutional legal reasoning
- The limiting factor is structure, observability, and constraint
- Transparent systems outperform opaque ones even on older models
- Legal reasoning quality depends more on procedural honesty than fluency

---

## Takeaway

This project shows that it is possible to build AI systems that:

- reason institutionally rather than narratively
- preserve doctrinal nuance over time
- support sustained inquiry instead of one-shot answers
- act as analytical tools rather than opinion engines

The result is not faster answers, but trustworthy ones.

---

## Cross-Corpus Extension: Section 122 Global Import Surcharge

Following the Supreme Court's decision in *Learning Resources*, the President immediately invoked Section 122 of the Trade Act of 1974 (19 U.S.C. § 2132) to impose a 10% global import surcharge, announced to increase to 15%.

The corpus has been extended with 21 blocks from three primary source documents:

- **Statute**: 19 U.S.C. § 2132 (9 blocks, segmented by subsection)
- **Presidential Proclamation** (February 20, 2026): Balance-of-payments findings, operative clauses, exemptions, severability (8 blocks)
- **White House Fact Sheet** (February 20, 2026): Policy summary, economic context, trade policy direction (4 blocks)

This extension enables cross-corpus analysis: querying across both the judicial decision and the executive response. The ADK pipeline can now draw on Section 122's explicit statutory delegation language when evaluating the *Learning Resources* majority's holding that Congress delegates tariff authority "clearly and with careful constraints."

## Status

This repository documents a working multi-corpus analytical system with a completed case study and cross-corpus extension.
The Section 122 corpus demonstrates the system's ability to ingest non-judicial primary sources (statutes, executive actions) alongside court decisions for comparative institutional analysis.
