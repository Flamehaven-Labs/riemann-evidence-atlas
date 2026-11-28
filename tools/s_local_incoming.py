"""Certify the constant incoming rows and the corresponding trace error terms."""

import argparse
from fractions import Fraction
from hashlib import sha256
from importlib.metadata import version
import json
from math import ceil, floor
from pathlib import Path

from flint import acb, arb, ctx

import s_local_primal as primal
import s_local_projection_upper as projection


CERTIFICATES = {
    "docs/masullo/s-local-primal-106.json": "3a12c7de6a2acb25a91f1c7ae85bdab7b83e93527463f5d784902dd5aa9c567f",
    "docs/masullo/s-local-dual-gram-160.json": primal.DUAL_SHA256,
}
PERIOD = 2
LOWER_GATE = 4
FIRST_FREQUENCY_POWER = -24
FIRST_TRIAL_POWER = -22
LAST_TRIAL_POWER = 9


def squared_mass(frequency_lower: arb, frequency_upper: arb, dyadic: bool,
                 depth: int, flat_norm_sq: arb) -> tuple[arb, arb]:
    """Upper bound the exact flat low-gate energy using a localized dyadic tail."""
    pi = arb.pi()
    amplitude = 4 * (frequency_upper.sqrt() - frequency_lower.sqrt())
    decay = 2 / (pi * frequency_lower.sqrt())
    cutoff = arb(2)**FIRST_FREQUENCY_POWER
    if dyadic:
        near_p = amplitude * (2 - arb(FIRST_FREQUENCY_POWER)) / 2 + decay
        near_q = amplitude / (2 * arb(2).log())
        near = cutoff * (near_p**2 + 2 * near_p * near_q + 2 * near_q**2)
    else:
        near = cutoff * amplitude**2

    def cosine(x: acb, analytic: bool) -> acb:
        lo = (frequency_lower * x).sqrt(analytic=analytic)
        hi = (frequency_upper * x).sqrt(analytic=analytic)
        return 2 * ((2 * hi).fresnel_c() - (2 * lo).fresnel_c()) / x.sqrt(analytic=analytic)

    total = near
    for power in range(FIRST_FREQUENCY_POWER, -LOWER_GATE):
        lo = arb(2)**power
        last = depth - power

        def finite(x: acb, analytic: bool) -> acb:
            if not dyadic:
                return cosine(x, analytic)
            value = sum((cosine(x * 2**j, analytic) for j in range(last + 1)), acb(0))
            return (value - cosine(x / 2, analytic)) / 2

        core = primal.integrate(lambda x, analytic: finite(x, analytic)**2, lo, 2 * lo)
        omitted = (decay / 2**(last + 1))**2 / (2 * lo) if dyadic else arb(0)
        total += (core.upper().sqrt() + omitted.sqrt())**2
    return (total if total < flat_norm_sq else flat_norm_sq), near


def trial_norm(dyadic: bool, weight_scale: arb) -> tuple[arb, arb, arb]:
    """Upper bound the weighted norm of the in-band triangular-spectrum trial."""
    band = arb(2)**-LOWER_GATE
    pi = arb.pi()
    beta = arb(1) / 4
    decay = 1 / (pi**2 * band)
    core = arb(0)
    for power in range(FIRST_TRIAL_POWER, LAST_TRIAL_POWER):
        lo = arb(2)**power
        last = max(0, 7 - power) if dyadic else 0
        exponent = -beta if power < 2 else beta

        def integrand(x: acb, analytic: bool) -> acb:
            value = band * sum(((pi * band * x * 2**j).sinc()**2
                                for j in range(last + 1)), acb(0))
            log_x = (x / 4).log(analytic=analytic)
            return value**2 * (exponent * log_x).exp() * (1 + log_x**2) / weight_scale

        finite = primal.integrate(integrand, lo, 2 * lo)
        # Bound the tail on this panel using its extreme weight and the integral of x^-4.
        edge = lo if power < 2 else 2 * lo
        s = abs((edge / 4).log())
        maximum_weight = (beta * s).exp() * (1 + s**2) / weight_scale
        omitted = ((4 * decay / (3 * 4**(last + 1)))**2 * maximum_weight
                   * lo**-3 * (arb(7) / 24)) if dyadic else arb(0)
        core += (finite.upper().sqrt() + omitted.sqrt())**2

    a, radius = arb(2)**FIRST_TRIAL_POWER, arb(2)**LAST_TRIAL_POWER
    left_log, right_log = (4 / a).log(), (radius / 4).log()
    p = band * (1 - FIRST_TRIAL_POWER) + 4 * decay / 3 if dyadic else band
    q = band / arb(2).log() if dyadic else arb(0)
    near = (a * (beta * left_log).exp() / weight_scale
            * primal.exponential_moment(left_log, 1 - beta, p, q))
    d = decay * (arb(4) / 3 if dyadic else 1)
    far = (d**2 * radius**-3 * (beta * right_log).exp() / weight_scale
           * primal.exponential_moment(right_log, 3 - beta, arb(1), arb(0)))
    return core + near + far, near, far


def trial_pairing(a: arb, b: arb, dyadic: bool) -> tuple[arb, arb, arb]:
    # The real integrand is nonnegative. Exact inner endpoints give a lower bound.
    denominator = 2**20
    lo = arb(ceil(float(a.upper() * denominator)) + 1) / denominator
    hi = arb(floor(float(b.lower() * denominator)) - 1) / denominator
    if not a < lo < hi < b:
        raise ValueError("failed to certify inner endpoints for the pairing")
    band = arb(2)**-LOWER_GATE
    pi = arb.pi()

    def integrand(x: acb, analytic: bool) -> acb:
        value = sum(((pi * band * x * 2**j).sinc()**2
                     for j in range(5 if dyadic else 1)), acb(0))
        return band * value / x.sqrt(analytic=analytic)

    return primal.integrate(integrand, lo, hi), lo, hi


def constant_coefficient() -> tuple[arb, arb]:
    """Enclose the magnitude of c_0 by monotonic rectangles for the G1 bump."""
    count = 512
    integral = arb(0)
    for i in range(1, count):
        s = arb(i) / (4 * count)
        u = 2 - 32 * s**2
        if u >= 1:
            integral += 1
        elif 0 < u < 1:
            # The normalized exponential formula equals smoothTransition on (0,1).
            integral += 1 / (1 + (1 / u - 1 / (1 - u)).exp())
        else:
            raise ValueError("unexpected G1 transition argument")
    return integral / (8 * PERIOD * count), (1 + integral) / (8 * PERIOD * count)


def certify(precision: int, depth: int) -> dict:
    ctx.prec = precision
    inputs = {}
    for name in ("tools/s_local_incoming.py", "tools/s_local_primal.py",
                 "tools/s_local_projection_upper.py", "tests/lean/E2AGeometricTraceTest.lean", *CERTIFICATES):
        inputs[name] = sha256((primal.ROOT / name).read_bytes()).hexdigest()
    if (inputs["tests/lean/E2AGeometricTraceTest.lean"] != projection.G1_SOURCE_SHA256
            or any(inputs[name] != digest for name, digest in CERTIFICATES.items())):
        raise ValueError("an input certificate or source does not match its pin")
    outgoing, dual = [json.loads((primal.ROOT / name).read_bytes())["rows"] for name in CERTIFICATES]
    log_four = arb(4).log()
    scale = (log_four / 4).exp() * (1 + log_four**2)
    j_length = log_four + arb(1) / 2
    if not j_length < PERIOD:
        raise ValueError("the period would overlap the translated G1 support")
    c_lo, c_hi = constant_coefficient()
    norm_bounds = {key: trial_norm(dyadic, scale)
                   for key, dyadic in (("real", False), ("real_and_two", True))}
    rows = {}
    total = arb(0)
    for window, (left, right) in projection.WINDOWS.items():
        a = arb(left) * (-arb(1) / 4).exp() / 2
        b = arb(right) * (arb(1) / 4).exp() / 2
        rows[window] = {}
        for place in ("real", "real_and_two"):
            print(f"Enclosing incoming row for {window}, {place}", flush=True)
            dyadic = place == "real_and_two"
            flat_energy, near_frequency = squared_mass(a, b, dyadic, depth, j_length)
            ambient = scale * flat_energy
            pairing, lo, hi = trial_pairing(a, b, dyadic)
            norm, near, far = norm_bounds[place]
            if not pairing > 0 or not norm > 0:
                raise ValueError("the one-vector primal reduction was not certified positive")
            primal_gain = pairing**2 / norm
            incoming_cap = ambient - primal_gain
            source_row = outgoing[window][place]
            if window == "outer" and dyadic:
                t = arb(79) / 128
                p = arb(source_row["finite_pairing_arb"]) - arb(source_row["pairing_theta_error_upper_expression_arb"])
                n = arb(source_row["norm_sq_upper_expression_arb"])
                out_lower = 2*t*p - t*t*n
                outgoing_cap = arb(dual[window][place]["projected_norm_sq_upper_expression_arb"]) - out_lower
            else:
                outgoing_cap = arb(source_row["residual_norm_sq_upper_expression_arb"])
            if not (incoming_cap > 0 and outgoing_cap > 0):
                raise ValueError("invalid residual bounds")
            term = c_hi * (outgoing_cap * incoming_cap).sqrt()
            total += term
            rows[window][place] = {
                "incoming_support_arb": [str(a), str(b)],
                "incoming_pairing_inner_interval_arb": [str(lo), str(hi)],
                "flat_energy_upper_expression_arb": str(flat_energy),
                "flat_energy_near_frequency_cap_arb": str(near_frequency),
                "trial_pairing_lower_expression_arb": str(pairing),
                "trial_norm_sq_upper_expression_arb": str(norm),
                "trial_norm_sq_near_cap_arb": str(near),
                "trial_norm_sq_far_cap_arb": str(far),
                "incoming_primal_gain_lower_expression_arb": str(primal_gain),
                "incoming_residual_norm_sq_upper_expression_arb": str(incoming_cap),
                "outgoing_residual_norm_sq_upper_expression_arb": str(outgoing_cap),
                "constant_rank_one_error_upper_expression_arb": str(term),
            }
    if any(sha256((primal.ROOT / name).read_bytes()).hexdigest() != digest for name, digest in inputs.items()):
        raise ValueError("a bound input changed during certification")
    return {"evidence": "constant Fourier term in fixed lower-gate unpolarized trace compression",
            "level": 4, "alpha": "1/8", "cells": primal.CELLS, "period": PERIOD, "gate": "1/16",
            "arb_precision_bits": precision, "spectral_dilation_depth": depth,
            "constant_coefficient_magnitude_lower_expression_arb": str(c_lo),
            "constant_coefficient_magnitude_upper_expression_arb": str(c_hi),
            "four_constant_rank_one_errors_upper_expression_arb": str(total),
            "rows": rows, "source_sha256": inputs, "python_flint_version": version("python-flint")}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precision", type=int, default=106)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    if args.precision < 80 or args.depth < 0:
        parser.error("require precision >= 80 and nonnegative depth")
    report = certify(args.precision, args.depth)
    with args.report.open("x", encoding="utf-8", newline="\n") as out:
        out.write(json.dumps(report, sort_keys=True, indent=2) + "\n")


if __name__ == "__main__":
    main()
