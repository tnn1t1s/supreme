import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DECISION_DIR = PROJECT_ROOT / "docs" / "decision"


def _parse_frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not match:
        return {}, text
    yaml_block = match.group(1)
    body = match.group(2).strip()
    metadata = {}
    for line in yaml_block.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            metadata[key.strip()] = val.strip().strip('"').strip("'")
    return metadata, body


def load_manifest() -> dict:
    """Load the decision corpus manifest with all opinion and block metadata.

    Returns:
        The manifest JSON with case name, docket numbers, decided date,
        opinions list (justice, type, block_count, page_range),
        and blocks list (block_id, justice, opinion_type, title, pages, doctrines).
    """
    manifests = list(DECISION_DIR.glob("*/manifest.json"))
    if not manifests:
        return {"error": "No manifest found in docs/decision/"}
    return json.loads(manifests[0].read_text())


def read_block(block_id: str) -> dict:
    """Read a specific block by its block_id. Returns metadata and full text.

    Args:
        block_id: The unique block identifier (e.g., "24-1287_roberts_majority_0005").

    Returns:
        Dict with block_id, metadata (justice, opinion_type, title, pages, doctrines),
        and full text content.
    """
    for manifest_path in DECISION_DIR.glob("*/manifest.json"):
        manifest = json.loads(manifest_path.read_text())
        for block in manifest.get("blocks", []):
            if block["block_id"] == block_id:
                block_file = manifest_path.parent / block["file"]
                if block_file.exists():
                    text = block_file.read_text()
                    metadata, body = _parse_frontmatter(text)
                    return {
                        "block_id": block_id,
                        "metadata": metadata,
                        "text": body,
                    }
                return {"error": f"Block file not found: {block['file']}"}
    return {"error": f"Block {block_id} not found in any manifest"}


def list_blocks(justice: str = "", opinion_type: str = "") -> list:
    """List available blocks with metadata. Optionally filter by justice and/or opinion type.

    Args:
        justice: Filter by justice name (case-insensitive, e.g., "Roberts").
        opinion_type: Filter by opinion type (e.g., "majority", "dissent").

    Returns:
        List of block metadata dicts (block_id, justice, opinion_type, title,
        page_start, page_end, word_count, doctrines).
    """
    results = []
    for manifest_path in DECISION_DIR.glob("*/manifest.json"):
        manifest = json.loads(manifest_path.read_text())
        for block in manifest.get("blocks", []):
            if justice and block.get("justice", "").lower() != justice.lower():
                continue
            if opinion_type and block.get("opinion_type", "").lower() != opinion_type.lower():
                continue
            results.append(block)
    return results
