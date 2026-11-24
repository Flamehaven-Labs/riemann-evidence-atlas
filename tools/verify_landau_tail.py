"""Check the Landau tail's rational arithmetic and optional Mathlib real proof."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
PROOFS = ROOT / "tests/lean"
LOCK = ROOT / "formal/landau/lake-manifest.json"
LEAN_COMMIT = "819816b2e0a3bf405af45ae5c7af2491d8f5bee6"
ENDPOINTS = "E2ATailEndpointAlgebra"
RATIONAL = "E2ALandauTailRational"
REAL = "E2ALandauTailReal"
RATIONAL_THEOREMS = {
    "small3_arithmetic", "small9_arithmetic", "small3_library_arithmetic",
    "small9_library_arithmetic", "reciprocal3_arithmetic", "reciprocal9_arithmetic",
    "exact_interval", "cap_comparisons",
}
REAL_THEOREMS = {
    "exp_neg_three_enclosed", "exp_neg_nine_enclosed",
    "tail_mass_eq", "tail_mass_enclosed", "tail_mass_caps",
}
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


class ImportUnavailable(OSError):
    """Lean could not load a compiled dependency."""


class ReceiptMismatch(ValueError):
    """Compilation succeeded but produced a different receipt."""


def run(command, cwd, env=None):
    result = subprocess.run(
        command, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", timeout=240,
    )
    if result.returncode != 0:
        diagnostic = result.stdout + result.stderr
        unreadable = re.search(
            r"error: (?:failed to read file|object file) '([^'\r\n]+\.olean(?:\.(?:private|server))?)'",
            diagnostic,
        )
        if unreadable:
            raise ImportUnavailable(f"Lean import unavailable: {unreadable[1]}")
    if result.returncode != 0 or result.stderr.strip():
        raise ValueError(f"{Path(command[0]).name} failed ({result.returncode})\n"
                         f"{result.stdout.strip()}\n{result.stderr.strip()}")
    return result.stdout.strip()


def mathlib_environment(project: Path, lean: Path) -> tuple[dict, str]:
    lock = json.loads(LOCK.read_bytes())
    if json.loads((project / LOCK.name).read_bytes()) != lock:
        raise ValueError("Mathlib project lock differs from the pinned manifest")
    expected = {package["name"]: package["rev"] for package in lock["packages"]}
    for name, commit in expected.items():
        package = project / ".lake/packages" / name
        if not package.is_dir():
            raise FileNotFoundError(package)
        if run(["git", "rev-parse", "HEAD"], package) != commit:
            raise ValueError(f"wrong pinned dependency: {name}")
        if run(["git", "status", "--porcelain", "--untracked-files=no"], package):
            raise ValueError(f"modified pinned dependency: {name}")
    modules = re.findall(r"^import (Mathlib\.\S+)$", (PROOFS / f"{REAL}.lean").read_text(encoding="utf-8"), re.M)
    built = project / ".lake/packages/mathlib/.lake/build/lib/lean"
    for module in modules:
        artifact = (built / module.replace(".", "/")).with_suffix(".olean")
        if not artifact.is_file():
            raise FileNotFoundError(artifact)
    lake = lean.with_name("lake" + lean.suffix)
    if not lake.is_file():
        raise FileNotFoundError(lake)
    env = {**os.environ, "PATH": str(lean.parent) + os.pathsep + os.environ.get("PATH", "")}
    env["LEAN_PATH"] = run(
        [str(lake), "env", sys.executable, "-E", "-S", "-c", "import os; print(os.environ['LEAN_PATH'])"],
        project, env,
    )
    return env, expected["mathlib"]


def compile_proof(
    lean: Path, work: Path, name: str, theorems: set[str], env: dict,
    namespace: str = "E2ALandauTail",
) -> dict:
    source = work / f"{name}.lean"
    shutil.copyfile(PROOFS / source.name, source)
    output = run([str(lean), "-j", "2", "-o", f"{name}.olean", source.name], work, env)
    axioms = {}
    for line in output.splitlines():
        match = re.fullmatch(rf"'{namespace}\.([a-z0-9_]+)' depends on axioms: \[(.*)\]", line)
        if match is None or match[1] in axioms:
            raise ValueError(f"unexpected Lean axiom report line: {line}")
        declared = set(match[2].split(", ")) if match[2] else set()
        if not declared <= ALLOWED_AXIOMS:
            raise ValueError(f"unexpected axioms for {match[1]}: {declared - ALLOWED_AXIOMS}")
        axioms[match[1]] = sorted(declared)
    if axioms.keys() != theorems:
        raise ValueError(f"incomplete Lean axiom report: {name}")
    return {"sha256": sha256(source.read_bytes()).hexdigest(), "axioms": axioms}


def verify(lean: Path, project: Path | None) -> dict:
    if not lean.is_file():
        raise FileNotFoundError(lean)
    version = run([str(lean), "--version"], ROOT)
    if not version.startswith("Lean (version 4.33.1,") or f"commit {LEAN_COMMIT}," not in version:
        raise ValueError(f"expected pinned Lean 4.33.1: {version}")
    mathlib = mathlib_environment(project, lean) if project is not None else None
    with TemporaryDirectory(prefix="landau-tail-") as directory:
        work = Path(directory)
        local_env = dict(os.environ)
        local_env["LEAN_PATH"] = str(work)
        endpoints = compile_proof(
            lean, work, ENDPOINTS, {"propagated_lower_matches", "propagated_upper_matches"},
            local_env, namespace=ENDPOINTS,
        )
        rational = compile_proof(lean, work, RATIONAL, RATIONAL_THEOREMS, local_env)
        real = {"status": "NOT_RUN"}
        if mathlib is not None:
            mathlib_env, commit = mathlib
            mathlib_env["LEAN_PATH"] = str(work) + os.pathsep + mathlib_env["LEAN_PATH"]
            real = {"status": "PASS", "mathlib_commit": commit,
                    "dependency_lock_sha256": sha256(LOCK.read_bytes()).hexdigest(),
                    **compile_proof(lean, work, REAL, REAL_THEOREMS, mathlib_env)}
    return {"schema": "riemann-evidence-landau-tail-v1", "lean_version": version,
            "endpoints": endpoints, "rational": {"status": "PASS", **rational}, "real": real,
            "original_rh_kernel_replay": "NOT_RUN", "claim_authority": "NONE"}


def require_receipt_match(actual: dict, expected: dict) -> None:
    """Compare the proof evidence while retaining both hosts' identities."""
    for receipt in (actual, expected):
        version = receipt.get("lean_version") if isinstance(receipt, dict) else None
        if (not isinstance(version, str) or not version.startswith("Lean (version 4.33.1,")
                or f"commit {LEAN_COMMIT}," not in version):
            raise ReceiptMismatch("receipt has a different Lean toolchain")
    actual_evidence = {key: value for key, value in actual.items() if key != "lean_version"}
    expected_evidence = {key: value for key, value in expected.items() if key != "lean_version"}
    if json.dumps(actual_evidence, sort_keys=True) != json.dumps(expected_evidence, sort_keys=True):
        raise ReceiptMismatch("proof evidence differs from the reference receipt")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--mathlib-project", type=Path)
    parser.add_argument("--expect", type=Path, help="compare with a receipt, excluding only the host banner")
    args = parser.parse_args()
    try:
        report = verify(args.lean.resolve(), args.mathlib_project.resolve() if args.mathlib_project else None)
    except (FileNotFoundError, ImportUnavailable) as error:
        print(f"ENV_BLOCKED: {error}", file=sys.stderr)
        return 2
    except subprocess.TimeoutExpired as error:
        print(f"RUN_TIMEOUT: {error}", file=sys.stderr)
        return 4
    except (ValueError, subprocess.SubprocessError) as error:
        print(f"LANDAU_TAIL_CHECK_FAILED: {error}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write((json.dumps(report, indent=2, sort_keys=True) + "\n").encode())
    if args.expect is not None:
        try:
            require_receipt_match(report, json.loads(args.expect.read_bytes()))
        except FileNotFoundError as error:
            print(f"ENV_BLOCKED: {error}", file=sys.stderr)
            return 2
        except ValueError as error:
            print(f"RECEIPT_MISMATCH: {error}", file=sys.stderr)
            return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
