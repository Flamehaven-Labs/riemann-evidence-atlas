"""Enclose d(1) for the fixed G1 test using FLINT complex ball quadrature."""

import argparse
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path

from flint import acb, arb, ctx


G1_SOURCE_SHA256 = "a3ec4fc5e93c99937315a55144822c477f4a4d7f2d35869b7d2ccb07cdb086c0"


def power_two(exponent: int) -> Fraction:
    return Fraction(2) ** exponent


def finite_coefficients(
    shell_depth: int, negative_depth: int,
) -> dict[tuple[Fraction, int], Fraction]:
    """Collect coefficients of I_(1-q)(2^k) in the finite telescoping sum."""
    coefficients = defaultdict(Fraction)
    for n in range(-negative_depth, shell_depth):
        for sign in (-1, 1):
            q = sign * power_two(-n)
            if n == 0:
                coefficients[q, -1] += 1
                coefficients[q, 0] -= 1
            for k in range(max(0, n), shell_depth):
                mass = power_two(-k-1)
                coefficients[q, k] += mass
                coefficients[q, k-1] -= mass
    return {key: c for key, c in coefficients.items() if c}


def omitted_series_bound(shell_depth: int, negative_depth: int) -> Fraction:
    """Upper bound for the omitted dyadic frequencies and S-units."""
    f_l1 = Fraction(6100)
    k = shell_depth
    bracket = 64 * (2 * k + 1) + Fraction(8, 3) + 24**2
    shells = f_l1 / 6 * power_two(-2*k) * (bracket * Fraction(4, 3) + Fraction(512, 9))
    stationary = Fraction(7, 2) * power_two(-k)
    negative_units = f_l1 / 6 * Fraction(32, 9) * power_two(-2*negative_depth)
    return shells + stationary + negative_units


def as_ball(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def certify() -> dict:
    driver = Path(__file__).resolve()
    proof = driver.parents[1] / "tests/lean/E2AGeometricTraceTest.lean"
    driver_digest = sha256(driver.read_bytes()).hexdigest()
    if sha256(proof.read_bytes()).hexdigest() != G1_SOURCE_SHA256:
        raise ValueError("the fixed G1 proof source differs from the pinned input")

    ctx.prec = 106
    shell_depth = 10
    negative_depth = 8
    epsilon = Fraction(1, 2**32)
    coefficients = finite_coefficients(shell_depth, negative_depth)
    c = arb(2).log()
    e = as_ball(epsilon)
    plateau = 1 / arb(32).sqrt()
    split = arb(3).sqrt() / 8
    segment_balls = [
        (c - arb(1)/4 + e, c - split, "left"),
        (c - split, c - plateau - e, "right"),
        (c - plateau + e, c - e, "flat"),
        (c + e, c + plateau - e, "flat"),
        (c + plateau + e, c + split, "right"),
        (c + split, c + arb(1)/4 - e, "left"),
    ]
    endpoint_rounding_cap = Fraction(1, 2**96)
    segments = []
    endpoint_rounding = arb(0)
    for start, end, portion in segment_balls:
        lo, hi = start.upper(), end.lower()
        if not (lo.is_exact() and hi.is_exact() and lo < hi):
            raise ValueError("invalid dyadic integration segment")
        endpoint_rounding += lo - start.lower() + end.upper() - hi
        segments.append((lo, hi, portion))
    if not endpoint_rounding < as_ball(endpoint_rounding_cap):
        raise ValueError("dyadic endpoint rounding exceeded its bound")
    omitted_length = 8 * epsilon + endpoint_rounding_cap
    pi = arb.pi()
    integral = arb(0)
    omitted_quadrature_cap = Fraction(0)
    for index, ((q, k), coeff) in enumerate(sorted(coefficients.items()), 1):
        radius = power_two(k)
        beta = 2 * pi * as_ball(radius)
        q_ball = as_ball(q)
        for start, end, portion in segments:
            def integrand(t, _analytic):
                if portion == "flat":
                    bump_value = acb(1)
                    bump_d2 = acb(0)
                else:
                    shift = t - c
                    u = 2 - 32 * shift**2
                    v = 1 - u
                    log_odds = -1/u + 1/v
                    ratio = (log_odds if portion == "left" else -log_odds).exp()
                    denominator = 1 + ratio
                    bump_value = (ratio if portion == "left" else 1) / denominator
                    variance = ratio / denominator**2
                    dlog = 1/u**2 + 1/v**2
                    d2log = -2/u**3 + 2/v**3
                    bump_d2 = variance * (
                        ((1-2*bump_value)*dlog**2+d2log) * (64*shift)**2 - 64*dlog
                    )
                y = (-t).exp() - q_ball
                sine_kernel = (beta*y).si() / (pi*y)
                return (bump_d2-bump_value/4)*(-t/2).exp()*sine_kernel
            result = acb.integral(
                integrand, start, end, abs_tol=arb(2)**-18, rel_tol=arb(2)**-20,
                eval_limit=120000, depth_limit=38,
            )
            if not result.is_finite():
                raise ValueError(f"quadrature did not enclose q={q}, k={k}, region={portion}")
            integral += as_ball(coeff) * result.real
        omitted_quadrature_cap += abs(coeff) * radius * 2 * 41000 * omitted_length
        if index % 50 == 0:
            print(f"Enclosed {index}/{len(coefficients)} real kernels", flush=True)

    series_cap = omitted_series_bound(shell_depth, negative_depth)
    total_cap = as_ball(series_cap + omitted_quadrature_cap)
    d1 = integral + arb(0, total_cap.upper())
    one_sided = -arb(2).log() / (4*arb(2).sqrt())
    balanced_limit = one_sided - 2 * d1
    if not balanced_limit > 0:
        raise ValueError(f"certified band has not separated the threshold: {balanced_limit}")
    if not (d1 > -arb(663)/100 and d1 < -arb(14)/10
            and balanced_limit > arb(268)/100 and balanced_limit < arb(1314)/100):
        raise ValueError("the result does not fit the recorded rational enclosures")
    if (sha256(driver.read_bytes()).hexdigest() != driver_digest
            or sha256(proof.read_bytes()).hexdigest() != G1_SOURCE_SHA256):
        raise ValueError("an input changed during the quadrature replay")
    return {
        "status": "POSITIVE_BALANCED_UNFOLDED_LIMIT",
        "cutoff_input_A": 1,
        "shell_depth": shell_depth,
        "negative_s_unit_depth": negative_depth,
        "retained_kernels": len(coefficients),
        "endpoint_trim": str(epsilon),
        "endpoint_rounding_total_cap": str(endpoint_rounding_cap),
        "omitted_series_error": str(series_cap),
        "omitted_endpoint_error": str(omitted_quadrature_cap),
        "finite_integral_arb": str(integral),
        "d1_arb": str(d1),
        "d1_rational_enclosure": ["-663/100", "-14/10"],
        "balanced_limit_arb": str(balanced_limit),
        "balanced_limit_lower": str(balanced_limit.lower()),
        "balanced_limit_upper": str(balanced_limit.upper()),
        "balanced_limit_rational_enclosure": ["268/100", "1314/100"],
        "flint_precision_bits": ctx.prec,
        "python_flint_version": version("python-flint"),
        "quadrature_source_sha256": driver_digest,
        "proof_source_sha256": G1_SOURCE_SHA256,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    payload = json.dumps(certify(), sort_keys=True, indent=2) + "\n"
    if args.report:
        with args.report.open("x", encoding="utf-8", newline="\n") as report:
            report.write(payload)
    print(payload, end="")


if __name__ == "__main__":
    main()
