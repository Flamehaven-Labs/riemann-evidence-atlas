"""Certify projected-norm upper bounds for the L=4 constant spatial rows."""

import argparse
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path

from flint import acb, arb, ctx


G1_SOURCE_SHA256 = "a3ec4fc5e93c99937315a55144822c477f4a4d7f2d35869b7d2ccb07cdb086c0"
PACKETS = 16
WINDOWS = {"near_origin": ("1/4", "1"), "outer": ("16", "64")}


def weighted_row_norm_sq(a: arb, b: arb, weight_scale: arb) -> arb:
    start, stop = (a / 4).log(), (b / 4).log()
    if b <= 4:
        exponent = -arb(1) / 4
    elif a >= 4:
        exponent = arb(1) / 4
    else:
        raise ValueError("split the spatial interval at the weight seam")

    def primitive(s: arb) -> arb:
        return (exponent * s).exp() * (
            (1 + s**2) / exponent - 2 * s / exponent**2 + 2 / exponent**3
        )

    return (primitive(stop) - primitive(start)) / weight_scale


def packet_pairing(a: arb, b: arb, lo: arb, hi: arb, dyadic: bool) -> arb:
    pi = arb.pi()

    def integrand(x: acb, analytic: bool) -> acb:
        value = (2 * pi * hi * x).sin() - (2 * pi * lo * x).sin()
        if dyadic:
            value -= (pi * hi * x).sin() - (pi * lo * x).sin()
        return value / (pi * x * x.sqrt(analytic=analytic))

    result = acb.integral(
        integrand, a, b, abs_tol=arb(2)**-68, rel_tol=arb(2)**-60, eval_limit=120000,
    )
    if not result.is_finite() or not result.imag.contains(0):
        raise ValueError(f"failed to enclose a real pairing on [{a}, {b}]")
    return result.real


def upper_bounds(a: arb, b: arb, dyadic: bool, weight_scale: arb) -> dict:
    norm_sq = weighted_row_norm_sq(a, b, weight_scale)
    pairings = [
        packet_pairing(a, b, 1 + arb(i) / PACKETS, 1 + arb(i + 1) / PACKETS, dyadic)
        for i in range(PACKETS)
    ]
    flat_gram_factor = arb(3) / 2 if dyadic else arb(1)
    results = {}
    previous = None
    for count in (4, 8, 16):
        group = PACKETS // count
        aggregated = [sum(pairings[j:j + group], arb(0)) for j in range(0, PACKETS, group)]
        gain = count * sum((entry**2 for entry in aggregated), arb(0)) / (
            flat_gram_factor * weight_scale
        )
        upper = norm_sq - gain
        if not (gain > 0 and upper > 0):
            raise ValueError("the bound did not certify a strict improvement")
        if previous is not None and not gain >= previous:
            raise ValueError("the partition refinement did not certify a nondecreasing gain")
        results[str(count)] = {
            "subtracted_amount_arb": str(gain),
            "projected_norm_sq_upper_expression_arb": str(upper),
        }
        previous = gain
    return {"ambient_norm_sq_arb": str(norm_sq), "finest_pairings_arb": list(map(str, pairings)),
            "by_exterior_partition": results}


def certify(precision: int) -> dict:
    ctx.prec = precision
    source = Path(__file__).resolve()
    proof = source.parents[1] / "tests/lean/E2AGeometricTraceTest.lean"
    source_hash = sha256(source.read_bytes()).hexdigest()
    if sha256(proof.read_bytes()).hexdigest() != G1_SOURCE_SHA256:
        raise ValueError("the fixed G1 source differs from the pinned input")
    d = arb(4).log()
    weight_scale = (d / 4).exp() * (1 + d**2)
    rows = {}
    for window, (lo, hi) in WINDOWS.items():
        rows[window] = {
            "aligned_interval": [lo, hi],
            "real": upper_bounds(arb(lo), arb(hi), False, weight_scale),
            "real_and_two": upper_bounds(arb(lo), arb(hi), True, weight_scale),
        }
    if (sha256(source.read_bytes()).hexdigest() != source_hash
            or sha256(proof.read_bytes()).hexdigest() != G1_SOURCE_SHA256):
        raise ValueError("an input changed during the certification")
    return {
        "evidence": "outward-rounded upper expressions for four projected row norms squared",
        "level": 4,
        "alpha": "1/8",
        "row": "indicator of aligned spatial interval divided by sqrt(x)",
        "exterior_frequency_interval": ["1", "2"],
        "flint_precision_bits": precision,
        "python_flint_version": version("python-flint"),
        "g1_source_sha256": G1_SOURCE_SHA256,
        "source_sha256": source_hash,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precision", type=int, default=106)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.precision < 80:
        parser.error("precision must be at least 80 bits")
    payload = json.dumps(certify(args.precision), sort_keys=True, indent=2) + "\n"
    if args.report:
        with args.report.open("x", encoding="utf-8", newline="\n") as out:
            out.write(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

