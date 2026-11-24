"""Compile the second Landau case and bind the real proof to its numerical report."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

from verify_baseline import RECEIPTS, require_sha256
from verify_landau_tail import (
    ENDPOINTS, LEAN_COMMIT, LOCK, PROOFS, RATIONAL, RATIONAL_THEOREMS, ROOT,
    ImportUnavailable, ReceiptMismatch, compile_proof, mathlib_environment,
    require_receipt_match, run,
)

CASE = "E2ALandauSecondCase"
NUMERICAL_REPORT = "docs/landau-second-case.json"
THEOREMS = {"tail_mass_eq", "exp_one_enclosed", "tail_mass_enclosed", "tail_mass_caps"}


def check_numerical_input() -> str:
    path = ROOT / NUMERICAL_REPORT
    digest = RECEIPTS[NUMERICAL_REPORT]
    require_sha256(path, digest)
    report = json.loads(path.read_bytes())
    refined = report["cases"]["refined_cap"]
    exhausted = report["cases"]["precision_exhausted"]
    details = refined["report"]["details"]
    if (refined["input"] != {
            "component": "outside_window", "k": 1, "rate": "2", "a": "1/2", "b": "2",
            "cap": details["cap"], "precision_bits": 256,
        } or exhausted["input"] != {**refined["input"], "precision_bits": 128}):
        raise ValueError("unexpected Landau specialization or changed cap")
    source = (PROOFS / f"{CASE}.lean").read_text(encoding="utf-8")
    for name, field in (("lower256", "lower"), ("upper256", "upper"), ("nearCap", "cap")):
        literal = re.search(rf"^def {name} : Rat :=\s+([0-9]+) / ([1-9][0-9]*)$", source, re.M)
        if literal is None or Fraction(*map(int, literal.groups())) != Fraction(details[field]):
            raise ValueError(f"Lean {name} differs from the frozen numerical report")
    return digest


def verify(lean: Path, project: Path) -> dict:
    numerical_sha = check_numerical_input()
    if not lean.is_file():
        raise FileNotFoundError(lean)
    version = run([str(lean), "--version"], ROOT)
    if not version.startswith("Lean (version 4.33.1,") or f"commit {LEAN_COMMIT}," not in version:
        raise ValueError(f"expected pinned Lean 4.33.1: {version}")
    mathlib_env, mathlib_commit = mathlib_environment(project, lean)
    with TemporaryDirectory(prefix="landau-second-case-") as directory:
        work = Path(directory)
        local_env = {**os.environ, "LEAN_PATH": str(work)}
        endpoints = compile_proof(
            lean, work, ENDPOINTS, {"propagated_lower_matches", "propagated_upper_matches"},
            local_env, namespace=ENDPOINTS,
        )
        rational = compile_proof(lean, work, RATIONAL, RATIONAL_THEOREMS, local_env)
        mathlib_env["LEAN_PATH"] = str(work) + os.pathsep + mathlib_env["LEAN_PATH"]
        real = compile_proof(lean, work, CASE, THEOREMS, mathlib_env, namespace=CASE)
    return {
        "schema": "riemann-evidence-landau-second-case-lean-v1",
        "lean_version": version,
        "mathlib_commit": mathlib_commit,
        "dependency_lock_sha256": sha256(LOCK.read_bytes()).hexdigest(),
        "numerical_report_sha256": numerical_sha,
        "imports": {ENDPOINTS: endpoints["sha256"], RATIONAL: rational["sha256"]},
        "real": {"status": "PASS", **real},
        "claim_authority": "NONE",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--mathlib-project", type=Path, required=True)
    parser.add_argument("--expect", type=Path, help="compare proof evidence with a saved receipt")
    args = parser.parse_args()
    try:
        report = verify(args.lean.resolve(), args.mathlib_project.resolve())
        if args.expect is not None:
            require_receipt_match(report, json.loads(args.expect.read_bytes()))
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
        print(f"LANDAU_SECOND_CASE_LEAN_FAILED: {error}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write((json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
