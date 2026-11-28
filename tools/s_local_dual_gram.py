"""Enclose the weighted Gram matrix of the sixteen exterior frequency packets."""

import argparse
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path

from flint import acb, arb, arb_mat, ctx

import s_local_projection_upper as reference


BETA = "1/4"
LEFT_RADIUS = "1/4096"
PERIOD = 32


def sine_coefficients(index: int, dyadic: bool) -> list[tuple[int, int]]:
    a, b = reference.PACKETS + index, reference.PACKETS + index + 1
    terms = [(2 * b, 1), (2 * a, -1)]
    if dyadic:
        terms.extend([(b, -1), (a, 1)])
    return terms


def gram_core(radius: int, weight_scale: arb) -> tuple[arb_mat, arb_mat, dict]:
    """Integrate scalar cosine moments and assemble both symmetric Gram matrices."""
    count = reference.PACKETS
    beta = arb(BETA)
    left = arb(LEFT_RADIUS)
    seam = arb(4)
    moments = {0: arb(0)}

    def moment(index: int) -> arb:
        if index not in moments:
            coefficient = arb(index) / PERIOD
            angular = arb.pi() * coefficient
            value = arb(0)
            for lo, hi, exponent in ((left, seam, beta), (seam, arb(radius), -beta)):
                def integrand(x: acb, analytic: bool) -> acb:
                    log_x = (x / seam).log(analytic=analytic)
                    return (weight_scale * (exponent * log_x).exp()
                            * (angular * x).sinc()**2 * (2 * coefficient**2)
                            / (1 + log_x**2))

                enclosure = acb.integral(
                    integrand, lo, hi, abs_tol=arb(2)**-68, rel_tol=arb(2)**-60,
                    eval_limit=200000, depth_limit=40,
                )
                if not enclosure.is_finite() or not enclosure.imag.contains(0):
                    raise ValueError(f"could not enclose cosine moment {index} on [{lo}, {hi}]")
                value += enclosure.real
            moments[index] = value
        return moments[index]

    def assemble(dyadic: bool) -> arb_mat:
        coefficients = [sine_coefficients(i, dyadic) for i in range(count)]
        result = arb_mat(count, count)
        for i, a in enumerate(coefficients):
            for j in range(i, count):
                entry = sum((s * t * (moment(m + n) - moment(abs(m - n)))
                             for m, s in a for n, t in coefficients[j]), arb(0)) / 2
                result[i, j] = entry
                result[j, i] = entry
        return result

    real = assemble(False)
    dyadic = assemble(True)
    return real, dyadic, {str(k): str(v) for k, v in sorted(moments.items())}


def tail_caps(radius: int, weight_scale: arb, dyadic: bool) -> tuple[arb, arb]:
    """Return operator bounds for the omitted positive semidefinite Gram terms."""
    count = reference.PACKETS
    beta = arb(BETA)
    left, right = arb(LEFT_RADIUS), arb(radius)
    packet_value = arb(3 if dyadic else 2) / count
    near = (count * packet_value**2 * weight_scale / arb(4)**beta
            * left**(1 + beta) / ((1 + beta) * (1 + (left / 4).log()**2)))
    right_density = (weight_scale * arb(4)**beta / arb.pi()**2
                     * right**(-2 - beta) / (1 + (right / 4).log()**2))
    # Average squared trigonometric numerator on any interval of length 32.
    period_average_cap = 8 if dyadic else 2
    far = period_average_cap * right_density * (PERIOD + right / (1 + beta))
    return near, far


def bracket_gain(core: arb_mat, pairing: list[arb], cap: arb) -> tuple[arb, arb]:
    count = len(pairing)
    b = arb_mat(count, 1, pairing)
    enlarged = arb_mat(core)
    for j in range(count):
        enlarged[j, j] += cap
    lower = (b.transpose() * enlarged.solve(b))[0, 0]
    upper = (b.transpose() * core.solve(b))[0, 0]
    if not (lower.is_finite() and upper.is_finite() and 0 < lower <= upper):
        raise ValueError("the interval solves did not separate the two gain bounds")
    return lower, upper


def certify(precision: int, radius: int) -> dict:
    ctx.prec = precision
    source = Path(__file__).resolve()
    reference_source = Path(reference.__file__).resolve()
    proof = source.parents[1] / "tests/lean/E2AGeometricTraceTest.lean"
    inputs = {path: sha256(path.read_bytes()).hexdigest()
              for path in (source, reference_source, proof)}
    if inputs[proof] != reference.G1_SOURCE_SHA256:
        raise ValueError("the fixed G1 source differs from the pinned input")
    d = arb(4).log()
    weight_scale = (d / 4).exp() * (1 + d**2)
    real, two, moments = gram_core(radius, weight_scale)
    rows, grams = {}, {}
    count = reference.PACKETS
    for places, core, dyadic in (("real", real, False), ("real_and_two", two, True)):
        near, far = tail_caps(radius, weight_scale, dyadic)
        cap = near + far
        grams[places] = {
            "core_arb": [[str(core[i, j]) for j in range(count)] for i in range(count)],
            "near_tail_operator_cap_arb": str(near),
            "far_tail_operator_cap_arb": str(far),
            "total_tail_operator_cap_arb": str(cap),
        }
        for window, (lo, hi) in reference.WINDOWS.items():
            a, b = arb(lo), arb(hi)
            pairings = [reference.packet_pairing(a, b, 1 + arb(i) / count,
                                                 1 + arb(i + 1) / count, dyadic)
                        for i in range(count)]
            lower, upper = bracket_gain(core, pairings, cap)
            old_gain = (count * sum((v**2 for v in pairings), arb(0))
                        / (weight_scale * (arb(3) / 2 if dyadic else 1)))
            norm_sq = reference.weighted_row_norm_sq(a, b, weight_scale)
            row_upper = norm_sq - lower
            if not (lower > old_gain and row_upper > 0):
                raise ValueError(f"no strict improvement certified for {window}, {places}")
            rows.setdefault(window, {})[places] = {
                "ambient_norm_sq_arb": str(norm_sq),
                "pairings_arb": list(map(str, pairings)),
                "previous_reduction_arb": str(old_gain),
                "optimal_gain_lower_expression_arb": str(lower),
                "optimal_gain_upper_expression_arb": str(upper),
                "projected_norm_sq_upper_expression_arb": str(row_upper),
            }
    if any(sha256(path.read_bytes()).hexdigest() != digest for path, digest in inputs.items()):
        raise ValueError("an input changed during the certification")
    return {
        "evidence": "weighted dual Gram enclosure and four improved projected-norm bounds",
        "level": 4,
        "alpha": "1/8",
        "exterior_frequency_interval": ["1", "2"],
        "exterior_packets": count,
        "gram_radial_core": [LEFT_RADIUS, str(radius)],
        "gram": grams,
        "gram_cosine_moments_arb": moments,
        "rows": rows,
        "flint_precision_bits": precision,
        "python_flint_version": version("python-flint"),
        "g1_source_sha256": inputs[proof],
        "source_sha256": inputs[source],
        "pairing_source_sha256": inputs[reference_source],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precision", type=int, default=106)
    parser.add_argument("--radius", type=int, default=128)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.precision < 80 or args.radius <= 4:
        parser.error("require precision of at least 80 bits and radius greater than 4")
    payload = json.dumps(certify(args.precision, args.radius), indent=2, sort_keys=True) + "\n"
    if args.report:
        with args.report.open("x", encoding="utf-8", newline="\n") as out:
            out.write(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

