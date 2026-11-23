"""Read direct references from the published Main.olean using its pinned Lean."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess


MAIN_OLEAN_SHA256 = "9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad"
EXTRACTOR = Path(__file__).with_name("ProofRefs.lean").resolve()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--module", type=Path, required=True)
    args = parser.parse_args()
    lean = args.lean.resolve()
    module = args.module.resolve()

    digest = sha256(module.read_bytes()).hexdigest()
    if digest != MAIN_OLEAN_SHA256:
        parser.error("Main.olean SHA-256 differs from the published proof artifact")
    version = subprocess.check_output([str(lean), "--version"], text=True).strip()
    if not re.match(r"Lean \(version 4\.33\.1,", version):
        parser.error(f"expected Lean 4.33.1, got {version}")

    raw = subprocess.check_output(
        [str(lean), "--run", str(EXTRACTOR), str(module), "riemannHypothesis"],
        text=True,
    )
    result = json.loads(raw)
    if (
        result["declaration"] != "riemannHypothesis"
        or result["kind"] != "theorem"
        or result["type_refs"] != ["RiemannHypothesis"]
        or result["value_refs"] != ["rhOfAll"]
        or not {"Statements", "Supplements.Kernels.MainTheoremsAll"}.issubset(
            result["module_imports"]
        )
    ):
        raise ValueError("unexpected declaration references in the pinned Main.olean")
    result.update({
        "module_sha256": digest,
        "extractor_sha256": sha256(EXTRACTOR.read_bytes()).hexdigest(),
        "lean_version": version,
        "dependency_scope": "DIRECT_STORED_EXPRESSION_REFERENCES",
        "original_proof_kernel_replay": "NOT_RUN",
    })
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
