# supremes-tariif

Institutional analysis toolkit for Supreme Court decisions and related primary sources. Multi-corpus RAG with cross-document analysis and automated commentary fact-checking.

## What This Does

Given a Supreme Court decision, this system:

1. **Segments** the slip opinion into attributed blocks (per-justice, per-section)
2. **Indexes** blocks with doctrinal metadata for vector search
3. **Analyzes** the decision through an 8-agent pipeline that maps votes, identifies holdings, classifies fractures, and applies Marks v. United States narrowest-ground analysis
4. **Cross-references** external commentary (e.g., National Review articles) against the primary legal record, producing structured claim assessments and impact analysis

The pipeline is deterministic: a query planner selects which agents run based on query intent, so simple factual lookups skip the full analysis chain.

## Corpora

| Corpus | Type | Blocks | Source |
|--------|------|--------|--------|
| *Learning Resources, Inc. v. Trump* (24-1287) | SCOTUS opinions | 53 | Slip opinion PDF (8 opinions) |
| Section 122 Global Import Surcharge | Statutory/executive | 21 | Statute, proclamation, fact sheet |
| National Review analysis | Media commentary | 2+ | Structured NR article artifacts |

## Quick Start

```bash
# 1. Setup
python3 -m venv .venv
.venv/bin/pip install llama-index llama-index-embeddings-huggingface pdfplumber google-adk

# 2. Set your Gemini API key
echo "GOOGLE_API_KEY=your-key-here" > decision_rag_adk/.env

# 3. Build the corpus + vector index
just decision-pipeline       # Learning Resources v. Trump
just section122-pipeline     # Section 122 statutory docs
just nr-ingest               # National Review articles (optional)

# 4. Run the analysis pipeline
just decision-adk            # interactive CLI
just decision-adk-web        # web UI at http://127.0.0.1:8000
```

## Retrieval (decision-rag)

Vector search over all indexed blocks with metadata filtering.

```bash
just decision-query "taxing power"                          # search all blocks
just decision-justice "IEEPA" Roberts                       # filter by justice
just decision-doctrine "delegation" nondelegation           # filter by doctrine
just decision-corpus "Section 122" section122_global_tariff # filter by corpus
just decision-doctype "surcharge" proclamation              # filter by doc type
just nr-query "majority holding"                            # search NR corpus
just nr-author "tariff" "McConnell"                         # NR by author
just decision-json "regulate importation"                   # JSON output
just decision-list                                          # list indexed decisions
```

## Analysis Pipeline (decision-adk)

8-agent pipeline on Google ADK with a Deterministic Affordance Planner (DAP). The planner analyzes query intent and selects which agents run.

### Agent Chain

```
User query
  -> Query Analyzer      detect intents (precedent, commentary_assessment, marks, etc.)
  -> DAP Compiler        build execution DAG from affordance catalog
  -> Retriever (flash)   vector search + manifest load
  -> JoinAnalysis (pro)  justice-to-section vote mapping
  -> HoldingCandidate (pro)  candidate holdings with width classification
  -> FractureClassifier (pro)  typed cross-opinion divergences
  -> MarksEvaluator (pro)     narrowest-ground analysis (when fractured)
  -> ClaimAssessor (pro)      structured claim extraction + classification
  -> ImpactAnalyst (pro)      downstream impact of misapplied claims
  -> Synthesis (pro)          grounded multi-section report
```

Not all agents run on every query. The planner selects based on intent:

| Intent | Agents Selected |
|--------|----------------|
| `precedent` | retrieval -> vote_structure -> holdings -> fractures -> synthesis |
| `precedent + marks` | + marks_evaluator |
| `commentary_assessment` | retrieval -> claim_assessment -> impact_analysis -> synthesis |
| `precedent + commentary_assessment` | all 8 agents |
| `factual_summary` | retrieval -> synthesis |

### 7 Global Invariants

Every agent enforces:

1. **Grounding** -- every claim cites block_id + page range
2. **Holding discipline** -- holding vs reasoning vs dicta
3. **No narrative collapse** -- individual justice attribution
4. **Minimality bias** -- narrowest reading preferred
5. **Doctrine precision** -- exact doctrinal labels
6. **No motive inference** -- text only, no speculation
7. **Marks skepticism** -- flag uncertainty in narrowest-ground analysis

### Claim Assessment

When external commentary is in scope, the **ClaimAssessor** extracts each distinct claim and classifies it:

| Status | Meaning |
|--------|---------|
| SUPPORTED | Claim accurately reflects the primary corpus |
| CONTRADICTED | Claim is directly at odds with primary authority |
| MISAPPLICATION | Claim references real content but applies it incorrectly |
| OMISSION | Commentary omits material context that changes understanding |
| OUTSIDE_CORPUS | Policy/rhetoric that the legal record cannot confirm or deny |

The **ImpactAnalyst** then assesses downstream consequences for flagged claims (CONTRADICTED, MISAPPLICATION, OMISSION), producing causal mechanism descriptions, error mode labels, and affected institutional actors.

## DAP Trace (Debugging)

Inspect execution plans, agent timing, and plan correctness:

```bash
just dap-list                                    # list sessions with plan summaries
just dap-plan SESSION_ID                         # show compiled plan
just dap-timeline SESSION_ID                     # agent timing waterfall
just dap-validate SESSION_ID                     # check plan vs actual execution
just dap-compare SESSION_A SESSION_B             # side-by-side plan comparison
just dap-compile "Assess McConnell's claims..."  # dry-run: show plan without running
just dap-features "What is the binding rule..."  # dry-run: show detected intents
```

## Ingestion

```bash
just decision-pipeline     # extract Learning Resources PDF + build index
just section122-pipeline   # extract Section 122 docs + build index
just nr-ingest             # convert NR JSON -> blocks -> rebuild index
just decision-ingest       # rebuild index only (after manual block edits)
just decision-clean        # delete vector index
```

### Adding National Review Articles

1. Place structured JSON in `docs/sources/national_review/YYYY-MM-DD/<slug>.json`
2. Run `just nr-ingest` to convert to blocks and rebuild the index
3. Use `just nr-dry-run` to validate JSON without writing blocks

## Project Structure

```
decision_rag_adk/           # Google ADK agent package
  __init__.py               # root_agent (DAPAgent with planner)
  agents/                   # 8 LlmAgents (one per pipeline stage)
  prompts/                  # invariants.py + 8 agent instructions
  tools/                    # retrieval.py (RAG query), corpus.py (filesystem)
  planner/                  # DAP: query analyzer, compiler, executor
    query_analyzer.py       # intent detection (heuristic rules)
    compiler.py             # affordance -> DAG compilation
    executor.py             # DAPAgent that runs compiled plans
    heuristic.py            # rule-based planner
    llm_planner.py          # LLM-based planner (Gemini)

config/
  affordances.yaml          # agent catalog: triggers, requires, inputs, outputs, cost

tools/bin/
  decision-rag              # RAG retriever CLI
  decision-adk              # ADK pipeline launcher
  extract-decision          # PDF -> blocks (Learning Resources)
  extract-section122        # HTML -> blocks (Section 122)
  nr-ingest                 # NR JSON -> blocks
  dap-trace                 # execution trace analyzer
  adk-sessions              # session history viewer

docs/decision/              # corpus (blocks, extracted text, manifests)
.rag_index_decision/        # persisted vector index
```

## Configuration

| File | Purpose |
|------|---------|
| `decision_rag_adk/.env` | `GOOGLE_API_KEY` (not committed) |
| `config/affordances.yaml` | Agent catalog for the DAP planner |
| `Justfile` | All task runner commands |

Environment variables:

| Variable | Default | Effect |
|----------|---------|--------|
| `DAP_PLANNER` | `heuristic` | Set to `llm` for LLM-based query planning |
| `DAP_PLANNER_MODEL` | (auto) | Override Gemini model for LLM planner |
| `GOOGLE_API_KEY` | (required) | Gemini API key |
