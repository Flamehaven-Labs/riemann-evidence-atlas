"""Replay the weighted mode-coalescence proof in the pinned Lean environment."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from verify_landau_tail import (
    ImportUnavailable, LEAN_COMMIT, LOCK, PROOFS, ROOT, ReceiptMismatch,
    mathlib_environment, require_receipt_match, run,
)
from verify_model_proofs import compile_with_axioms

STRIP = PROOFS / "E2APositiveStripGram.lean"
CONFLUENCE = PROOFS / "E2AModeConfluence.lean"


def verify(lean: Path, project: Path) -> dict:
    if not lean.is_file():
        raise FileNotFoundError(lean)
    version = run([str(lean), "--version"], ROOT)
    if not version.startswith("Lean (version 4.33.1,") or f"commit {LEAN_COMMIT}," not in version:
        raise ValueError(f"unexpected Lean toolchain: {version}")
    env, commit = mathlib_environment(project, lean)
    with TemporaryDirectory(prefix="atlas-mode-confluence-") as tmp:
        work = Path(tmp)
        strip = work / STRIP.name
        proof = work / CONFLUENCE.name
        strip.write_bytes(STRIP.read_bytes())
        proof.write_bytes(CONFLUENCE.read_bytes())
        run([str(lean), "-j", "2", "-o", str(strip.with_suffix(".olean")), strip.name], work, env)
        env["LEAN_PATH"] = str(work) + os.pathsep + env["LEAN_PATH"]
        axioms = compile_with_axioms(lean, proof, env, root=work)
        expected = {
            f"E2AModeConfluence.{name}" for name in (
                "divided_mode_pointwise", "mode_jet_squared_norm", "divided_mode_weighted_l2",
                "gram_mode_weighted_l2", "divided_block", "divided_block_entry_limit",
                "limiting_block_nilpotent",
            )
        }
        if {line.split("'")[1] for line in axioms} != expected:
            raise ValueError("mode coalescence declaration inventory differs")
        return {
            "axioms": axioms,
            "base_proof_sha256": sha256(strip.read_bytes()).hexdigest(),
            "dependency_lock_sha256": sha256(LOCK.read_bytes()).hexdigest(),
            "lean_version": version,
            "mathlib_commit": commit,
            "source_sha256": sha256(proof.read_bytes()).hexdigest(),
            "status": "PASS",
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--mathlib-project", type=Path, required=True)
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    try:
        receipt = verify(args.lean.resolve(), args.mathlib_project.resolve())
        if args.expect is not None:
            require_receipt_match(receipt, json.loads(args.expect.read_bytes()))
    except (FileNotFoundError, ImportUnavailable) as error:
        print(f"ENV_BLOCKED: {error}", file=sys.stderr)
        return 2
    except ReceiptMismatch as error:
        print(f"RECEIPT_MISMATCH: {error}", file=sys.stderr)
        return 3
    except subprocess.TimeoutExpired as error:
        print(f"RUN_TIMEOUT: {error}", file=sys.stderr)
        return 4
    except (ValueError, subprocess.SubprocessError) as error:
        print(f"MODE_CONFLUENCE_REPLAY_FAILED: {error}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write((json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
