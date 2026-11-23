"""Extract multiple direct-ref records from the same pinned Lean .olean.

A narrow inspection of stored expressions, not a kernel theorem check.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from riemann_evidence.proof_dependency import inspect_value_paths, normalize_records


EXTRACTOR = Path(__file__).with_name("ProofRefs.lean")


def _strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def extract(lean: Path, module: Path, targets: list[str], expected_sha: str | None = None):
    if not lean.is_file() or not module.is_file() or not EXTRACTOR.is_file():
        raise ValueError("Lean, .olean or extractor missing")
    digest = hashlib.sha256(module.read_bytes()).hexdigest()
    if expected_sha is not None and digest != expected_sha:
        raise ValueError("module hash differs from pin")
    version = subprocess.check_output([str(lean), "--version"], text=True, timeout=60).strip()
    if not re.match(r"Lean \(version 4\.33\.1,", version):
        raise ValueError(f"wrong Lean toolchain: {version}")
    records = []
    for target in targets:
        raw = subprocess.check_output(
            [str(lean), "--run", str(EXTRACTOR), str(module), target],
            text=True, timeout=90,
        )
        records.append(json.loads(raw, object_pairs_hook=_strict_object))
    normalize_records(records)
    return {
        "schema": "riemann-evidence-stored-proof-path-replay-v1",
        "module_sha256": digest,
        "extractor_sha256": hashlib.sha256(EXTRACTOR.read_bytes()).hexdigest(),
        "lean_version": version,
        "records": records,
        "analyses": {t: inspect_value_paths(records, t) for t in targets},
        "kernel_replay": "NOT_RUN",
        "external_import_closure": "NOT_RUN",
        "claim_authority": "NONE",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--module", type=Path, required=True)
    parser.add_argument("--target", action="append", required=True)
    parser.add_argument("--expected-sha256", default=None)
    args = parser.parse_args()
    if args.expected_sha256 is not None and not re.fullmatch(r"[a-f0-9]{64}", args.expected_sha256):
        parser.error("expected SHA-256 must be 64 lowercase hex characters")
    result = extract(args.lean, args.module, args.target, args.expected_sha256)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
