"""Enclose Landau window and tail integrals with exact rational arithmetic."""

import json
from collections.abc import Callable
from fractions import Fraction

from riemann_evidence.rational_intervals import PRECISIONS, exp_bounds, expm1_bounds
from riemann_evidence.verification import Finding, Status, Verification, run_verification


def polynomial(k: int, x: Fraction) -> Fraction:
    """Return the finite sum of x**j / j! for 0 <= j <= k."""
    term = total = Fraction(1)
    for j in range(1, k + 1):
        term *= x / j
        total += term
    return total


def kernel_mass(k: int, rate: Fraction, a: Fraction, b: Fraction, bits: int):
    """Enclose the integral of u**k * exp(-rate*u) / k! from a to b."""
    if type(k) is not int or not 0 <= k <= 64 or rate <= 0 or not 0 <= a < b or rate*b > 16:
        raise ValueError("expected integer 0 <= k <= 64, rate > 0, 0 <= a < b, and rate*b <= 16")
    left = polynomial(k, rate*a)
    right = polynomial(k, rate*b)
    lo_a, hi_a = exp_bounds(-rate*a, bits)
    lo_b, hi_b = exp_bounds(-rate*b, bits)
    scale = rate**(k + 1)
    lo = max(Fraction(0), (left*lo_a - right*hi_b) / scale)
    hi = (left*hi_a - right*lo_b) / scale
    return lo, hi


def rational(value):
    if not isinstance(value, str) or len(value) > 512:
        raise ValueError("expected a rational string of at most 512 characters")
    return Fraction(value)


def unique_object(pairs):
    output = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate field {key}")
        output[key] = value
    return output


def decide_upper_cap(
    enclose: Callable[[int], tuple[Fraction, Fraction]],
    cap: Fraction,
    budget: int,
) -> Finding:
    """Decide x <= cap only when justified by an outward enclosure of x."""
    if type(budget) is not int or budget not in PRECISIONS:
        raise ValueError("unsupported precision budget")
    for bits in PRECISIONS:
        if bits > budget:
            break
        lo, hi = enclose(bits)
        if not isinstance(lo, Fraction) or not isinstance(hi, Fraction) or lo > hi:
            raise ArithmeticError("invalid outward enclosure")
        details = {"lower": str(lo), "upper": str(hi), "cap": str(cap), "fractional_bits": bits}
        if hi <= cap:
            return Finding(Status.PASS, {**details, "reason": "upper endpoint meets cap"})
        if lo > cap:
            return Finding(Status.FAIL, {**details, "reason": "lower endpoint exceeds cap"})
    return Finding(Status.UNRESOLVED, {**details, "reason": "precision budget exhausted"})


def evaluate(evidence):
    try:
        raw = evidence["window"]
        if len(raw) > 4096:
            raise ValueError("input exceeds 4096 bytes")
        case = json.loads(raw, object_pairs_hook=unique_object)
        if not isinstance(case, dict) or set(case) != {
            "component", "k", "rate", "a", "b", "cap", "precision_bits"
        }:
            raise ValueError("unexpected window fields")
        k = case["k"]
        rate, a, b, cap = (rational(case[key]) for key in ("rate", "a", "b", "cap"))
        budget = case["precision_bits"]
        if cap < 0:
            raise ValueError("negative cap")
        component = case["component"]
        if component not in ("window", "outside_window"):
            raise ValueError("unknown kernel component")

        def enclose(bits):
            lo, hi = kernel_mass(k, rate, a, b, bits)
            if component == "window":
                return lo, hi
            total = Fraction(1) / rate**(k + 1)
            return max(Fraction(0), total - hi), total - lo

        return decide_upper_cap(enclose, cap, budget)
    except (ValueError, ZeroDivisionError) as exc:
        return Finding(Status.FAIL, {"reason": f"invalid window: {exc}"})


CHECK = Verification(
    check_id="landau-window-kernel-mass",
    revision="3",
    target="Window or complementary positive-axis integral of u^k exp(-rate*u)/k!",
    method="Closed-form primitive and total mass with outward rational bounds",
    domain="Dimensionless nonnegative window; positive rate; rate*b <= 16",
    evidence_class="BOUNDED_NUMERICAL_KERNEL_CHECK",
    inputs=("window",),
    evaluate=evaluate,
)


def evaluate_nsrw_ratio(evidence):
    try:
        raw = evidence["ratio"]
        if len(raw) > 4096:
            raise ValueError("input exceeds 4096 bytes")
        case = json.loads(raw, object_pairs_hook=unique_object)
        if not isinstance(case, dict) or set(case) != {"lambda", "cap", "precision_bits"}:
            raise ValueError("unexpected ratio fields")
        lam, cap = rational(case["lambda"]), rational(case["cap"])
        if lam != Fraction(1, 10**12) or cap < 0:
            raise ValueError("expected fixed MB-06 lambda and a nonnegative cap")
        return decide_upper_cap(
            lambda bits: mb06_ratio(lam, bits), cap, case["precision_bits"]
        )
    except (ValueError, ZeroDivisionError) as exc:
        return Finding(Status.FAIL, {"reason": f"invalid ratio input: {exc}"})
    except ArithmeticError as exc:
        return Finding(Status.UNRESOLVED, {"reason": str(exc)})


def mb06_ratio(lam: Fraction, bits: int) -> tuple[Fraction, Fraction]:
    num_lo, num_hi = expm1_bounds(Fraction(17, 10) * lam, bits)
    den_lo, den_hi = expm1_bounds(2 * lam, bits)
    if not (0 < num_lo <= num_hi and 0 < den_lo <= den_hi):
        raise ArithmeticError("positive ratio factors could not be enclosed")
    return num_lo / den_hi, num_hi / den_lo


NSRW_CHECK = Verification(
    check_id="nsrw-mb06-normalized-ratio-cap",
    revision="1",
    target="Normalized factor R(lambda) in the MomentBound inequality",
    method="Outward rational expm1 intervals and the shared upper-cap decision rule",
    domain="Dimensionless factor at the fixed MB-06 lambda=1/10^12",
    evidence_class="BOUNDED_NUMERICAL_FACTOR_CHECK",
    inputs=("ratio",),
    evaluate=evaluate_nsrw_ratio,
)


def run_cases():
    base = {
        "component": "window", "k": 3, "rate": "2", "a": "0", "b": "4",
        "cap": "1/16", "precision_bits": 128,
    }
    landau = {**base, "rate": "3", "a": "1", "b": "3", "cap": "1/100"}
    tail = {**landau, "component": "outside_window"}
    lo, hi = kernel_mass(3, Fraction(2), Fraction(0), Fraction(4), 128)
    midpoint = str((lo + hi) / 2)
    cases = {
        "landau_shaped_window": (landau, "PASS"),
        "landau_tail_valid_cap": ({**tail, "cap": "1/200"}, "PASS"),
        "landau_tail_violated_cap": ({**tail, "cap": "1/300"}, "FAIL"),
        "valid_cap": (base, "PASS"),
        "violated_cap": ({**base, "cap": "1/32"}, "FAIL"),
        "precision_exhausted": ({**base, "cap": midpoint}, "UNRESOLVED"),
        "refined_cap": ({**base, "cap": midpoint, "precision_bits": 256}, "PASS"),
        "invalid_window": ({**base, "b": "-4"}, "FAIL"),
    }
    reports = {}
    for name, (case, expected) in cases.items():
        raw = json.dumps(case, sort_keys=True).encode()
        reports[name] = run_verification(CHECK, {"window": raw})
        if reports[name]["status"] != expected:
            raise AssertionError((name, reports[name]))
    assert reports["refined_cap"]["details"]["fractional_bits"] == 256
    # For rate=1, k=0, the integral on [0,1] equals 1-exp(-1).
    lo, hi = kernel_mass(0, Fraction(1), Fraction(0), Fraction(1), 128)
    assert Fraction(63, 100) < lo <= hi < Fraction(64, 100)
    for name, cap, expected in (
        ("nsrw_ratio_valid_cap", "17/20", "PASS"),
        ("nsrw_ratio_violated_cap", "849/1000", "FAIL"),
    ):
        raw = json.dumps(
            {"lambda": "1/1000000000000", "cap": cap, "precision_bits": 128},
            sort_keys=True,
        ).encode()
        reports[name] = run_verification(NSRW_CHECK, {"ratio": raw})
        assert reports[name]["status"] == expected, (name, reports[name])
    return reports


def verify_saved_report(raw: bytes) -> bool:
    """Recompute the complete case suite and check its parsed report."""
    try:
        report = json.loads(raw, object_pairs_hook=unique_object)
    except (ValueError, UnicodeError):
        return False
    return json.dumps(report, sort_keys=True) == json.dumps(run_cases(), sort_keys=True)


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument("--window", type=Path, help="JSON for a Landau window or tail")
    inputs.add_argument("--ratio", type=Path, help="JSON for the fixed MB-06 ratio")
    inputs.add_argument("--verify-report", type=Path, help="Replay and compare a complete report")
    args = parser.parse_args()

    if args.verify_report is not None:
        ok = verify_saved_report(args.verify_report.read_bytes())
        print("REPORT MATCH" if ok else "REPORT MISMATCH")
        raise SystemExit(0 if ok else 1)
    if args.window is None and args.ratio is None:
        print(json.dumps(run_cases(), indent=2))
    else:
        if args.window is not None:
            report = run_verification(CHECK, {"window": args.window.read_bytes()})
        else:
            report = run_verification(NSRW_CHECK, {"ratio": args.ratio.read_bytes()})
        print(json.dumps(report, indent=2))
        raise SystemExit({"PASS": 0, "FAIL": 1, "UNRESOLVED": 2}.get(report["status"], 3))
