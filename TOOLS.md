# TOOLS.md — CLI Tool Reference

This project includes five CLI tools in `tools/bin/`. All are invoked through the project's `.venv` Python or directly via `just` recipes. None require installation beyond the project's virtual environment.

---

## extract-decision

**Path:** `tools/bin/extract-decision`
**Language:** Python 3 (requires `pdfplumber`)
**Purpose:** Converts a Supreme Court slip opinion PDF into structured, tagged markdown blocks suitable for RAG ingestion.

### What It Does

1. Reads the slip opinion PDF from `docs/decision/.../source/`.
2. Splits the document by justice and opinion type using hardcoded page ranges (8 opinions in this case).
3. Segments each opinion into semantically meaningful blocks (80–500 words) by detecting section headings (`I`, `II-A`, `III`, etc.) and paragraph boundaries.
4. Classifies each block's doctrinal content using regex pattern matching against 9 doctrine categories, scoring by match count with primary (3+ matches) and secondary (1+ matches) thresholds.
5. Writes each block as a markdown file with YAML frontmatter containing structured metadata: justice, opinion type, page range, block ID, and doctrine tags.
6. Generates `manifest.json` — a complete index of all opinions and blocks with their metadata.

### Output Structure

```
docs/decision/2026-02-20_learning-resources-v-trump_24-1287/
├── source/24-1287_slip_opinion.pdf     # Input PDF
├── extracted/{justice}_{type}.md        # Full opinion text (1 file per opinion)
├── blocks/{justice}_{type}/{NNNN}.md    # Individual blocks with frontmatter
└── manifest.json                        # Complete corpus index
```

### Block Frontmatter Fields

| Field | Description | Example |
|-------|-------------|---------|
| `justice` | Authoring justice | `Roberts` |
| `opinion_type` | Category | `majority`, `concurrence`, `dissent`, `concurrence_in_part`, `syllabus` |
| `title` | Section heading detected during segmentation | `II-A` |
| `block_id` | Unique identifier: `{docket}_{justice}_{type}_{NNNN}` | `24-1287_roberts_majority_0005` |
| `page_start`, `page_end` | PDF page range | `7`, `12` |
| `doctrines_primary` | Comma-separated primary doctrine tags (3+ regex matches) | `statutory_interpretation,emergency_powers` |
| `doctrines_secondary` | Comma-separated secondary doctrine tags (1–2 matches) | `major_questions` |

### Doctrine Classification

Nine doctrine categories, each with 4–6 regex patterns:

| Doctrine | Sample patterns |
|----------|----------------|
| `major_questions` | `major questions`, `extraordinary.*delegat`, `clear congressional authorization` |
| `clear_statement` | `clear.statement rule`, `expressly (given\|conferred\|authorized)` |
| `nondelegation` | `nondelegation`, `intelligible principle`, `legislative power.*delegat` |
| `separation_of_powers` | `separation of powers`, `Vesting Clause`, `constitutional structure` |
| `taxing_power` | `taxing power`, `Taxes, Duties, Imposts`, `birth.right power` |
| `statutory_interpretation` | `ordinary meaning`, `plain (meaning\|text\|reading)`, `noscitur a sociis` |
| `foreign_affairs` | `foreign affairs`, `national security`, `Commander in Chief` |
| `emergency_powers` | `emergency power`, `national emergenc`, `Youngstown` |
| `congressional_delegation` | `Congress.*delegat`, `historical.*delegat`, `tariff.*delegat` |

A block receives a "primary" tag at 3+ matches and "secondary" at 1–2 matches. Maximum 3 primary and 2 secondary per block.

### Usage

```bash
just extract                   # or: .venv/bin/python tools/bin/extract-decision
just decision-pipeline         # extract + ingest in one step
```

### Design Decisions

- **Hardcoded opinion page ranges**: The slip opinion's structure doesn't have reliable machine-parseable markers for opinion boundaries. Page ranges are set manually per case in the `OPINIONS` list.
- **Regex-based doctrine classification**: Chosen over LLM classification for determinism and speed. The patterns are tuned for this specific decision's vocabulary but are generalizable.
- **Block size window (80–500 words)**: Below 80 words, blocks lack context for embedding. Above 500, they dilute retrieval precision. The segmenter splits at paragraph boundaries within this window.

---

## decision-rag

**Path:** `tools/bin/decision-rag`
**Language:** Python 3 (requires `llama-index`, `llama-index-embeddings-huggingface`)
**Purpose:** Vector search over the structured block corpus with metadata filtering by justice, opinion type, and doctrine.

### What It Does

1. **Ingest**: Reads all block markdown files, parses their YAML frontmatter into LlamaIndex `Document` metadata, and builds a `VectorStoreIndex` using `BAAI/bge-small-en-v1.5` embeddings. Persists to `.rag_index_decision/`.
2. **Query**: Loads the persisted index and retrieves blocks by semantic similarity, with optional metadata filters. Returns results with similarity scores, full metadata, and text previews.
3. **List**: Reads `manifest.json` and prints a summary of all indexed decisions, opinions, and block counts.

### Metadata Filters

Filters are passed to LlamaIndex's `MetadataFilters` and applied at retrieval time (not post-hoc). Multiple filters of the same type use OR logic; mixed filter types also use OR when combined.

| Flag | Filter | Example |
|------|--------|---------|
| `-j` / `--justice` | Justice name (repeatable) | `-j Roberts -j Gorsuch` |
| `-t` / `--type` | Opinion type (repeatable) | `-t dissent` |
| `-d` / `--doctrine` | Doctrine tag (repeatable) | `-d major_questions -d nondelegation` |
| `-k` / `--top-k` | Number of results (default 10) | `-k 20` |
| `--json` | JSON output | |

### Output Formats

**Human-readable** (default): Numbered nodes with score, metadata summary, and text preview (1500 chars max).

**JSON** (`--json`): Array of objects with `score`, `metadata` dict (all frontmatter fields), and `text` (2000 chars max).

### Usage

```bash
just decision-query "taxing power"              # All opinions
just decision-justice "IEEPA" Roberts            # Filter by justice
just decision-doctrine "delegation" nondelegation # Filter by doctrine
just decision-json "emergency powers"            # JSON output
just decision-list                               # List indexed decisions
just decision-ingest                             # Rebuild index
just decision-clean                              # Delete index
```

### Embedding Model

Uses `BAAI/bge-small-en-v1.5` — a 33M parameter model producing 384-dimensional embeddings. Chosen for:
- Fast local inference (no API key required)
- Strong performance on legal/technical text retrieval benchmarks
- Small enough to run on CPU without GPU

The index stores no LLM — retrieval is pure vector similarity. LLM-based analysis is handled by the ADK pipeline.

### Design Decisions

- **No LLM at retrieval time**: The retriever returns raw blocks with scores. All interpretation is deferred to the ADK agents. This makes retrieval deterministic and fast.
- **Frontmatter as metadata**: Every block's YAML frontmatter fields become LlamaIndex metadata fields, enabling structured filtering at retrieval time rather than post-hoc filtering.
- **Separate from ADK tools**: `decision-rag` is a standalone CLI. The ADK tool `query_decision_rag` shells out to it via subprocess, keeping the retrieval implementation independent of the agent framework.

---

## decision-adk

**Path:** `tools/bin/decision-adk`
**Language:** Bash (wraps `adk` CLI from `google-adk`)
**Purpose:** Launcher for the 6-agent ADK analysis pipeline. Thin shell wrapper that resolves paths and dispatches to `adk run` or `adk web`.

### What It Does

1. Resolves `PROJECT_ROOT`, `VENV_PYTHON`, and `ADK` binary paths.
2. Validates that `adk` is installed and the agent package exists.
3. Dispatches to either:
   - `adk run decision_rag_adk` — interactive CLI mode (stdin/stdout)
   - `adk web .` — web UI at `http://127.0.0.1:8000` (must point at project root for app discovery)

### Usage

```bash
just decision-adk              # Interactive CLI
just decision-adk-web          # Web UI at http://127.0.0.1:8000
tools/bin/decision-adk run     # Same as above (explicit)
tools/bin/decision-adk web     # Same as above (explicit)
tools/bin/decision-adk --help  # Print usage
```

### Important: Web Mode Path

`adk web` must receive the **project root** (`.`), not the agent directory, for ADK's app discovery to find `decision_rag_adk/__init__.py`. The `run` command receives the agent directory directly.

---

## adk-sessions

**Path:** `tools/bin/adk-sessions`
**Language:** Python 3 (stdlib only — `sqlite3`, `json`, `argparse`)
**Purpose:** Retrieve prompt/response pairs from the ADK session history database. Pairs each agent's system prompt (from `decision_rag_adk/prompts/`) with the actual response it produced during pipeline runs.

### What It Does

1. Reads the SQLite session database at `decision_rag_adk/.adk/session.db`, which is created and populated by Google ADK automatically when agents run.
2. Parses the `events` table, where each event is a JSON blob following ADK's Event model (`author`, `content.parts`, `function_call`, `function_response`).
3. Groups events into "turns" — each turn starts with a `user` event (the query) followed by agent events in pipeline order.
4. Pairs each agent's response with its system prompt from the `decision_rag_adk/prompts/` module.

### ADK Session Database Schema

ADK persists sessions in SQLite with four tables:

| Table | Purpose |
|-------|---------|
| `sessions` | Session metadata: `app_name`, `user_id`, `id`, `state`, timestamps |
| `events` | Chronological event log: `id`, `session_id`, `invocation_id`, `timestamp`, `event_data` (JSON) |
| `app_states` | Application-level state |
| `user_states` | User-level state |

The `event_data` JSON follows ADK's Event model:

```json
{
  "author": "retriever",
  "content": {
    "parts": [
      {"text": "..."},
      {"function_call": {"name": "load_manifest", "args": {}}},
      {"function_response": {"name": "load_manifest", "response": {...}}}
    ]
  },
  "invocation_id": "...",
  "id": "...",
  "timestamp": 1771690299.43
}
```

The `author` field identifies the source: `"user"` for user input, or the agent's name (e.g., `"retriever"`, `"synthesis"`) for agent output.

### Commands

**`list`** — List all sessions with event counts, query counts, agents involved, and first query preview.

```bash
just adk-list
```

Output:
```
  b8448ceb-7c25-4b20-b4ca-244e5a5aa428
    created=2026-02-21 11:11  user=user  events=60  queries=6
    agents: fracture_classifier, holding_candidate, join_analysis, marks_evaluator, retriever, synthesis
    q1: What is the narrowest controlling principle that explains the judgme...
```

**`show SESSION_ID`** — Display prompt/response pairs for each agent in a session. Supports prefix matching on session IDs (e.g., `b844` instead of the full UUID).

```bash
just adk-show b844                    # Full session
just adk-agent b844 synthesis         # Single agent
just adk-query b844 2                 # Specific query in multi-query session
just adk-show-prompts b844            # Include system prompts inline
just adk-export b844                  # Full JSON with tool call details
```

Flags:
| Flag | Effect |
|------|--------|
| `-a AGENT` | Filter to a single agent |
| `-q N` | Show only query N (1-indexed) |
| `--json` | JSON output with system prompts and response text |
| `--show-prompt` | Print each agent's system prompt before its response |
| `--include-tools` | Include full tool call/response payloads in JSON output |

**`agents`** — List all 6 agents with their prompt character and line counts.

```bash
just adk-agents
```

**`prompt AGENT`** — Print the full system prompt for a specific agent (invariants preamble + agent-specific instruction).

```bash
just adk-prompt retriever
```

### How Turns Are Grouped

Events in a session are ordered by timestamp. A new "turn" begins whenever a `user` event with text content appears. All subsequent agent events (tool calls, tool responses, text responses) are grouped under that turn until the next user event. This maps naturally to the SequentialAgent pipeline: each user query triggers a full 6-agent pass.

### Design Decisions

- **Raw SQLite, not ADK's `DatabaseSessionService`**: The installed ADK v1.25.1 uses a v1 schema (JSON-based), but the session DB was created with the v0 schema (epoch float timestamps). ADK's migration tool also fails on this data. Raw `sqlite3` reads work reliably.
- **Prompt pairing via imports**: Agent prompts are loaded from the `decision_rag_adk.prompts` Python module, the same source the agents use at runtime. This ensures the displayed prompt always matches what the agent actually received.
- **Session ID prefix matching**: Full UUIDs are unwieldy. The tool resolves short prefixes (e.g., `b844`) to full session IDs, erroring on ambiguous matches.

---

## podcast-rag

**Path:** `tools/bin/podcast-rag`
**Language:** Python 3 (requires `llama-index`, `llama-index-embeddings-huggingface`)
**Purpose:** RAG retriever for podcast transcript research. Separate from the decision analysis pipeline.

### What It Does

1. **Ingest**: Indexes all files in `data/` using LlamaIndex's `SimpleDirectoryReader` with the same `BAAI/bge-small-en-v1.5` embeddings. Persists to `.rag_index/`.
2. **Query**: Single-query retrieval against the transcript index.
3. **Research**: Multi-query expansion — generates 5 thematic queries from a topic (arguments/evidence, frameworks, risks/counterarguments, portfolio connections, historical trends) and deduplicates results.
4. **Program mode**: Appends instructions for feeding the retrieved evidence to an LLM to produce a 5-point evidence-based program with verbatim citations.

### Usage

```bash
just ingest                    # Index data/ directory
just query "macro themes"      # Single query
just research "rate policy"    # 5-dimension topic research
just program "portfolio hedging" # 5-point evidence-based program
```

### Design Decisions

- **Same embedding model as decision-rag**: Both use `BAAI/bge-small-en-v1.5` for consistency.
- **Multi-query deduplication**: The research mode tracks seen text prefixes (200 chars) to avoid showing the same chunk across multiple thematic queries.
- **No LLM synthesis**: Like `decision-rag`, this tool retrieves only. Synthesis is left to the consumer.

---

## Justfile Recipes

All tools are accessible via `just` recipes. The full recipe list:

### Decision RAG
| Recipe | Command |
|--------|---------|
| `just decision-query Q` | Query all opinions |
| `just decision-justice Q J` | Filter by justice |
| `just decision-doctrine Q D` | Filter by doctrine |
| `just decision-json Q` | JSON output |
| `just decision-list` | List indexed decisions |
| `just decision-ingest` | Rebuild index |
| `just decision-clean` | Delete index |
| `just decision-pipeline` | Extract PDF + rebuild index |

### Decision ADK
| Recipe | Command |
|--------|---------|
| `just decision-adk` | Interactive CLI pipeline |
| `just decision-adk-web` | Web UI |

### ADK Sessions
| Recipe | Command |
|--------|---------|
| `just adk-list` | List sessions |
| `just adk-show ID` | Show full session |
| `just adk-agent ID A` | Single agent pair |
| `just adk-query ID N` | Specific query |
| `just adk-show-prompts ID` | Include system prompts |
| `just adk-export ID` | JSON export with tools |
| `just adk-agents` | List agent prompts |
| `just adk-prompt A` | Print agent prompt |

### Podcast RAG
| Recipe | Command |
|--------|---------|
| `just ingest` | Index transcripts |
| `just query Q` | Single query |
| `just research T` | Multi-query research |
| `just program T` | 5-point program |

---

## Dependencies

| Tool | Python Packages | System |
|------|----------------|--------|
| `extract-decision` | `pdfplumber` | — |
| `decision-rag` | `llama-index`, `llama-index-embeddings-huggingface` | — |
| `decision-adk` | `google-adk` (v1.25.1) | `adk` CLI in venv |
| `adk-sessions` | (stdlib only) | — |
| `podcast-rag` | `llama-index`, `llama-index-embeddings-huggingface` | — |

All tools use the project venv at `.venv/bin/python`. Never use system Python.
