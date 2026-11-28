"""Check the scoped exterior-zero bridge against pinned Lean and source artifacts."""

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from replay_rh_proof_refs import MAIN_OLEAN_SHA256
from verify_landau_tail import LEAN_COMMIT, LOCK, PROOFS, ROOT, mathlib_environment, run


BRIDGE = "E2ADirichletExteriorBridge"
STATEMENTS = ROOT / "sources/rh-Statements.lean"
STATEMENTS_SHA = "79ef7ca776e42abe1f46caee13ea09bd19f1e2d0b1620d8d5d200258f33b47bf"
TARGET = "LFunction_eq_zero_re"
AXIOMS = {
    "exterior_empty",
    "exterior_hasSum_zero",
    "strip_only_countermodel",
}


def verify(lean: Path, project: Path, main: Path) -> dict:
    version = run([str(lean), "--version"], ROOT)
    if not version.startswith("Lean (version 4.33.1,") or f"commit {LEAN_COMMIT}," not in version:
        raise ValueError(f"unexpected Lean version: {version}")
    main_sha = sha256(main.read_bytes()).hexdigest()
    if main_sha != MAIN_OLEAN_SHA256:
        raise ValueError("the Main.olean bytes differ from the pinned artifact")
    extractor = ROOT / "tools/ProofRefs.lean"
    refs = json.loads(run([str(lean), "--run", str(extractor), str(main), TARGET], ROOT))
    if (refs["declaration"] != TARGET or refs["kind"] != "theorem"
            or refs["type_refs"] != ["DirichletLZerosOnLine"] or "claimAll" not in refs["value_refs"]):
        raise ValueError("unexpected original theorem type or proof reference")
    source = STATEMENTS.read_bytes()
    if sha256(source).hexdigest() != STATEMENTS_SHA:
        raise ValueError("the archived Statements source differs from the manifest")
    first, separator, body = source.partition(b"\n")
    if not separator or first.rstrip(b"\r") != b"import Mathlib":
        raise ValueError("unexpected archived Statements import")
    replacement = (
        b"import Mathlib.NumberTheory.LSeries.DirichletContinuation\n"
        b"import Mathlib.NumberTheory.LSeries.RiemannZeta\n"
    )
    env, commit = mathlib_environment(project, lean)
    bridge = PROOFS / f"{BRIDGE}.lean"
    with TemporaryDirectory(prefix="dirichlet-exterior-") as directory:
        work = Path(directory)
        (work / "Statements.lean").write_bytes(replacement + body)
        run([str(lean), "-j", "1", "-o", "Statements.olean", "Statements.lean"], work, env)
        env["LEAN_PATH"] = str(work) + os.pathsep + env["LEAN_PATH"]
        stdout = run([str(lean), f"--root={ROOT}", "-j", "1", str(bridge)], ROOT, env)
    names = set()
    for line in stdout.splitlines():
        head, _, tail = line.partition("' depends on axioms: [")
        if not head.startswith(f"'{BRIDGE}.") or not tail.endswith("]"):
            raise ValueError(f"unexpected Lean axiom output: {line}")
        name = head.removeprefix(f"'{BRIDGE}.")
        if name in names or not set(tail[:-1].split(", ")) <= {"propext", "Classical.choice", "Quot.sound"}:
            raise ValueError(f"unexpected axiom dependencies: {line}")
        names.add(name)
    if names != AXIOMS:
        raise ValueError("incomplete axiom log")
    return {
        "status": "PASS_CONDITIONAL_BRIDGE",
        "lean_version": version,
        "mathlib_commit": commit,
        "dependency_lock_sha256": sha256(LOCK.read_bytes()).hexdigest(),
        "bridge_sha256": sha256(bridge.read_bytes()).hexdigest(),
        "statements_sha256": STATEMENTS_SHA,
        "statement_body_sha256": sha256(body).hexdigest(),
        "statement_replay_imports": replacement.decode().splitlines(),
        "main_olean_sha256": main_sha,
        "original_declaration_references": refs,
        "original_proof_kernel_replay": "NOT_RUN",
        "axioms": stdout.splitlines(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--mathlib-project", required=True, type=Path)
    parser.add_argument("--main", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    payload = verify(args.lean.resolve(), args.mathlib_project.resolve(), args.main.resolve())
    with args.report.open("x", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"], args.report)


if __name__ == "__main__":
    main()
