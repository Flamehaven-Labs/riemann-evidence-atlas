"""Enclose four 128-cell primal trial objectives in the fixed S-local model."""

import argparse
from fractions import Fraction
from hashlib import sha256
from importlib.metadata import version
import json
from math import factorial
from pathlib import Path

from flint import acb, acb_poly, arb, ctx

import s_local_projection_upper as projection


CELLS = 128
SCALE = 2**40
LEFT_POWER = -28
ROOT = Path(__file__).resolve().parents[1]
DUAL_PATH = ROOT / "docs/masullo/s-local-dual-gram-160.json"
DUAL_SHA256 = "7620c8086921ae466d179211526fc6f5f8e63a04a14cabbe5366d4cc95041c4f"


def propose_trials() -> dict:
    """Use the existing Galerkin quadrature only to select trial coefficients."""
    import numpy as np
    import s_local_low_galerkin as galerkin

    basis = galerkin.hat_basis(CELLS, 1 / 16)
    if not np.array_equal(basis.edges, np.arange(CELLS + 1) / CELLS):
        raise ValueError("the Galerkin mesh is not the expected uniform dyadic mesh")
    x, w = galerkin.radius_quadrature(2.0**-30, 512, 0.25, 7)
    weights = w * galerkin.weighted_measure(x, 4, 0.125)
    result = {window: {} for window in projection.WINDOWS}
    for places, dyadic in (("real", False), ("real_and_two", True)):
        values = galerkin.physical(basis, x, dyadic, 1024)
        gram = galerkin.weighted_gram(values, weights)
        for window, (a, b) in projection.WINDOWS.items():
            s, v = galerkin.radius_quadrature(float(Fraction(a)), float(Fraction(b)), 0.25, 7)
            pairing = galerkin.physical(basis, s, dyadic, 1024).T @ (
                v * galerkin.weighted_measure(s, 4, 0.125) / np.sqrt(s))
            result[window][places] = [round(float(c) * SCALE) for c in np.linalg.solve(gram, pairing)]
    return result


def integrate(integrand, lo: arb, hi: arb) -> arb:
    enclosed = acb.integral(
        integrand, lo, hi, abs_tol=arb(2)**-20, rel_tol=arb(2)**-20,
        eval_limit=100000, depth_limit=35,
    )
    if not enclosed.is_finite() or not enclosed.imag.contains(0):
        raise ValueError(f"failed to enclose a real integral on [{lo}, {hi}]")
    return enclosed.real


def exponential_moment(t: arb, decay: arb, p: arb, q: arb) -> arb:
    """Integrate (1+(t+r)^2)(p+q*r)^2 against exp(-decay*r), r >= 0."""
    coefficients = [p*p, 2*p*q, q*q]
    return sum((a * b * factorial(i + j) / decay**(i + j + 1)
                for i, a in enumerate((1 + t*t, 2*t, arb(1)))
                for j, b in enumerate(coefficients)), arb(0))


def objective(numerators: list[int], window: tuple[str, str], dyadic: bool,
              right_power: int, theta_power: int, weight_scale: arb) -> dict:
    if len(numerators) != CELLS or any(type(c) is not int for c in numerators):
        raise ValueError("expected exactly 128 integer trial numerators")
    values = [arb(c) / SCALE for c in numerators] + [arb(0)]
    slopes = [CELLS * (b - a) for a, b in zip(values, values[1:])]
    jumps = [-slopes[0]] + [a - b for a, b in zip(slopes, slopes[1:])] + [slopes[-1]]
    pi = arb.pi()
    angular = 2 * pi / CELLS
    factor = 2 * pi**2
    cosine_polynomial = acb_poly(jumps)
    # The first nine coefficients of f as a polynomial in x squared.
    taylor = [(-1)**k * angular**(2*k) *
              sum((v * i**(2*k) for i, v in enumerate(jumps)), arb(0))
              / (factor * factorial(2*k)) for k in range(1, 10)]
    l1 = (abs(values[0]) + 2 * sum(map(abs, values[1:]), arb(0))) / CELLS
    sup = sum(map(abs, jumps), arb(0)) / factor
    mean_square = (jumps[0]**2 + sum((v**2 for v in jumps[1:]), arb(0)) / 2) / factor**2
    beta = arb(1) / 4
    row_a, row_b = map(arb, window)
    core_sq, pairing, core_error_sq, row_error_sq = (arb(0) for _ in range(4))

    for power in range(LEFT_POWER, right_power):
        lo = arb(2)**power
        hi = 2 * lo
        exponent = -beta if power < 2 else beta
        last = max(0, theta_power - power) if dyadic else 0
        small = max(0, -3 - power) if dyadic else 0
        if small:
            small_scale = arb(2)**(small - 1)
            small_series = acb_poly([
                coefficient * (small if k == 0 else (1 - arb(4)**(-k*small)) / (1 - arb(4)**-k))
                for k, coefficient in enumerate(taylor)
            ])

        def profile(x: acb) -> acb:
            phase_argument = acb(0, angular) * (2**small * x)
            phase = phase_argument.exp()
            inverse = (-phase_argument).exp()
            total = acb(0)
            scale = 4**small
            for index in range(small, last + 1):
                total += (cosine_polynomial(phase) + cosine_polynomial(inverse)) / scale
                if index < last:
                    phase = phase**2
                    inverse = inverse**2
                    scale *= 4
            result = total / (2 * factor * x**2)
            return result + small_series((small_scale * x)**2) if small else result

        def density(x: acb, analytic: bool) -> acb:
            t = (x / 4).log(analytic=analytic)
            return (exponent * t).exp() * (1 + t*t) / weight_scale

        core_sq += integrate(lambda x, analytic: profile(x)**2 * density(x, analytic), lo, hi)
        inside = row_a <= lo and hi <= row_b
        if inside:
            pairing += integrate(
                lambda x, analytic: profile(x) * density(x, analytic) / x.sqrt(analytic=analytic), lo, hi
            )
        if dyadic:
            # The full omitted profile is bounded by the sum of a geometric series.
            first_omitted = arb(2)**(last + 1)
            t_lo, t_hi = (lo / 4).log(), (hi / 4).log()
            log_max = abs(t_lo) if power < 2 else abs(t_hi)
            weight_max = (beta * log_max).exp() * (1 + log_max**2) / weight_scale
            missing = (4 * sup / (3 * first_omitted**2))**2
            squared_cap = missing * weight_max * (lo**-3 - hi**-3) / 3
            if power + last + 1 >= 7:
                # All omitted dilations traverse an integer number of periods.
                mean_cap = (4 / (3 * first_omitted**2))**2 * mean_square * weight_max * lo**-3
                if mean_cap < squared_cap:
                    squared_cap = mean_cap
            if small:
                uniform_error = l1 * (pi / 4)**18 / (factorial(18) * (1 - arb(2)**-18))
                squared_cap = (squared_cap.sqrt() + uniform_error * (weight_max * lo).sqrt())**2
            core_error_sq += squared_cap
            if inside:
                row_error_sq += squared_cap

    a, radius = arb(2)**LEFT_POWER, arb(2)**right_power
    log_a, log_radius = (4 / a).log(), (radius / 4).log()
    transition = arb(16)
    if dyadic:
        small_radius = arb(1) / 8
        at_zero = abs(taylor[0])
        p = (at_zero * (1 + (small_radius / a).log() / arb(2).log())
             + 8 * pi**2 * l1 * small_radius**2 / 3 + 7 * l1 + 4 * sup / (3 * transition**2))
        q = at_zero / arb(2).log()
    else:
        p, q = l1, arb(0)
    near_sq = a * (beta * log_a).exp() / weight_scale * exponential_moment(log_a, 1 - beta, p, q)
    weight_radius = (beta * log_radius).exp() * (1 + log_radius**2) / weight_scale
    far_sq = (mean_square * (arb(4) / 3 if dyadic else 1)**2 * weight_radius / radius**4
              * (CELLS + radius / (2 - beta)))
    if not core_sq > 0:
        raise ValueError("the finite core integral did not certify a positive norm")
    norm_upper = (core_sq.sqrt() + core_error_sq.sqrt())**2 + near_sq + far_sq
    row_norm = projection.weighted_row_norm_sq(row_a, row_b, weight_scale)
    pairing_error = (row_error_sq * row_norm).sqrt()
    lower_expression = 2 * (pairing - pairing_error) - norm_upper
    if not lower_expression > 0:
        raise ValueError(f"no positive primal lower bound for {window}: "
                         f"objective {lower_expression}, pairing {pairing}, norm upper {norm_upper}")
    return {
        "trial_numerators": numerators,
        "finite_core_norm_sq_arb": str(core_sq),
        "finite_pairing_arb": str(pairing),
        "core_theta_error_sq_upper_expression_arb": str(core_error_sq),
        "pairing_theta_error_upper_expression_arb": str(pairing_error),
        "near_norm_sq_upper_expression_arb": str(near_sq),
        "far_norm_sq_upper_expression_arb": str(far_sq),
        "norm_sq_upper_expression_arb": str(norm_upper),
        "primal_norm_sq_lower_expression_arb": str(lower_expression),
    }


def certify(precision: int, right_power: int, theta_power: int, trials: dict) -> dict:
    ctx.prec = precision
    paths = ["tools/s_local_primal.py", "tools/s_local_low_galerkin.py",
             "tools/s_local_projection_upper.py", "tools/s_local_dual_gram.py",
             "tests/lean/E2AGeometricTraceTest.lean"]
    inputs = {name: sha256((ROOT / name).read_bytes()).hexdigest() for name in paths}
    dual_bytes = DUAL_PATH.read_bytes()
    if sha256(dual_bytes).hexdigest() != DUAL_SHA256:
        raise ValueError("the dual certificate does not match its pinned hash")
    dual = json.loads(dual_bytes)
    for name, field in ((paths[2], "pairing_source_sha256"), (paths[3], "source_sha256"),
                        (paths[4], "g1_source_sha256")):
        if inputs[name] != dual[field]:
            raise ValueError(f"the dual certificate does not match {name}")
    d = arb(4).log()
    weight_scale = (d / 4).exp() * (1 + d*d)
    rows = {}
    for window, endpoints in projection.WINDOWS.items():
        rows[window] = {}
        for places in ("real", "real_and_two"):
            print(f"Enclosing {window}, {places}", flush=True)
            result = objective(trials[window][places], endpoints, places == "real_and_two",
                               right_power, theta_power, weight_scale)
            cap = arb(dual["rows"][window][places]["projected_norm_sq_upper_expression_arb"])
            residual = cap - arb(result["primal_norm_sq_lower_expression_arb"])
            if not residual > 0:
                raise ValueError("dual and primal bounds are inconsistent")
            result["residual_norm_sq_upper_expression_arb"] = str(residual)
            rows[window][places] = result
            print(f"  Primal lower expression {result['primal_norm_sq_lower_expression_arb']}", flush=True)
    if any(sha256((ROOT / name).read_bytes()).hexdigest() != digest for name, digest in inputs.items()):
        raise ValueError("an input changed during certification")
    return {"evidence": "four primal projection lower bounds and omitted-basis upper bounds",
            "source_sha256": inputs, "dual_report_sha256": DUAL_SHA256, "level": 4, "alpha": "1/8",
            "cells": CELLS, "trial_denominator": SCALE, "flint_precision_bits": precision,
            "python_flint_version": version("python-flint"), "core_power_bounds": [LEFT_POWER, right_power],
            "theta_power": theta_power, "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precision", type=int, default=106)
    parser.add_argument("--right-power", type=int, default=8)
    parser.add_argument("--theta-power", type=int, default=6)
    parser.add_argument("--trials-from", type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    if args.precision < 80 or args.right_power < 6 or args.theta_power < 5:
        parser.error("require precision >= 80, right power >= 6, and theta power >= 5")
    if args.trials_from:
        saved = json.loads(args.trials_from.read_bytes())
        if saved["trial_denominator"] != SCALE:
            raise ValueError("trial denominator mismatch")
        trials = {window: {place: row["trial_numerators"] for place, row in places.items()}
                  for window, places in saved["rows"].items()}
    else:
        trials = propose_trials()
    report = certify(args.precision, args.right_power, args.theta_power, trials)
    with args.report.open("x", encoding="utf-8", newline="\n") as out:
        out.write(json.dumps(report, sort_keys=True, indent=2) + "\n")


if __name__ == "__main__":
    main()
