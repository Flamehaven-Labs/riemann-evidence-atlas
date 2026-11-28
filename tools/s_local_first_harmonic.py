"""Certify the first conjugate pair in the fixed lower-gate trace expansion."""

import argparse
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path

from flint import acb, arb, arb_mat, ctx

import s_local_dual_gram as dual
import s_local_incoming as incoming
import s_local_primal as primal
import s_local_projection_upper as projection


GRAM = "docs/masullo/s-local-dual-gram-160.json"
CONSTANT = "docs/masullo/s-local-incoming-160.json"
CERTIFICATES = {
    GRAM: primal.DUAL_SHA256,
    CONSTANT: "0e7de63b5f21263669164d53f84ed703152182314d1bb64a420039ce272c5d6e",
}
DYADIC_TERMS = 4
BUDGET = "0.7551450173"


def complex_integral(function, a: arb, b: arb) -> acb:
    # Affine substitution lets the integrator use exact path endpoints.
    width = b - a
    result = width * acb.integral(
        lambda s, analytic: function(a + width * s, analytic), 0, 1,
        abs_tol=arb(2)**-35, rel_tol=arb(2)**-34, eval_limit=100000, depth_limit=35,
    )
    if not result.is_finite():
        raise ValueError(f"could not enclose integral on [{a}, {b}]")
    return result


def phase(x: acb, analytic: bool) -> acb:
    return (acb(0, arb.pi()) * (x / 4).log(analytic=analytic)).exp()


def incoming_phase(x: acb, analytic: bool) -> acb:
    return phase(x, analytic) / x.sqrt(analytic=analytic)


def cosine_packet(x: acb, lo: arb, hi: arb) -> acb:
    pi = arb.pi()
    return ((2 * pi * hi * x).sin() - (2 * pi * lo * x).sin()) / (pi * x)


def first_coefficient(count: int) -> tuple[arb, arb, arb, arb]:
    """Monotone rectangles for the centered bump and its first cosine moment."""
    h_sum, cosine_sum = arb(0), arb(0)
    pi = arb.pi()
    for i in range(1, count):
        s = arb(i) / (4 * count)
        u = 2 - 32 * s**2
        if u >= 1:
            h = arb(1)
        elif 0 < u < 1:
            h = 1 / (1 + (1/u - 1/(1-u)).exp())
        else:
            raise ValueError("unexpected G1 transition sample")
        h_sum += h
        cosine_sum += h * (pi*s).cos()
    measure = arb(1) / (2 * incoming.PERIOD * count)
    c0_lo, c0_hi = measure * h_sum / 4, measure * (1 + h_sum) / 4
    factor = (pi**2 + arb(1)/4) * measure
    return factor * cosine_sum, factor * (1 + cosine_sum), c0_lo, c0_hi


def outgoing_dual(a: arb, b: arb, dyadic: bool, gram: dict) -> arb:
    pairings = []
    count = projection.PACKETS
    for i in range(count):
        lo, hi = 1 + arb(i)/count, 1 + arb(i+1)/count

        def integrand(x: acb, analytic: bool) -> acb:
            packet = cosine_packet(x, lo, hi)
            if dyadic:
                packet -= ((arb.pi()*hi*x).sin() - (arb.pi()*lo*x).sin()) / (arb.pi()*x)
            return incoming_phase(x, analytic) * packet

        pairings.append(complex_integral(integrand, a, b))
    core = arb_mat([[arb(value) for value in line] for line in gram["core_arb"]])
    tail = arb(gram["total_tail_operator_cap_arb"])
    # The real and imaginary components are orthogonal in the quadratic objective.
    gains = [dual.bracket_gain(core, [getattr(p, part) for p in pairings], tail)[0]
             for part in ("real", "imag")]
    return sum(gains, arb(0))


def modulus_lower(pairing: acb, error: arb) -> arb:
    return max(arb(0), (abs(pairing) - error).lower())


def incoming_complement(a: arb, b: arb, dyadic: bool) -> tuple[arb, list[dict]]:
    """Remove certified energy from the complement of the flat lower gate."""
    pi = arb.pi()
    oscillatory_boundary = (a**(-arb(3)/2) + b**(-arb(3)/2)
                            + (arb(2)/3) * abs(acb(-arb(3)/2, pi))
                            * (a**(-arb(3)/2) - b**(-arb(3)/2)))
    direct_error = (arb(2)**(1-DYADIC_TERMS) / pi) * (a.rsqrt() - b.rsqrt())
    gain = arb(0)
    rows = []
    for k in range(-incoming.LOWER_GATE, 1):
        lo, hi = arb(2)**k, arb(2)**(k+1)

        def integrand(x: acb, analytic: bool) -> acb:
            if not dyadic:
                return incoming_phase(x, analytic) * cosine_packet(x, lo, hi)
            finite = sum((cosine_packet(x*2**j, lo, hi) for j in range(DYADIC_TERMS+1)), acb(0))
            return incoming_phase(x, analytic) * (finite - cosine_packet(x/2, lo, hi)) / 2

        pairing = complex_integral(integrand, a, b)
        error = arb(0)
        if dyadic:
            by_parts = oscillatory_boundary * (1/lo + 1/hi) / (12*pi**2 * 4**DYADIC_TERMS)
            error = by_parts if by_parts < direct_error else direct_error
        reduction = modulus_lower(pairing, error)**2 / (hi-lo)
        gain += reduction
        rows.append({"left": str(lo), "right": str(hi), "pairing_real_arb": str(pairing.real),
                     "pairing_imag_arb": str(pairing.imag), "pairing_tail_cap_arb": str(error),
                     "energy_lower_bound_arb": str(reduction)})
    return gain, rows


def triangle_trial(a: arb, b: arb, dyadic: bool, weight_scale: arb, weighted: bool) -> tuple[acb, arb]:
    band = arb(2)**-incoming.LOWER_GATE
    pi = arb.pi()
    last = DYADIC_TERMS if dyadic else 0
    beta = -arb(1)/4 if b <= 4 else arb(1)/4
    if not (b <= 4 or a >= 4):
        raise ValueError("split the pairing at the weight seam")

    def integrand(x: acb, analytic: bool) -> acb:
        value = band * sum(((pi*band*x*2**j).sinc()**2 for j in range(last+1)), acb(0))
        result = value * incoming_phase(x, analytic)
        if weighted:
            s = (x/4).log(analytic=analytic)
            result *= (beta*s).exp() * (1+s**2) / weight_scale
        return result

    pairing = complex_integral(integrand, a, b)
    tail = arb(0)
    if dyadic:
        pointwise = 1 / (3*pi**2 * band * 4**last)
        tail = pointwise * (arb(2)/3) * (a**(-arb(3)/2) - b**(-arb(3)/2))
        if weighted:
            log_edge = abs(((a if b <= 4 else b)/4).log())
            tail *= (log_edge/4).exp() * (1+log_edge**2) / weight_scale
    return pairing, tail


def certify(precision: int, subdivisions: int) -> dict:
    ctx.prec = precision
    sources = ("tools/s_local_first_harmonic.py", "tools/s_local_dual_gram.py", "tools/s_local_primal.py",
               "tools/s_local_incoming.py", "tools/s_local_projection_upper.py", "tests/lean/E2AGeometricTraceTest.lean")
    inputs = {name: sha256((primal.ROOT / name).read_bytes()).hexdigest() for name in (*sources, *CERTIFICATES)}
    if (inputs[sources[-1]] != projection.G1_SOURCE_SHA256
            or any(inputs[name] != value for name, value in CERTIFICATES.items())):
        raise ValueError("an input source or certificate differs from its pin")
    gram, constant = [json.loads((primal.ROOT / path).read_bytes()) for path in CERTIFICATES]
    c_lo, c_hi, c0_lo, c0_hi = first_coefficient(subdivisions)
    length = arb(4).log() + arb(1)/2
    scale = arb(2).sqrt() * (1 + arb(4).log()**2)
    if not (length < incoming.PERIOD and 0 < c_lo < c_hi):
        raise ValueError("invalid Fourier coefficient or period")
    rows, total = {}, arb(0)
    for window, endpoints in projection.WINDOWS.items():
        rows[window] = {}
        a, b = map(arb, endpoints)
        j_lo, j_hi = a*(-arb(1)/4).exp()/2, b*(arb(1)/4).exp()/2
        ambient_out = projection.weighted_row_norm_sq(a, b, scale)
        for place in ("real", "real_and_two"):
            print(f"Enclosing first harmonic for {window}, {place}", flush=True)
            dyadic = place == "real_and_two"
            norm = arb(constant["rows"][window][place]["trial_norm_sq_upper_expression_arb"])
            if not norm > 0:
                raise ValueError("the pinned trial norm has no positive denominator")
            p_out, error_out = triangle_trial(a, b, dyadic, scale, weighted=True)
            p_in, error_in = triangle_trial(j_lo, j_hi, dyadic, scale, weighted=False)
            g_out = modulus_lower(p_out, error_out)**2 / norm
            g_in = modulus_lower(p_in, error_in)**2 / norm
            out_dual = outgoing_dual(a, b, dyadic, gram["gram"][place])
            in_dual, in_packets = incoming_complement(j_lo, j_hi, dyadic)
            eta_out = ambient_out - out_dual - g_out
            eta_in = scale*(length-in_dual) - g_in
            if not (eta_out > 0 and eta_in > 0):
                raise ValueError("inconsistent residual bounds")
            term = 2*c_hi*(eta_out*eta_in).sqrt()
            total += term
            rows[window][place] = {
                "outgoing_ambient_norm_sq_arb": str(ambient_out),
                "outgoing_dual_gain_lower_expression_arb": str(out_dual),
                "outgoing_primal_gain_lower_expression_arb": str(g_out),
                "incoming_flat_complement_gain_lower_expression_arb": str(in_dual),
                "incoming_flat_complement_packets": in_packets,
                "incoming_primal_gain_lower_expression_arb": str(g_in),
                "triangle_trial_norm_sq_upper_expression_arb": str(norm),
                "triangle_trial_pairing_real_imag_arb": {
                    "outgoing": [str(p_out.real), str(p_out.imag)], "incoming": [str(p_in.real), str(p_in.imag)]},
                "triangle_trial_pairing_tail_caps_arb": [str(error_out), str(error_in)],
                "outgoing_residual_norm_sq_upper_expression_arb": str(eta_out),
                "incoming_residual_norm_sq_upper_expression_arb": str(eta_in),
                "conjugate_pair_trace_error_upper_expression_arb": str(term),
            }
    budget = arb(BUDGET)
    outcome = "FITS" if total < budget else "BOUND_EXCEEDS_BUDGET" if total > budget else "UNRESOLVED"
    if any(sha256((primal.ROOT / name).read_bytes()).hexdigest() != value for name, value in inputs.items()):
        raise ValueError("an input changed during certification")
    return {
        "evidence": "norm-product bounds on both first-harmonic terms of the fixed lower-gate trace",
        "level": 4, "alpha": "1/8", "cells": primal.CELLS, "period": incoming.PERIOD, "gate": "1/16",
        "coefficient_rectangle_count": subdivisions, "arb_precision_bits": precision,
        "coefficient_magnitude_lower_expression_arb": str(c_lo),
        "coefficient_magnitude_upper_expression_arb": str(c_hi),
        "coefficient_ratio_lower_expression_arb": str(c_lo/c0_hi),
        "coefficient_ratio_upper_expression_arb": str(c_hi/c0_lo),
        "incoming_flat_norm_sq_arb": str(length), "weight_normalization_arb": str(scale),
        "four_conjugate_pair_errors_upper_expression_arb": str(total),
        "remaining_budget_scale": BUDGET, "norm_product_budget_result": outcome,
        "python_flint_version": version("python-flint"), "source_sha256": inputs, "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precision", type=int, default=106)
    parser.add_argument("--subdivisions", type=int, default=1024)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    if args.precision < 80 or args.subdivisions < 16 or args.subdivisions & (args.subdivisions-1):
        parser.error("require precision >= 80 and a power-of-two subdivision count >= 16")
    report = certify(args.precision, args.subdivisions)
    with args.report.open("x", encoding="utf-8", newline="\n") as out:
        out.write(json.dumps(report, sort_keys=True, indent=2) + "\n")


if __name__ == "__main__":
    main()
