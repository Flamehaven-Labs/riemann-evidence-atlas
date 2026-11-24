"""Second RH-only Landau tail case; preserve the v0.2.0 ten-case report."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

from riemann_evidence.verification import run_verification
from window_kernel import CHECK, unique_object

ROOT = Path(__file__).resolve().parent
SOURCE = "sources/rh-landauWindowIneq.lean"
SOURCE_SHA = "e3d5d760bcefe1242d4f5b0ced44fc055f1fa8dfe048a2222cf2c39ae812e59c"
MANIFEST = "lean-extract-manifest.json"
MANIFEST_SHA = "60e69fe0e8acea56ea843c826c44236bbc225663f17276fbcbc099973c67a082"
# Fixed before running the new case; midpoint of the predicted 128-bit interval.
NEAR_CAP = "242158075435671337967324601779809645921/2722258935367507707706996859454145691648"
MODEL = {"component": "outside_window", "k": 1, "rate": "2", "a": "1/2", "b": "2"}
CASES = (
    ("valid_cap", "1/10", 128, "PASS"),
    ("violated_cap", "1/20", 128, "FAIL"),
    ("precision_exhausted", NEAR_CAP, 128, "UNRESOLVED"),
    ("refined_cap", NEAR_CAP, 256, "PASS"),
)


def run_cases() -> dict:
    """Use the original CHECK for each exact input. No new arithmetic backend."""
    manifest = (ROOT / MANIFEST).read_bytes()
    if sha256(manifest).hexdigest() != MANIFEST_SHA:
        raise ValueError("original extract manifest mismatch")
    # The original source itself is optional in a clean checkout.
    source = ROOT / SOURCE
    if source.is_file() and sha256(source.read_bytes()).hexdigest() != SOURCE_SHA:
        raise ValueError("local original source mismatch")
    cases = {}
    for name, cap, budget, expected in CASES:
        model = {**MODEL, "cap": cap, "precision_bits": budget}
        raw = json.dumps(model, sort_keys=True).encode("utf-8")
        report = run_verification(CHECK, {"window": raw})
        if report["status"] != expected or report["details"].get("fractional_bits") != budget:
            raise ValueError(f"unexpected decision or precision: {name}: {report}")
        cases[name] = {"input": model, "report": report}
    return {
        "schema": "riemann-evidence-landau-second-case-v1",
        "source": {"declaration": "Deduction.landau_window_ineq",
                   "surface": "third RHS term, integral only; excludes 2*C0",
                   "path": SOURCE, "sha256": SOURCE_SHA,
                   "extract_manifest_sha256": MANIFEST_SHA},
        "source_claim": "PARAMETERIZED_KERNEL_SPECIALIZATION",
        "formal_real_proof": "NOT_RUN",
        "claim_authority": "NONE",
        "code_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest()
                        for p in ("landau_second_case.py", "window_kernel.py",
                                  "riemann_evidence/rational_intervals.py",
                                  "riemann_evidence/verification.py")},
        "cases": cases,
    }


def verify_saved_report(raw: bytes) -> bool:
    try:
        observed = json.loads(raw, object_pairs_hook=unique_object)
    except (ValueError, UnicodeError):
        return False
    return json.dumps(observed, sort_keys=True) == json.dumps(run_cases(), sort_keys=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--emit", action="store_true", help="print candidate report without writing")
    group.add_argument("--verify-report", type=Path)
    args = parser.parse_args()
    if args.emit:
        print(json.dumps(run_cases(), indent=2, sort_keys=True))
        return 0
    ok = verify_saved_report(args.verify_report.read_bytes())
    print("LANDAU_SECOND_CASE_REPORT_MATCH" if ok else "LANDAU_SECOND_CASE_REPORT_MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
