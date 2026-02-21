# Flirting with Models - Podcast RAG Research

venv := ".venv/bin/python"
rag := "tools/bin/podcast-rag"

# Index all transcripts in data/
ingest:
    {{venv}} {{rag}} ingest

# Single query against the index
query q:
    {{venv}} {{rag}} query "{{q}}"

# Single query, JSON output
query-json q:
    {{venv}} {{rag}} query "{{q}}" --json

# Multi-query research on a topic
research topic:
    {{venv}} {{rag}} research "{{topic}}"

# 5-point evidence-based program
program topic:
    {{venv}} {{rag}} research "{{topic}}" --program

# Research with custom top-k
research-deep topic k="10":
    {{venv}} {{rag}} research "{{topic}}" -k {{k}}

# Add a transcript to data/ and re-index
add file:
    cp "{{file}}" data/
    {{venv}} {{rag}} ingest

# Install dependencies
setup:
    python3 -m venv .venv
    .venv/bin/pip install llama-index llama-index-embeddings-huggingface

# Clean the index
clean:
    rm -rf .rag_index

# === Decision RAG ===
drag := "tools/bin/decision-rag"

# Extract opinions from slip opinion PDF into tagged blocks
extract:
    {{venv}} tools/bin/extract-decision

# Index decision blocks with metadata
decision-ingest:
    {{venv}} {{drag}} ingest

# Query decision (all opinions)
decision-query q:
    {{venv}} {{drag}} query "{{q}}"

# Query filtered by justice
decision-justice q j:
    {{venv}} {{drag}} query "{{q}}" -j {{j}}

# Query filtered by opinion type (majority|concurrence|dissent|etc)
decision-type q t:
    {{venv}} {{drag}} query "{{q}}" -t {{t}}

# Query filtered by doctrine tag
# Tags: major_questions|clear_statement|nondelegation|separation_of_powers|
#       taxing_power|statutory_interpretation|foreign_affairs|emergency_powers|
#       congressional_delegation
decision-doctrine q d:
    {{venv}} {{drag}} query "{{q}}" -d {{d}}

# Query with JSON output
decision-json q:
    {{venv}} {{drag}} query "{{q}}" --json

# List indexed decisions
decision-list:
    {{venv}} {{drag}} list

# Clean decision index
decision-clean:
    rm -rf .rag_index_decision

# Full pipeline: extract → ingest
decision-pipeline:
    {{venv}} tools/bin/extract-decision
    {{venv}} {{drag}} ingest

# Setup with pdfplumber
setup-decision:
    .venv/bin/pip install pdfplumber

# === Decision ADK (6-agent analysis pipeline) ===

# Interactive CLI analysis
decision-adk:
    tools/bin/decision-adk run

# Web UI analysis
decision-adk-web:
    tools/bin/decision-adk web
