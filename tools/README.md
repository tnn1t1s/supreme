# tools/

CLI tools for corpus ingestion, retrieval, and analysis.

## tools/bin/

| Tool | Purpose |
|------|---------|
| `decision-rag` | LlamaIndex vector search over decision blocks with metadata filtering (-j, -t, -d, -c, --doc-type) |
| `decision-adk` | Launcher for the 6-agent ADK analysis pipeline (CLI and web UI) |
| `extract-decision` | Converts slip opinion PDF into segmented markdown blocks with doctrine tagging |
| `extract-section122` | Converts Section 122 source HTML into segmented markdown blocks with extended frontmatter |
| `adk-sessions` | Retrieves prompt/response pairs from ADK session history database |
| `podcast-rag` | Podcast transcript RAG (legacy, unrelated to decision analysis) |
