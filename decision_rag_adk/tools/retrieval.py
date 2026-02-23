import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DECISION_RAG_BIN = PROJECT_ROOT / "tools" / "bin" / "decision-rag"
VENV_PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"


def query_decision_rag(
    query: str,
    justice: str = "",
    opinion_type: str = "",
    doctrine: str = "",
    corpus: str = "",
    author: str = "",
    top_k: int = 10,
) -> dict:
    """Query the Supreme Court decision RAG index with optional metadata filters.

    Args:
        query: Search query text (e.g., "taxing power", "nondelegation").
        justice: Comma-separated justice names to filter by (e.g., "Roberts" or "Gorsuch,Barrett").
        opinion_type: Comma-separated opinion types to filter by (majority, concurrence, dissent, concurrence_in_part, syllabus).
        doctrine: Comma-separated doctrine tags to filter by (major_questions, nondelegation, taxing_power, etc.).
        corpus: Comma-separated corpus names to filter by (e.g., "national_review", "section122_global_tariff").
        author: Comma-separated author names to filter by (for national_review corpus).
        top_k: Number of top results to return (default 10).

    Returns:
        JSON array of matching blocks with scores, metadata, and text previews.
    """
    python = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable
    cmd = [
        python,
        str(DECISION_RAG_BIN),
        "query",
        query,
        "--json",
        "-k",
        str(top_k),
    ]
    if justice:
        for j in justice.split(","):
            j = j.strip()
            if j:
                cmd.extend(["-j", j])
    if opinion_type:
        for t in opinion_type.split(","):
            t = t.strip()
            if t:
                cmd.extend(["-t", t])
    if doctrine:
        for d in doctrine.split(","):
            d = d.strip()
            if d:
                cmd.extend(["-d", d])
    if corpus:
        for c in corpus.split(","):
            c = c.strip()
            if c:
                cmd.extend(["-c", c])
    if author:
        for a in author.split(","):
            a = a.strip()
            if a:
                cmd.extend(["-a", a])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        timeout=60,
    )
    if result.returncode != 0:
        return {"error": result.stderr.strip(), "command": " ".join(cmd)}
    stdout = result.stdout.strip()
    json_start = stdout.find("[")
    if json_start > 0:
        stdout = stdout[json_start:]
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON output", "raw": result.stdout[:2000]}
