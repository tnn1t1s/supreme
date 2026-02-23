import hashlib
import json
from pathlib import Path

import yaml


def load_affordance_catalog(catalog_path="config/affordances.yaml"):
    with open(catalog_path) as f:
        raw = yaml.safe_load(f)
    return raw["affordances"], raw.get("version", "unknown")


def load_corpus_manifest(docs_root="docs/decision"):
    root = Path(docs_root)
    manifests = {}
    for mf in sorted(root.glob("*/manifest.json")):
        with open(mf) as f:
            data = json.load(f)
        corpus_key = mf.parent.name
        manifests[corpus_key] = data
    return manifests


def _corpus_has_scotus(manifests):
    for _key, manifest in manifests.items():
        for block in manifest.get("blocks", []):
            if block.get("justice"):
                return True
        for op in manifest.get("opinions", []):
            if op.get("justice"):
                return True
    return False


def _build_output_map(catalog):
    out = {}
    for aff_id, aff in catalog.items():
        for key in aff.get("outputs", []):
            out[key] = aff_id
    return out


def compile_plan(query_features, manifests, catalog, catalog_version="unknown"):
    active_intents = [k for k, v in query_features["intents"].items() if v]
    output_map = _build_output_map(catalog)
    scotus_present = _corpus_has_scotus(manifests)

    # Step 1: candidate generation
    candidates = set()
    selection_reasons = {}
    for aff_id, aff in catalog.items():
        for trigger in aff.get("triggers_any", []):
            if trigger in active_intents:
                candidates.add(aff_id)
                selection_reasons[aff_id] = f"triggered by intent.{trigger}"
                break

    # Step 2: dependency closure
    changed = True
    while changed:
        changed = False
        for aff_id in list(candidates):
            for inp in catalog[aff_id].get("inputs", []):
                producer = output_map.get(inp)
                if producer and producer not in candidates:
                    candidates.add(producer)
                    selection_reasons[producer] = f"added as dependency: produces {inp} needed by {aff_id}"
                    changed = True

    # Step 3: precondition validation
    rejected = {}
    validated = set()
    produced_keys = set()
    for aff_id in candidates:
        for out in catalog[aff_id].get("outputs", []):
            produced_keys.add(out)

    for aff_id in list(candidates):
        reqs = catalog[aff_id].get("requires", [])
        ok = True
        for req in reqs:
            if req == "manifest.loaded":
                continue
            if req == "corpus.scotus_present" and not scotus_present:
                rejected[aff_id] = f"precondition failed: {req}"
                ok = False
                break
            if req.startswith("state.has("):
                key = req[len("state.has("):-1]
                if key not in produced_keys:
                    rejected[aff_id] = f"precondition failed: {req} — no producer in plan"
                    ok = False
                    break
        if ok:
            validated.add(aff_id)
        else:
            candidates.discard(aff_id)

    # Step 4: DAG construction
    # Terminal nodes must run after all non-terminal nodes
    terminal = {a for a in validated if catalog[a].get("phase") == "terminal"}
    non_terminal = validated - terminal
    nodes = sorted(validated)
    edges = []
    for aff_id in nodes:
        for inp in catalog[aff_id].get("inputs", []):
            producer = output_map.get(inp)
            if producer and producer in validated:
                edges.append({"from": producer, "to": aff_id, "key": inp})
    for t in terminal:
        for nt in non_terminal:
            if not any(e["from"] == nt and e["to"] == t for e in edges):
                edges.append({"from": nt, "to": t, "key": "_terminal_order"})

    execution_order = _topological_sort(nodes, edges)

    # Step 5: corpus scope
    override = query_features.get("corpus_scope_override")
    corpus_scope = override if override else _determine_corpus_scope(active_intents, manifests)

    catalog_hash = hashlib.sha256(
        json.dumps(catalog, sort_keys=True).encode()
    ).hexdigest()[:12]

    return {
        "dag": {"nodes": nodes, "edges": edges},
        "execution_order": execution_order,
        "selected_affordances": [
            {"id": a, "reason": selection_reasons.get(a, "dependency")}
            for a in execution_order
        ],
        "rejected_affordances": [
            {"id": a, "reason": r} for a, r in rejected.items()
        ],
        "query_features": query_features,
        "corpus_scope": corpus_scope,
        "catalog_version": catalog_hash,
    }


def _topological_sort(nodes, edges):
    adj = {n: [] for n in nodes}
    in_degree = {n: 0 for n in nodes}
    for e in edges:
        adj[e["from"]].append(e["to"])
        in_degree[e["to"]] += 1

    queue = sorted([n for n in nodes if in_degree[n] == 0])
    order = []
    while queue:
        n = queue.pop(0)
        order.append(n)
        for child in sorted(adj[n]):
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)
                queue.sort()

    if len(order) != len(nodes):
        remaining = set(nodes) - set(order)
        raise ValueError(f"Cycle detected in DAG: {remaining}")

    return order


def _determine_corpus_scope(active_intents, manifests):
    all_corpora = list(manifests.keys())
    if "commentary_assessment" in active_intents:
        return all_corpora
    return [c for c in all_corpora if "national_review" not in c.lower()]
