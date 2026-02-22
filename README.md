# supremes-tariif

Institutional analysis toolkit for Supreme Court decisions and related primary sources. Multi-corpus RAG with cross-document analysis.

## Corpora

| Corpus | Blocks | Source |
|--------|--------|--------|
| *Learning Resources, Inc. v. Trump* (24-1287) | 53 | Slip opinion PDF (8 opinions) |
| Section 122 Global Import Surcharge | 21 | Statute, proclamation, fact sheet |

## Tools

### decision-rag (retrieval)

Vector search over 74 segmented blocks with metadata filtering. Supports cross-corpus queries.

```bash
just decision-query "taxing power"              # search all blocks
just decision-justice "IEEPA" Roberts            # filter by justice
just decision-doctrine "delegation" nondelegation # filter by doctrine
just decision-corpus "Section 122" section122_global_tariff  # filter by corpus
just decision-doctype "surcharge" proclamation   # filter by doc type
just decision-json "regulate importation"        # JSON output
just decision-list                               # list indexed decisions
```

### decision-adk (analysis pipeline)

6-agent sequential pipeline on Google ADK. Each agent reads the corpus, builds structured JSON, and passes state to the next.

```
User query
  -> RetrieverAgent (flash)     vector search + manifest load
  -> JoinAnalysisAgent (pro)    justice-to-section vote mapping
  -> HoldingCandidateAgent (pro) candidate holdings with width classification
  -> FractureClassifierAgent (pro) typed cross-opinion divergences
  -> MarksEvaluatorAgent (pro)  narrowest-ground analysis
  -> SynthesisAgent (pro)       8-section grounded report
```

```bash
just decision-adk              # interactive CLI
just decision-adk-web          # web UI at http://127.0.0.1:8000
tools/bin/decision-adk --help  # usage
```

#### 7 Global Invariants

Every agent enforces:

1. **Grounding** -- every claim cites block_id + page range
2. **Holding discipline** -- holding vs reasoning vs dicta
3. **No narrative collapse** -- individual justice attribution
4. **Minimality bias** -- narrowest reading preferred
5. **Doctrine precision** -- exact doctrinal labels
6. **No motive inference** -- text only, no speculation
7. **Marks skepticism** -- flag uncertainty in narrowest-ground analysis

#### Corpus: Learning Resources v. Trump

53 blocks across 8 opinions from the slip opinion PDF:

| Justice | Type | Blocks | Pages |
|---------|------|--------|-------|
| Syllabus | syllabus | 2 | 1-6 |
| Roberts | majority | 7 | 7-27 |
| Gorsuch | concurrence | 16 | 28-73 |
| Barrett | concurrence | 1 | 74-77 |
| Kagan | concurrence in part | 2 | 78-84 |
| Jackson | concurrence in part | 1 | 85-89 |
| Thomas | dissent | 9 | 90-107 |
| Kavanaugh | dissent | 15 | 108-170 |

#### Corpus: Section 122 Global Import Surcharge

21 blocks across 3 primary source documents:

| Document | Type | Blocks |
|----------|------|--------|
| 19 U.S.C. § 2132 | statute | 9 |
| Presidential Proclamation (2026-02-20) | proclamation | 8 |
| White House Fact Sheet (2026-02-20) | fact_sheet | 4 |

Pending sources: Federal Register notice, CBP implementation guidance.

### Ingestion tools

```bash
just decision-pipeline         # extract Learning Resources + ingest
just section122-pipeline       # extract Section 122 + ingest
just extract-section122        # extract Section 122 blocks only
```

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install llama-index llama-index-embeddings-huggingface pdfplumber google-adk
just decision-pipeline         # extract blocks + build vector index
```

Set your Gemini API key in `decision_rag_adk/.env`:
```
GOOGLE_API_KEY=your-key-here
```

## Structure

```
tools/bin/
  decision-rag          # RAG retriever CLI (LlamaIndex + BGE embeddings)
  decision-adk          # ADK pipeline launcher
  extract-decision      # PDF -> markdown blocks (Learning Resources)
  extract-section122    # HTML -> markdown blocks (Section 122 corpus)

decision_rag_adk/       # Google ADK agent package
  __init__.py           # root_agent (SequentialAgent)
  agents/               # 6 LlmAgents
  tools/                # retrieval.py (shells to decision-rag), corpus.py (filesystem)
  prompts/              # invariants.py + 6 agent instructions

docs/decision/          # corpus (blocks, extracted text, manifest.json)
.rag_index_decision/    # persisted vector index
```
