"""Replay the Mellin translation model with its pinned Lean dependencies."""

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
from verify_mode_confluence import CONFLUENCE, STRIP
from verify_model_proofs import compile_with_axioms

PROOF = PROOFS / "E2AMellinTranslation.lean"
DECLARATIONS = {
    f"E2AMellinTranslation.{name}" for name in (
        "multiplier_hasDerivAt", "translate_mode", "translate_jet",
        "translate_divided_mode", "translate_divided_weighted_l2",
        "weight_translate_le", "translate_weighted_l2_le",
    )
}


def verify(lean: Path, project: Path) -> dict:
    if not lean.is_file():
        raise FileNotFoundError(lean)
    version = run([str(lean), "--version"], ROOT)
    if not version.startswith("Lean (version 4.33.1,") or f"commit {LEAN_COMMIT}," not in version:
        raise ValueError(f"unexpected Lean toolchain: {version}")
    env, commit = mathlib_environment(project, lean)
    with TemporaryDirectory(prefix="atlas-mellin-translation-") as tmp:
        work = Path(tmp)
        sources = (STRIP, CONFLUENCE, PROOF)
        inputs = {source.name: source.read_bytes() for source in sources}
        for name, data in inputs.items():
            (work / name).write_bytes(data)
        env["LEAN_PATH"] = str(work) + os.pathsep + env["LEAN_PATH"]
        for source in sources[:-1]:
            run([str(lean), "-j", "2", "-o", f"{source.stem}.olean", source.name], work, env)
        axioms = compile_with_axioms(lean, work / PROOF.name, env, root=work)
        if {line.split("'")[1] for line in axioms} != DECLARATIONS:
            raise ValueError("Mellin translation declaration inventory differs")
    return {
        "axioms": axioms,
        "dependency_lock_sha256": sha256(LOCK.read_bytes()).hexdigest(),
        "lean_version": version,
        "mathlib_commit": commit,
        "source_sha256": {name: sha256(data).hexdigest() for name, data in inputs.items()},
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
        print(f"MELLIN_TRANSLATION_REPLAY_FAILED: {error}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write((json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
