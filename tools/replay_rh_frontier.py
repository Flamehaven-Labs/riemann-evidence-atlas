"""Classify open RH proof-value references using bounded local evidence."""

import argparse
import gzip
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
from tempfile import TemporaryDirectory

from replay_rh_module_set import ARCHIVE_SHA256


RECEIPT_SHA256 = "de121ac9ac426cc666410147abe107ab41e2d06effc01e4e2c480e88a1a1e582"
GRAPH_SHA256 = "82c88d25d909a1399c754b87ce298e1939ab0908aeb4766fdac8a57387c71dc5"
EXTRACTOR = Path(__file__).with_name("ProofFrontier.lean").resolve()


def checked_bytes(path, expected):
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != expected:
        raise ValueError(f"SHA-256 differs from pin: {path.name}")
    return raw


def graph_candidates(path, names):
    """Read publisher classifications for exact names, without treating them as Lean kinds."""
    candidates = {}
    # The publisher's pinned file places each declaration on one JSON line.
    name_field = re.compile(r'"name":\s*("(?:[^"\\]|\\.)*")')
    with gzip.open(path, "rt", encoding="utf-8") as lines:
        for line in lines:
            if not line.lstrip().startswith('{"id":'):
                continue
            matched = name_field.search(line)
            if matched is None:
                raise ValueError("published declaration row without a name")
            name = json.loads(matched[1])
            if name in names:
                row = json.loads(line.strip().rstrip(","))
                if name in candidates:
                    raise ValueError(f"duplicate published declaration name: {name}")
                source = row["file"]
                module = source.removesuffix(".lean").replace("/", ".") if source else None
                candidates[name] = {
                    "module": module,
                    "kind": row["kind"],
                    "evidence": "PUBLISHED_GRAPH_CATALOG",
                    "has_value": None,
                    "value_refs": None,
                }
    return candidates


def classify(sources, observed, candidates):
    if len({row["name"] for row in observed}) != len(observed):
        raise ValueError("ambiguous compiled declaration ownership")
    by_name = {row["name"]: row for row in observed}
    if set(by_name) - sources.keys():
        raise ValueError("compiled extractor returned unrequested names")

    rows = []
    for name, users in sorted(sources.items()):
        entry = by_name.get(name) or candidates.get(name)
        if entry is None:
            entry = {"module": None, "kind": None, "evidence": "UNCONFIRMED",
                     "has_value": None, "value_refs": None}
        if name in by_name:
            axiom = "AXIOM_DECLARATION" if entry["kind"] == "axiom" else "OTHER_DECLARATION_KIND"
        else:
            axiom = "UNCONFIRMED"
        rows.append({**entry, "name": name, "referrers": sorted(users), "axiom_status": axiom})
    return rows


def replay(lean, frontier, archive, branches, graph):
    seed = json.loads(checked_bytes(frontier, RECEIPT_SHA256))
    checked_bytes(archive, ARCHIVE_SHA256)
    checked_bytes(graph, GRAPH_SHA256)
    version = subprocess.check_output([str(lean.resolve()), "--version"], text=True).strip()
    if not version.startswith("Lean (version 4.33.1,"):
        raise ValueError(f"expected Lean 4.33.1: {version}")
    sources = {}
    for edge in seed["analysis"]["unresolved_edges"]:
        if edge["kind"] == "value":
            sources.setdefault(edge["to"], set()).add(edge["from"])
    if sorted(sources) != seed["analysis"]["external_or_unresolved_references"]:
        raise ValueError("inconsistent seed VALUE frontier")

    with TemporaryDirectory(prefix="riemann-frontier-") as temp:
        root = Path(temp)
        artifacts = []
        with tarfile.open(archive, "r:gz") as tar:
            for module, binding in seed["module_inputs"].items():
                member = binding["archive_member"]
                if "archive" in binding:
                    path = branches / Path(member).name
                    checked_bytes(path, binding["sha256"])
                else:
                    info = tar.getmember(member)
                    if not info.isfile():
                        raise ValueError(f"expected regular .olean file: {member}")
                    path = root / Path(member).name
                    with tar.extractfile(info) as source:
                        module_bytes = source.read()
                    if sha256(module_bytes).hexdigest() != binding["sha256"]:
                        raise ValueError(f"compiled module bytes differ from pin: {module}")
                    path.write_bytes(module_bytes)
                artifacts.append([module, str(path.resolve())])
        query = root / "query.json"
        query.write_text(json.dumps([sorted(sources), artifacts]), encoding="utf-8")
        raw = subprocess.check_output(
            [str(lean.resolve()), "-j", "2", "--run", str(EXTRACTOR), str(query)],
            text=True, encoding="utf-8", timeout=120,
        )
        observed = json.loads(raw)

    remaining = sources.keys() - {row["name"] for row in observed}
    rows = classify(sources, observed, graph_candidates(graph, remaining))
    expanded = [row["name"] for row in rows
                if row["evidence"] == "PINNED_RH_OLEAN" and row["has_value"]]
    return {
        "schema": "riemann-evidence-value-frontier-v1",
        "seed_receipt_sha256": RECEIPT_SHA256,
        "catalog_sha256": GRAPH_SHA256,
        "extractor_sha256": sha256(EXTRACTOR.read_bytes()).hexdigest(),
        "lean_version": version,
        "toolchain_imports": ["Init"],
        "distinct_original_value_references": len(rows),
        "evidence_counts": {tag: sum(row["evidence"] == tag for row in rows)
                            for tag in sorted({row["evidence"] for row in rows})},
        "opened_pinned_rh_values": expanded,
        "frontier": rows,
        "transitive_closure": "NOT_RUN",
        "original_proof_kernel_replay": "NOT_RUN",
        "claim_authority": "NONE",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("lean", "frontier", "archive", "branch-dir", "graph"):
        parser.add_argument(f"--{arg}", type=Path, required=True)
    args = parser.parse_args()
    report = replay(args.lean, args.frontier, args.archive, args.branch_dir, args.graph)
    sys.stdout.buffer.write((json.dumps(report, indent=2, sort_keys=True) + "\n").encode())


if __name__ == "__main__":
    main()
