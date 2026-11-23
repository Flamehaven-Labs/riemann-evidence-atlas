"""Check Lean declaration matching on a fixture and optional pinned RH inputs."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from riemann_evidence.proof_dependency import inspect_value_paths, normalize_records

CATALOG = ROOT / "tools/ProofCatalog.lean"
FIXTURE = ROOT / "tests/lean/ChoiceDependenceFixture.lean"
LEAN_COMMIT = "819816b2e0a3bf405af45ae5c7af2491d8f5bee6"
RH_RIGHT_MODULE = "Formalism.GammaFactorNonvanishing.RhOfRight"
RH_RIGHT_SHA256 = "cf24f82f3f24144070062b19beedf83f0919c4e894c56759597fa76e2e93bc70"
FRONTIER = ROOT / "docs/rh-frontier-classification.json"
FRONTIER_SHA256 = "1d38bce4b88b68c1979ac9889a25873de321070523ac7306b2583b1bce0b5e99"

FIXTURE_KINDS = {
    "auditChosenNat": "definition",
    "auditComputedFromChosen": "definition",
    "auditProofMentionsComputed": "theorem",
    "auditProofCallsChoice": "theorem",
    "auditJoinChoicePaths": "theorem",
    "auditFixtureAxiom": "axiom",
    "auditOpaque": "opaque",
    "Bool": "inductive",
    "Bool.true": "constructor",
    "Bool.rec": "recursor",
    "Classical.choice": "axiom",
}


def require_pin(path: Path, digest: str) -> bytes:
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != digest:
        raise ValueError(f"SHA-256 differs from pin: {path}")
    return raw


def catalog(lean: Path, directory: Path, names: set[str], module: str, artifact: Path):
    request = directory / "request.json"
    request.write_text(json.dumps({
        "names": sorted(names),
        "artifacts": [[module, str(artifact)]],
        "includeInit": True,
    }), encoding="utf-8")
    raw = subprocess.check_output(
        [str(lean), "-j", "2", "--run", str(CATALOG), str(request)], timeout=150,
    )
    rows = normalize_records(json.loads(raw))
    if rows.keys() - names:
        raise ValueError("catalog returned an unrequested declaration")
    return rows


def fixture_match(lean: Path, directory: Path) -> dict:
    fixture = directory / FIXTURE.name
    fixture.write_bytes(FIXTURE.read_bytes())
    compiled = fixture.with_suffix(".olean")
    subprocess.run(
        [str(lean), "-j", "2", "-o", str(compiled), fixture.name],
        cwd=directory, check=True, timeout=150,
    )
    rows = catalog(lean, directory, set(FIXTURE_KINDS), fixture.stem, compiled)
    if {name: row["kind"] for name, row in rows.items()} != FIXTURE_KINDS:
        raise ValueError("fixture declaration kinds differ")
    if rows["auditFixtureAxiom"]["value_refs"] is not None:
        raise ValueError("an axiom has no stored VALUE")
    paths = inspect_value_paths(list(rows.values()), "auditJoinChoicePaths")["choice_paths"]
    expected = {
        ("auditJoinChoicePaths", "auditProofCallsChoice", "Classical.choice"),
        ("auditJoinChoicePaths", "auditComputedFromChosen", "auditChosenNat", "Classical.choice"),
    }
    if {tuple(row["path"]) for row in paths} != expected or len(paths) != len(expected):
        raise ValueError(f"fixture choice paths differ: {paths!r}")
    return {"declarations": {name: rows[name] for name in sorted(rows)}, "choice_paths": paths}


def original_match(lean: Path, directory: Path, artifact: Path) -> dict:
    require_pin(artifact, RH_RIGHT_SHA256)
    frontier = json.loads(require_pin(FRONTIER, FRONTIER_SHA256))["frontier"]
    helpers = {row["name"]: row["value_refs"] for row in frontier
               if row["name"] in {"Formalism.VW.rh_of_right._proof_1_1", "Formalism.VW.rh_of_right._proof_1_2"}}
    names = set(helpers)
    referrers: dict[str, list[str]] = {}
    for helper, refs in helpers.items():
        for name in refs:
            referrers.setdefault(name, []).append(helper)
    rows = catalog(lean, directory, names | referrers.keys(), RH_RIGHT_MODULE, artifact)
    for helper, refs in helpers.items():
        row = rows[helper]
        if (row["value_refs"] != refs or row["kind"] != "theorem"
                or row["module"] != RH_RIGHT_MODULE or row["evidence"] != "SUPPLIED_OLEAN"):
            raise ValueError(f"stored VALUE differs from pin: {helper}")
    return {
        "input_olean_sha256": RH_RIGHT_SHA256,
        "helpers": [rows[name] for name in sorted(names)],
        "distinct_helper_value_references": len(referrers),
        "references": [
            {"referrers": sorted(referrers[name]), "declaration": name, "match": rows.get(name)}
            for name in sorted(referrers)
        ],
        "transitive_closure": "NOT_RUN",
    }


def semantic_digest(semantic: dict) -> str:
    return sha256(json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def verify(lean: Path, artifact: Path | None) -> dict:
    version = subprocess.check_output([str(lean), "--version"], timeout=30).decode().strip()
    if not version.startswith("Lean (version 4.33.1,") or f"commit {LEAN_COMMIT}," not in version:
        raise ValueError(f"expected pinned Lean 4.33.1: {version}")
    with TemporaryDirectory(prefix="riemann-lean-match-") as temp:
        directory = Path(temp)
        fixture = fixture_match(lean, directory)
        original = original_match(lean, directory, artifact) if artifact is not None else None
    semantic = {
        "schema": "riemann-evidence-lean-match-v2",
        "lean_commit": LEAN_COMMIT,
        "catalog_sha256": sha256(CATALOG.read_bytes()).hexdigest(),
        "fixture_source_sha256": sha256(FIXTURE.read_bytes()).hexdigest(),
        "fixture": fixture,
        "original": original,
        "original_proof_kernel_replay": "NOT_RUN",
    }
    return {"semantic": semantic, "semantic_sha256": semantic_digest(semantic), "lean_version": version}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--rh-of-right", type=Path)
    parser.add_argument("--expect", type=Path, help="compare canonical declarations and their input pins")
    args = parser.parse_args()
    try:
        report = verify(args.lean.resolve(), args.rh_of_right.resolve() if args.rh_of_right else None)
        if args.expect is not None:
            reference = json.loads(args.expect.read_bytes())
            if (not isinstance(reference, dict) or not isinstance(reference.get("semantic"), dict)
                    or semantic_digest(reference["semantic"]) != reference.get("semantic_sha256")
                    or report["semantic_sha256"] != reference["semantic_sha256"]):
                raise ValueError("Lean declaration comparison differs from pinned report")
    except FileNotFoundError as error:
        print(f"ENV_BLOCKED: {error}", file=sys.stderr)
        return 2
    except (ValueError, subprocess.SubprocessError) as error:
        print(f"LEAN_MATCH_FAILED: {error}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write((json.dumps(report, indent=2, sort_keys=True) + "\n").encode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
