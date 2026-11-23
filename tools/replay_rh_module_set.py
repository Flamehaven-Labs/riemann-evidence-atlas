"""Replay the first cross-module references of RH's compiled declarations."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import tarfile
from tempfile import TemporaryDirectory

from replay_proof_dependency import extract
from riemann_evidence.proof_dependency import inspect_module_set


ARCHIVE_SHA256 = "31ed2ace3a3d2a3daff6dc689d7848c15f5d7ce77a71eb68d481b03e72b7cabe"
MAIN_SHA256 = "9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad"
TARGETS = {
    "Main": ("riemannHypothesis",),
    "Supplements.Kernels.MainTheorems": ("rhOfAll", "allChi"),
}
BRANCHES = {
    "Formalism.GammaFactorNonvanishing.CritLine": (
        "Formalism.VW.rh_of_every",
        "10eb57ebfe01dffd2cff3890214eed84dc5e1373da81ddadb6c98eccc40341e7",
        "alp-oleans-Formalism.tar.gz",
    ),
    "Development.AutomorphicArithmetic.CharacterBoxes.MainConclusion": (
        "UpperTheory.FinalTheorems.everyCharacter",
        "96f053d27b81461fcf5ca2fe9a234384bc6ead9697de76cee37e13686aa156df",
        "alp-oleans-Development-AutomorphicArithmetic.tar.gz",
    ),
}
RH_OF_RIGHT_MODULE = "Formalism.GammaFactorNonvanishing.RhOfRight"
RH_OF_RIGHT_INPUT = (
    "Formalism.VW.rh_of_right",
    "cf24f82f3f24144070062b19beedf83f0919c4e894c56759597fa76e2e93bc70",
    "alp-oleans-Formalism.tar.gz",
)
EVERY_CHARACTER = "UpperTheory.FinalTheorems.everyCharacter"
EVERY_CHARACTER_OF_ROW = "UpperTheory.FinalTheorems.everyCharacter_of_row"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--branch-dir", type=Path,
                        help="directory containing both individually pinned branch .olean files")
    parser.add_argument("--next-layer", action="store_true",
                        help="also inspect rh_of_right and everyCharacter_of_row")
    args = parser.parse_args()
    if args.next_layer and args.branch_dir is None:
        parser.error("--next-layer requires --branch-dir")

    archive_digest = sha256(args.archive.read_bytes()).hexdigest()
    if archive_digest != ARCHIVE_SHA256:
        parser.error("compiled module archive SHA-256 differs from pin")

    records = []
    module_by_declaration = {}
    inputs = {}
    with TemporaryDirectory(prefix="riemann-module-set-") as directory:
        with tarfile.open(args.archive, mode="r:gz") as archive:
            for module, names in TARGETS.items():
                member = f"alp-oleans/lib/{module.replace('.', '/')}.olean"
                info = archive.getmember(member)
                if not info.isfile():
                    raise ValueError(f"expected a regular compiled artifact: {member}")
                compiled = Path(directory) / Path(member).name
                with archive.extractfile(info) as source:
                    compiled.write_bytes(source.read())
                receipt = extract(
                    args.lean.resolve(), compiled, list(names),
                    expected_sha=MAIN_SHA256 if module == "Main" else None,
                )
                if [row["declaration"] for row in receipt["records"]] != list(names):
                    raise ValueError(f"extractor returned unexpected declarations: {module}")
                records.extend(receipt["records"])
                module_by_declaration.update(dict.fromkeys(names, module))
                inputs[module] = {"archive_member": member, "sha256": receipt["module_sha256"]}

    if args.branch_dir is not None:
        branches = dict(BRANCHES)
        if args.next_layer:
            branches[RH_OF_RIGHT_MODULE] = RH_OF_RIGHT_INPUT
        for module, (name, digest, archive_name) in branches.items():
            member = f"alp-oleans/lib/{module.replace('.', '/')}.olean"
            compiled = args.branch_dir / Path(member).name
            names = [name]
            if args.next_layer and name == EVERY_CHARACTER:
                names.append(EVERY_CHARACTER_OF_ROW)
            branch = extract(args.lean.resolve(), compiled, names, expected_sha=digest)
            if [row["declaration"] for row in branch["records"]] != names:
                raise ValueError(f"extractor returned unexpected declaration: {module}")
            records.extend(branch["records"])
            module_by_declaration.update(dict.fromkeys(names, module))
            inputs[module] = {
                "archive": archive_name, "archive_member": member,
                "sha256": branch["module_sha256"],
            }

    root = "riemannHypothesis"
    analysis = inspect_module_set(records, module_by_declaration, root)
    cross_value_edges = {
        (edge["from"], edge["to"]) for edge in analysis["resolved_edges"]
        if edge["kind"] == "value" and edge["from_module"] != edge["to_module"]
    }
    if (root, "rhOfAll") not in cross_value_edges:
        raise ValueError("expected proof-value edge across the two compiled modules")
    if "rhOfAll" in analysis["external_or_unresolved_references"]:
        raise ValueError("rhOfAll remained unresolved after loading its compiled declaration")
    if args.branch_dir is not None:
        expected_branches = {
            ("rhOfAll", "Formalism.VW.rh_of_every"),
            ("allChi", "UpperTheory.FinalTheorems.everyCharacter"),
        }
        if not expected_branches.issubset(cross_value_edges):
            raise ValueError("expected proof-value edges to both compiled branch declarations")
    if args.next_layer:
        value_edges = {
            (edge["from"], edge["to"]) for edge in analysis["resolved_edges"]
            if edge["kind"] == "value"
        }
        expected_layer = {
            ("Formalism.VW.rh_of_every", RH_OF_RIGHT_INPUT[0]),
            (EVERY_CHARACTER, EVERY_CHARACTER_OF_ROW),
        }
        if not expected_layer.issubset(value_edges):
            raise ValueError("expected proof-value edges to both next-layer declarations")

    print(json.dumps({
        "schema": "riemann-evidence-rh-module-set-replay-v1",
        "archive_sha256": archive_digest,
        "module_inputs": inputs,
        "extractor_sha256": receipt["extractor_sha256"],
        "lean_version": receipt["lean_version"],
        "records": records,
        "analysis": analysis,
        "claim_authority": "NONE",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
