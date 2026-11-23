"""Replay the standalone baseline and, optionally, pinned original input bytes."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
NEXT_LAYER = "docs/rh-next-layer-module-set.json"
FRONTIER = "docs/rh-frontier-classification.json"
PRIME_TWO = "docs/masullo/P2_LOCAL_SURFACE.json"
PRIME_TWO_CHARACTERS = "docs/masullo/P2_CHARACTER_COMPARISON.json"
RECEIPTS = {
    "window-results-v2.json": "ad3d31ceaf5a9a78e5f17f5c25ac087394eb57ebfb3cfdd977aa57c61ac66bf1",
    PRIME_TWO: "298d90f4f80e932d6d1eb1034dd76fca519555dada786964f0b5d7ce28cdec03",
    PRIME_TWO_CHARACTERS: "bbdc488501a875c0d0121d386f2b3e0a6d5b4edbcbc03bc6e1db0231e3ddbd89",
    "docs/rh-module-set-pilot.json": "0b541e3ceb684e8f457fc6a91f84256bc13943a5519f2b85cb6b1ae15f37ac34",
    "docs/rh-branch-module-set.json": "f213bd94da41795a8bf8dff610312679cdb32347e08ab8420f4bddb39f7bf90c",
    NEXT_LAYER: "de121ac9ac426cc666410147abe107ab41e2d06effc01e4e2c480e88a1a1e582",
    FRONTIER: "1d38bce4b88b68c1979ac9889a25873de321070523ac7306b2583b1bce0b5e99",
}


def require_sha256(path: Path, expected: str) -> None:
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError(f"SHA-256 mismatch: {path}")


def run_python(*args: str, capture: bool = False) -> bytes | None:
    return subprocess.run(
        [sys.executable, "-E", "-S", *args],
        cwd=ROOT, check=True, capture_output=capture, timeout=300,
    ).stdout


def portable_replay() -> None:
    for relative, digest in RECEIPTS.items():
        require_sha256(ROOT / relative, digest)
    run_python("-m", "unittest", "discover", "-s", "tests", "-v")
    run_python("window_kernel.py", "--verify-report", "window-results-v2.json")
    run_python("tools/prime_two_local_surface.py", "--verify-report", PRIME_TWO)
    run_python("tools/prime_two_local_surface.py", "--characters", "--verify-report", PRIME_TWO_CHARACTERS)
    run_python("tools/local_notebook_smoke.py")
    print("P0_PORTABLE_BASELINE_PASS", flush=True)


def source_replay(lean: Path, assets: Path, pdf: Path) -> None:
    archive = assets / "alp-oleans-Main-and-small.tar.gz"
    graph = assets / "verified-rh-graph.json.gz"
    branches = assets / "branch-inputs"
    for path in (lean, archive, graph, pdf, *(branches / name for name in (
        "CritLine.olean", "MainConclusion.olean", "RhOfRight.olean",
    ))):
        if not path.is_file():
            raise FileNotFoundError(path)
    require_sha256(pdf, "e039d3f6cf0a4b14f03c7edb85097752dd65c0a2fe543c76fe992be234f97bf5")

    version = subprocess.check_output([str(lean), "--version"], timeout=30).decode().strip()
    if not version.startswith("Lean (version 4.33.1,"):
        raise ValueError(f"expected Lean 4.33.1: {version}")
    compile_check = subprocess.run(
        [str(lean), "-j", "2", "tests/lean/E2ATailCapCertificate.lean"],
        cwd=ROOT, check=True, capture_output=True, timeout=120,
    )
    if compile_check.stderr or b"sorryAx" in compile_check.stdout:
        raise ValueError("unexpected Lean certificate output")
    print("RATIONAL_TAIL_CAP_LEAN_PASS", flush=True)

    base = ("--lean", str(lean), "--archive", str(archive), "--branch-dir", str(branches))
    for command, expected in (
        (("tools/replay_rh_module_set.py", *base, "--next-layer"), NEXT_LAYER),
        (("tools/replay_rh_frontier.py", *base, "--frontier", NEXT_LAYER, "--graph", str(graph)), FRONTIER),
    ):
        for attempt in (1, 2):
            stdout = run_python(*command, capture=True)
            assert stdout is not None
            if stdout.replace(b"\r\n", b"\n") != (ROOT / expected).read_bytes():
                raise ValueError(f"replay differs from pinned receipt: {expected} (attempt {attempt})")
            print(f"PINNED_REPLAY_MATCH {expected} {attempt}/2", flush=True)
    print("P0_PINNED_SOURCE_REPLAY_PASS", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("lean", "proof-assets", "masullo-pdf"):
        parser.add_argument(f"--{option}", type=Path)
    args = parser.parse_args()
    sources = (args.lean, args.proof_assets, args.masullo_pdf)
    if any(sources) and not all(sources):
        parser.error("--lean, --proof-assets and --masullo-pdf must be supplied together")

    try:
        portable_replay()
        if all(sources):
            source_replay(*(path.resolve() for path in sources))
        else:
            print("P0_PINNED_SOURCE_REPLAY_NOT_RUN")
    except FileNotFoundError as error:
        print(f"ENV_BLOCKED: {error}", file=sys.stderr)
        return 2
    except (subprocess.SubprocessError, ValueError) as error:
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            sys.stderr.buffer.write(error.stderr)
        print(f"BASELINE_REPLAY_FAILED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
