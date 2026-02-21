# Installation

## Requirements

- Python 3.14+
- [just](https://github.com/casey/just) task runner
- A [Google AI Studio API key](https://aistudio.google.com/apikey)

## Setup

### 1. Clone

```bash
git clone https://github.com/tnn1t1s/supreme.git
cd supreme
```

### 2. Create virtual environment

```bash
python3.14 -m venv .venv
```

### 3. Install dependencies

```bash
.venv/bin/pip install llama-index llama-index-embeddings-huggingface pdfplumber google-adk
```

### 4. Configure API key

```bash
echo "GOOGLE_API_KEY=your-key-here" > decision_rag_adk/.env
```

### 5. Build the vector index

If you have the slip opinion PDF in `docs/decision/.../source/`:

```bash
just decision-pipeline
```

If blocks are already extracted (they ship with the repo):

```bash
just decision-ingest
```

### 6. Verify

```bash
just decision-list
```

Should output the case metadata with 53 blocks across 8 opinions.

## Running the Analysis Pipeline

### Interactive CLI

```bash
just decision-adk
```

### Web UI

```bash
just decision-adk-web
```

Opens at http://127.0.0.1:8000. Select `decision_rag_adk` from the dropdown.

### Raw retrieval (no agents)

```bash
just decision-query "taxing power"
just decision-justice "IEEPA" Roberts
just decision-doctrine "delegation" nondelegation
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'google'`

google-adk not installed in venv. Run:

```bash
.venv/bin/pip install google-adk
```

### `No index found. Building...`

Vector index doesn't exist yet. Run:

```bash
just decision-ingest
```

### ADK web shows no agents in dropdown

You ran `adk web decision_rag_adk` instead of `adk web .` — the web server must point at the project root for app discovery. Use `just decision-adk-web` or `tools/bin/decision-adk web`.

### `LLM is explicitly disabled. Using MockLLM.`

This is a harmless stderr message from LlamaIndex during retrieval. The retrieval tool filters it out automatically.
