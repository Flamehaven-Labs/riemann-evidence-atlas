"""Recompile the research models and compare their Windows and Colab evidence."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys

from verify_landau_second_case_lean import CASE, verify as verify_second_landau
from verify_landau_tail import (
    ALLOWED_AXIOMS, ImportUnavailable, LEAN_COMMIT, LOCK, PROOFS, REAL, ROOT,
    ReceiptMismatch, mathlib_environment, require_receipt_match, run,
)

REFLECTION = "E2ARhReflectionCos"
MODEL_PROOFS = {
    "biorthogonal-gap": "E2ABiorthogonalGap",
    "two-zero-block": "E2ATwoZeroBlock",
    "positive-strip-gram": "E2APositiveStripGram",
}


def mathlib_imports() -> list[str]:
    return sorted({
        module
        for name in (REAL, CASE, REFLECTION, *MODEL_PROOFS.values())
        for module in re.findall(
            r"^import (Mathlib\.\S+)$", (PROOFS / f"{name}.lean").read_text(encoding="utf-8"), re.M
        )
    })


def read_receipt(relative: str) -> dict:
    return json.loads((ROOT / "docs" / relative).read_bytes())


def save_receipt(output: Path, name: str, receipt: dict) -> None:
    (output / f"{name}.json").write_bytes(
        (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )


def compile_with_axioms(lean: Path, source: Path, env: dict[str, str]) -> list[str]:
    output = run([str(lean), f"--root={ROOT}", "-j", "2", str(source)], ROOT, env)
    lines = output.splitlines()
    names = set()
    for line in lines:
        match = re.fullmatch(r"'([^']+)' depends on axioms: \[(.*)\]", line)
        if match is None or match[1] in names or not set(match[2].split(", ")) <= ALLOWED_AXIOMS:
            raise ValueError(f"invalid Lean axiom report for {source.name}: {line}")
        names.add(match[1])
    if not names:
        raise ValueError(f"missing Lean axiom report: {source.name}")
    return lines


def verify(lean: Path, project: Path, output: Path) -> None:
    if not lean.is_file():
        raise FileNotFoundError(lean)
    version = run([str(lean), "--version"], ROOT)
    if not version.startswith("Lean (version 4.33.1,") or f"commit {LEAN_COMMIT}," not in version:
        raise ValueError(f"unexpected Lean toolchain: {version}")
    env, commit = mathlib_environment(project, lean)
    shared = {
        "lean_version": version, "mathlib_commit": commit,
        "dependency_lock_sha256": sha256(LOCK.read_bytes()).hexdigest(), "status": "PASS",
    }
    output.mkdir(parents=True, exist_ok=True)
    second_landau = verify_second_landau(lean, project)
    for host in ("lean", "colab"):
        require_receipt_match(second_landau, read_receipt(f"landau-second-case-{host}-replay.json"))
    save_receipt(output, "landau-second-case", second_landau)
    print("landau-second-case: Windows and Colab evidence matched", flush=True)
    for name, module in (("rh-reflection-cos", REFLECTION), *MODEL_PROOFS.items()):
        source = PROOFS / f"{module}.lean"
        axioms = compile_with_axioms(lean, source, env)
        receipt = {
            **shared, "source_sha256": sha256(source.read_bytes()).hexdigest(), "axioms": axioms,
            "axioms_log_sha256": sha256(("\n".join(axioms) + "\n").encode("utf-8")).hexdigest(),
        }
        if module == REFLECTION:
            if (
                receipt["source_sha256"] != "91d6fe07fa612ba6079d653d8928bbb2a3f2bef98f9377ee694a9f488c555006"
                or receipt["axioms_log_sha256"] != "a062993d32ef6d25882cb836896d7fb7a90b9a7a90105f23d669fe69407779ad"
            ):
                raise ReceiptMismatch("RH reflection proof or axiom output differs from the Colab phase replay")
        else:
            for host in ("windows", "colab"):
                require_receipt_match(receipt, read_receipt(f"masullo/{name}-{host}-replay.json"))
        save_receipt(output, name, receipt)
        print(f"{name}: {len(axioms)} declarations matched", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mathlib-imports", action="store_true")
    parser.add_argument("--lean", type=Path)
    parser.add_argument("--mathlib-project", type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if args.mathlib_imports:
        print("\n".join(mathlib_imports()))
        return 0
    if None in (args.lean, args.mathlib_project, args.output_dir):
        parser.error("--lean, --mathlib-project and --output-dir are required for replay")
    try:
        verify(args.lean.resolve(), args.mathlib_project.resolve(), args.output_dir.resolve())
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
        print(f"FORMAL_MODEL_REPLAY_FAILED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
