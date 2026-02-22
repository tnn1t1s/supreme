# CLAUDE.md - supremes-tariif

## Project

Institutional analysis toolkit for Supreme Court decisions. Multi-corpus RAG with cross-document analysis.

Cases:
- *Learning Resources, Inc. v. Trump* (24-1287, 25-250), decided 2026-02-20
- Section 122 Global Import Surcharge (19 U.S.C. § 2132), proclaimed 2026-02-20

## Stack

```yaml
Python: .venv/bin/python (3.14) | ALWAYS use venv
RAG: LlamaIndex + BAAI/bge-small-en-v1.5 embeddings
ADK: google-adk 1.25.1 | Gemini 2.5 flash + pro
Runner: just (Justfile)
```

## Key Paths

```yaml
Corpus 1: docs/decision/2026-02-20_learning-resources-v-trump_24-1287/
Corpus 2: docs/decision/2026-02-21_section-122-global-tariff/
Manifest: docs/decision/.../manifest.json
Blocks: docs/decision/.../blocks/{opinion|doc_type}/{NNNN}.md
Vector Index: .rag_index_decision/
ADK Package: decision_rag_adk/
ADK Prompts: decision_rag_adk/prompts/
ADK Tools: decision_rag_adk/tools/
CLI Tools: tools/bin/{decision-rag,decision-adk,extract-decision,extract-section122}
API Key: decision_rag_adk/.env (GOOGLE_API_KEY)
```

## ADK Pipeline (decision_rag_adk)

```yaml
Architecture: SequentialAgent with 6 LlmAgent sub-agents
Entry: decision_rag_adk/__init__.py -> root_agent

Agents:
  1. retriever: gemini-2.5-flash | tools: query_decision_rag, load_manifest | output_key: retrieved_blocks
  2. join_analysis: gemini-2.5-pro | tools: read_block, list_blocks | output_key: join_structure
  3. holding_candidate: gemini-2.5-pro | tools: read_block | output_key: holding_candidates
  4. fracture_classifier: gemini-2.5-pro | tools: read_block, list_blocks | output_key: fractures
  5. marks_evaluator: gemini-2.5-pro | tools: read_block | output_key: marks_analysis
  6. synthesis: gemini-2.5-pro | no tools | renders final report from all state

Invariants (7): Grounding | Holding discipline | No narrative collapse | Minimality bias | Doctrine precision | No motive inference | Marks skepticism
Invariants injected: prompts/invariants.py prepended to every agent instruction

Tools:
  retrieval.py: Shells out to tools/bin/decision-rag query --json (uses venv python)
  corpus.py: Direct filesystem reads (manifest, blocks, list)
```

## Commands

```yaml
Analysis:
  just decision-adk           # Interactive CLI pipeline
  just decision-adk-web       # Web UI at http://127.0.0.1:8000
  tools/bin/decision-adk web  # Same as above

Retrieval:
  just decision-query "q"     # Search all opinions
  just decision-justice "q" J # Filter by justice
  just decision-doctrine "q" d # Filter by doctrine
  just decision-corpus "q" c  # Filter by corpus (e.g. section122_global_tariff)
  just decision-doctype "q" dt # Filter by doc type (statute|proclamation|fact_sheet)
  just decision-json "q"     # JSON output
  just decision-list          # List indexed decisions

Ingestion:
  just decision-pipeline      # Extract PDF + build index (Learning Resources)
  just section122-pipeline    # Extract Section 122 docs + build index
  just decision-ingest        # Rebuild index only
  just decision-clean         # Delete vector index
```

## Block Format

```yaml
Frontmatter: YAML between --- delimiters
Fields (decision): justice, opinion_type, title, case, docket, date, source, page_start, page_end, block_id, doctrines_primary, doctrines_secondary
Fields (section122): corpus, doc_type, title, date, source_name, source_url, actor, authority, action, scope, judicial_status, related_cases, block_id, doctrines_primary, doctrines_secondary
Doctrines: Comma-separated strings | "none" for empty
block_id format (decision): {docket}_{justice}_{opinion_type}_{NNNN}
block_id format (section122): {date}_{corpus}_{doc_type}_{NNNN}
```

## Prompt Tuning

```yaml
Location: decision_rag_adk/prompts/
Files: invariants.py (shared) + {retriever,join_analysis,holding,fracture,marks,synthesis}.py

Holding width: case_specific vs general_principle (prompts/holding.py)
Fracture fields: vote_split, majority_required, affects_outcome (prompts/fracture.py)
Synthesis voice: Clerical not interpretive | Subject = justices/opinions | No evaluative adverbs (prompts/synthesis.py)
```

## Rules

```yaml
- NEVER use system python | Always .venv/bin/python
- NEVER commit decision_rag_adk/.env (contains API key)
- Retrieval tool shells to decision-rag CLI with venv python (not shebang)
- ADK web must point at project root (.), not agent dir, for app discovery
- Prompt changes take effect on next query (no restart needed for adk web)
```
