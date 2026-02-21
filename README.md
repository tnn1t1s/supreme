# supremes-tariif

Institutional analysis toolkit for Supreme Court decisions. Built around the *Learning Resources, Inc. v. Trump* (24-1287) tariff case.

## Tools

### decision-rag (retrieval)

Vector search over 53 segmented opinion blocks with metadata filtering.

```bash
just decision-query "taxing power"              # search all opinions
just decision-justice "IEEPA" Roberts            # filter by justice
just decision-doctrine "delegation" nondelegation # filter by doctrine
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

#### Corpus

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

### extract-decision (ingestion)

Converts slip opinion PDF into segmented markdown blocks with YAML frontmatter and automated doctrine tagging.

```bash
just decision-pipeline         # extract + ingest
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
  extract-decision      # PDF -> markdown blocks

decision_rag_adk/       # Google ADK agent package
  __init__.py           # root_agent (SequentialAgent)
  agents/               # 6 LlmAgents
  tools/                # retrieval.py (shells to decision-rag), corpus.py (filesystem)
  prompts/              # invariants.py + 6 agent instructions

docs/decision/          # corpus (blocks, extracted text, manifest.json)
.rag_index_decision/    # persisted vector index
```
