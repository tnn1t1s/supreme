# National Review Analysis Agent (NR-AA)

## Purpose

This system turns a paid National Review subscription into a **high-leverage analytical signal** rather than a passive reading habit.

The goal is **not** to scrape, replicate, or summarize National Review articles for redistribution.  
The goal is to **model NR as an institution** — its claims, frames, assumptions, and strategic posture — and make those artifacts queryable alongside legal, statutory, and policy corpora.

This agent functions as a *reader, distiller, and router* that feeds structured analysis into an existing multi-agent research pipeline.

---

## Core Design Principles

1. **Legitimacy First**
   - Respect NR’s paywall and terms of service.
   - No bulk scraping.
   - No storage of full article text.
   - Treat the agent as a *human reading assistant*, not a crawler.

2. **Analysis Artifacts, Not Content Artifacts**
   - Store *claims, frames, metadata, and excerpts* — not prose.
   - Every stored object must be independently reconstructable from memory + link.

3. **Institutional Modeling > Opinion Mining**
   - The unit of value is not “what NR said,” but:
     - what it *assumes*
     - what it *emphasizes*
     - what it *omits*
     - how those change over time

4. **Cross-Corpus Reasoning**
   - NR analysis must be queryable against:
     - Supreme Court opinions
     - statutes (e.g., IEEPA, Section 122)
     - administrative actions
   - The system should detect alignment, tension, and misapplication.

---

## System Architecture

### Components

- **NR Reader Agent** (human-in-the-loop, web-assisted)
- **Structured Notes Store** (JSON artifacts)
- **RAG Index** (claims + metadata only)
- **Synthesis / Audit Agents** (already existing in pipeline)

---

## Ingestion Workflow

### Step 1: Human-Authorized Reading

- User opens NR article in browser (logged in).
- Web agent assists navigation and extraction.
- No automated login or scraping.

### Step 2: Structured Extraction

For each article, the agent produces a **single JSON note file**.

#### File Path Convention

docs/sources/national_review/YYYY-MM-DD/<slug>.json


---

## JSON Schema (Canonical)

```json
{
  "source": "National Review",
  "url": "https://www.nationalreview.com/...",
  "title": "Article Title",
  "author": "Author Name",
  "published_at": "2026-02-22",
  "section": "Bench Memos | The Corner | News | Opinion",
  "topic_tags": [
    "SCOTUS",
    "tariffs",
    "executive_power",
    "major_questions"
  ],
  "stance_vector": {
    "executive_power": "favor_constraints | favor_discretion | mixed",
    "court_legitimacy": "support | skeptical | mixed",
    "congress_role": "pro_congress | anti_congress | mixed"
  },
  "claims": [
    {
      "claim": "The Court’s decision improperly restricts executive flexibility in foreign affairs.",
      "support_type": "textual | historical | institutional | economic | moral"
    },
    {
      "claim": "Congress’s abdication forces courts into a policymaking role.",
      "support_type": "institutional"
    }
  ],
  "anchors": [
    {
      "quote": "≤25 words from the article",
      "note": "Why this sentence anchors the author’s argument"
    }
  ],
  "assumptions": [
    "Foreign affairs powers should be interpreted broadly",
    "Congressional dysfunction is a given, not a correctable failure"
  ],
  "tensions_or_flags": [
    "Treats plurality MQ reasoning as de facto holding",
    "Conflates regulation with taxation"
  ],
  "questions_for_cross_analysis": [
    "Does the statutory text actually support this delegation claim?",
    "Which justices explicitly reject this framing?"
  ]
}
Indexing Rules (Critical)

Only the following fields are indexed into RAG:

title

author

published_at

section

topic_tags

stance_vector

claims.claim

claims.support_type

assumptions

tensions_or_flags

Anchors are stored but NOT indexed verbatim.
They are used only for citation integrity and recall grounding.

Queries This System Must Support

Examples:

“What is NR’s dominant framing of Learning Resources v. Trump?”

“Which NR authors treat the major questions doctrine as binding here?”

“List NR claims that conflict with the 6-justice statutory holding.”

“Show how NR’s view of executive emergency power has shifted over 30 days.”

Weekly Synthesis Job (High ROI)
Output: nr_weekly_frame_report.md

Contents:

Top recurring claims (frequency-weighted)

New frames introduced this week

Frames dropped since last week

Internal disagreements across authors

Citation patterns (courts, statutes, economists)

Drift indicators (hardening, moderation, fragmentation)

This turns the subscription into an institutional time-series model.

Integration with Legal / Policy Corpus

When NR content references a case or statute already in the system:

The pipeline should auto-run:

Claim Audit

Supported by corpus

Contradicted by corpus

Outside corpus (policy / rhetoric)

Misapplication Detection

Plurality vs holding

Dicta vs binding language

Category errors (e.g., regulation ≠ taxation)

Strategic Framing Analysis

Is NR describing constraint, channeling, or expansion of power?

Does the frame align with dissent or majority logic?

Agent Prompt (Reader Agent)
You are a subscriber-reading assistant.

You must not scrape in bulk, bypass paywalls, or reproduce full articles.

Given a National Review article URL that the user is authorized to view,
produce a structured JSON analysis artifact.

Rules:
- No full-text copying.
- Max 3 direct quotes, each ≤25 words.
- All claims must be paraphrased.
- Identify assumptions and framing choices.
- Flag potential misapplications of law.
- Output JSON only, matching the canonical schema.
- Save to the specified file path.

Return:
1) file path written
2) a 5-bullet summary of analytical takeaways
What This System Is (and Is Not)

It IS:

A way to extract durable insight from elite media

A bridge between journalism, law, and policy analysis

A force multiplier for a paid subscription

It is NOT:

A content scraper

A plagiarism engine

A partisan amplifier

Success Criteria

The system is successful if:

You can explain NR’s position better than NR commenters

You can predict how NR will frame the next related decision

You can respectfully steelman NR arguments without adopting them

You no longer confuse rhetoric with doctrine

At that point, the $59/year has paid for itself many times over.


---

If you want, next steps could be:
- A **Bench Memos–specific stance taxonomy**
- A **“plurality misuse detector”** module
- Or adapting this exact spec for *American Affairs* or *Compact*
