"""Replay a fixed, exact rational Euler-factor identity at p=2."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path


def compute(*, p: int = 2, m: int = 8) -> dict:
    if type(p) is not int or p < 2 or type(m) is not int or m <= 0:
        raise ValueError("p >= 2 and integer m > 0 are required")
    cases = []
    for s in (2, 3, 4):
        x = Fraction(1, p**s)
        local_factor = 1 / (1 - x)
        derivative_coeff = x / (1 - x)
        partial = sum((x**k for k in range(1, m + 1)), Fraction(0))
        tail = x**(m + 1) / (1 - x)
        if partial + tail != derivative_coeff:
            raise ArithmeticError("geometric series identity failed")
        cases.append({
            "p": p, "s": s, "terms": m,
            "L_p": str(local_factor),
            "negative_log_derivative_over_log_p": str(derivative_coeff),
            "finite_prime_power_weight": str(partial),
            "exact_tail": str(tail),
            "identity_holds": True,
        })
    return {
        "schema": "e2a-prime-two-exact-local-surface-v1",
        "claim_scope": "EXACT_RATIONAL_EULER_FACTOR_IDENTITY_ONLY",
        "numeric_relevance_to_masullo_objection": "NOT_ESTABLISHED",
        "proof_of_either_rh_or_grh": "NO",
        "inputs": {"p": p, "m": m, "s": [2, 3, 4]},
        "cases": cases,
        "claim_authority": "NONE",
    }


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def verify_report(raw: bytes) -> None:
    recorded = json.loads(raw, object_pairs_hook=reject_duplicates)
    if json.dumps(recorded, sort_keys=True) != json.dumps(compute(), sort_keys=True):
        raise ValueError("report mismatch")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--verify-report", type=Path)
    mode.add_argument("--output", type=Path, help="write a generated report to this path")
    args = parser.parse_args()
    if args.verify_report:
        try:
            verify_report(args.verify_report.read_bytes())
        except (OSError, ValueError) as error:
            parser.exit(1, f"P2_EXACT_RATIONAL_REPORT_REJECTED: {error}\n")
        print("P2_EXACT_RATIONAL_REPORT_MATCH")
    else:
        encoded = json.dumps(compute(), indent=2, sort_keys=True) + "\n"
        if args.output is None:
            print(encoded, end="")
        else:
            args.output.write_bytes(encoded.encode("utf-8"))


if __name__ == "__main__":
    main()
