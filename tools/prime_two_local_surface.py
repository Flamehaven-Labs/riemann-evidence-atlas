"""Replay exact rational local Euler factors and character comparisons."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path

# Each residue table is indexed modulo its length. The primitive table's
# length is the conductor. Dirichlet characters are zero on nonunits.
CHARACTERS = (
    ("trivial_mod_1", (1,), (1,)),
    ("quadratic_mod_3", (0, 1, -1), (0, 1, -1)),
    ("primitive_mod_4", (0, 1, 0, -1), (0, 1, 0, -1)),
    ("principal_mod_4", (0, 1, 0, 1), (1,)),
)


def local_terms(x: Fraction, terms: int) -> dict:
    factor = 1 / (1 - x)
    derivative = x * factor
    partial = sum((x**k for k in range(1, terms + 1)), Fraction(0))
    tail = x**(terms + 1) * factor
    if partial + tail != derivative:
        raise ArithmeticError("geometric series identity failed")
    return {
        "L_p": str(factor),
        "negative_log_derivative_over_log_p": str(derivative),
        "finite_prime_power_weight": str(partial),
        "exact_tail": str(tail),
        "identity_holds": True,
    }


def compute(*, p: int = 2, m: int = 8) -> dict:
    if type(p) is not int or p < 2 or type(m) is not int or m <= 0:
        raise ValueError("p >= 2 and integer m > 0 are required")
    cases = []
    for s in (2, 3, 4):
        x = Fraction(1, p**s)
        cases.append({"p": p, "s": s, "terms": m, **local_terms(x, m)})
    return {
        "schema": "e2a-prime-two-exact-local-surface-v1",
        "claim_scope": "EXACT_RATIONAL_EULER_FACTOR_IDENTITY_ONLY",
        "numeric_relevance_to_masullo_objection": "NOT_ESTABLISHED",
        "proof_of_either_rh_or_grh": "NO",
        "inputs": {"p": p, "m": m, "s": [2, 3, 4]},
        "cases": cases,
        "claim_authority": "NONE",
    }


def compute_character_comparison() -> dict:
    p, s, terms = 2, 2, 8
    cases = []
    for label, level_values, primitive_values in CHARACTERS:
        modulus, conductor = len(level_values), len(primitive_values)
        level_chi = level_values[p % modulus]
        primitive_chi = primitive_values[p % conductor]
        level = local_terms(Fraction(level_chi, p**s), terms)
        primitive_x = Fraction(primitive_chi, p**s)
        primitive = local_terms(primitive_x, terms)
        omitted_by_level = modulus % p == 0 and conductor % p != 0
        removal_x = primitive_x if omitted_by_level else Fraction(0)
        factor = 1 - removal_x
        removal_derivative = -removal_x / factor
        derivative_key = "negative_log_derivative_over_log_p"
        if (
            Fraction(level["L_p"]) != factor * Fraction(primitive["L_p"])
            or Fraction(level[derivative_key])
            != Fraction(primitive[derivative_key]) + removal_derivative
        ):
            raise ArithmeticError(f"change-of-level identity failed: {label}")
        cases.append({
            "character": label,
            "modulus": modulus,
            "conductor": conductor,
            "ramified_at_p": conductor % p == 0,
            "omitted_by_level": omitted_by_level,
            "at_level": {"character_at_p": level_chi, **level},
            "at_conductor": {"character_at_p": primitive_chi, **primitive},
            "finite_removal_factor": str(factor),
            "finite_removal_log_derivative_coefficient": str(removal_derivative),
        })
    return {
        "schema": "e2a-prime-two-character-comparison-v2",
        "claim_scope": "EXACT_RATIONAL_LOCAL_EULER_FACTORS",
        "trace_formula_correspondence": "HELD",
        "claim_authority": "NONE",
        "inputs": {"p": p, "s": s, "terms": terms},
        "cases": cases,
    }


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def verify_report(raw: bytes, *, characters: bool = False) -> None:
    recorded = json.loads(raw, object_pairs_hook=reject_duplicates)
    expected = compute_character_comparison() if characters else compute()
    if json.dumps(recorded, sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("report mismatch")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--characters", action="store_true", help="use the four fixed character cases")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--verify-report", type=Path)
    mode.add_argument("--output", type=Path, help="write a generated report to this path")
    args = parser.parse_args()
    if args.verify_report:
        try:
            verify_report(args.verify_report.read_bytes(), characters=args.characters)
        except (OSError, ValueError) as error:
            parser.exit(1, f"P2_EXACT_RATIONAL_REPORT_REJECTED: {error}\n")
        print("P2_EXACT_RATIONAL_REPORT_MATCH")
    else:
        report = compute_character_comparison() if args.characters else compute()
        encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.output is None:
            print(encoded, end="")
        else:
            args.output.write_bytes(encoded.encode("utf-8"))


if __name__ == "__main__":
    main()
