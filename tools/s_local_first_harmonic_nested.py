"""Compare signed first-harmonic traces in nested finite Galerkin spaces."""

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

import numpy as np

import s_local_low_galerkin as galerkin


WINDOWS = {"near_origin": ("1/4", "1"), "outer": ("16", "64")}
ALPHA = 1/8
LEVEL = 4


def phase(x: np.ndarray) -> np.ndarray:
    return np.exp(1j * np.pi * np.log(x/LEVEL))


def solve(gram: np.ndarray, outgoing: np.ndarray) -> np.ndarray:
    scale = np.sqrt(np.diag(gram))
    gram_scaled = (gram / scale[:, None]) / scale
    return np.linalg.solve(gram_scaled, outgoing / scale) / scale


def diagnose(refined: bool) -> dict:
    fine = galerkin.hat_basis(256, 1/LEVEL**2)
    coarse = galerkin.hat_basis(128, 1/LEVEL**2)
    fine_nodes = fine.edges[:-1]
    prolong = coarse.piece_values(fine_nodes, fine_nodes)
    if not np.all(np.isin(coarse.edges, fine.edges)):
        raise ValueError("the trial spaces do not have nested nodes")
    t, w = galerkin.kernel_quadrature(36)
    coefficient = (w @ np.exp(-1j*np.pi*t))/2
    if not 2.02129 < abs(coefficient) < 2.02253:
        raise ValueError("the numerical Fourier coefficient falls outside the certified enclosure")
    gram_radius, gram_step, gram_order, extent, row_step = (
        (640, 0.20, 8, 4096, 0.10) if refined else (512, 0.25, 7, 2048, 0.125)
    )
    x, weights = galerkin.radius_quadrature(2.0**-33, gram_radius, gram_step, gram_order)
    weights *= galerkin.weighted_measure(x, LEVEL, ALPHA)
    rows = {window: {} for window in WINDOWS}
    for place, dyadic in (("real", False), ("real_and_two", True)):
        physical = galerkin.physical(fine, x, dyadic, extent)
        gram = galerkin.weighted_gram(physical, weights)
        coarse_gram = prolong.T @ gram @ prolong
        gated = galerkin.low_spectrum(fine, 1/LEVEL**2, dyadic)
        for window, endpoints in WINDOWS.items():
            a, b = map(lambda s: float(Fraction(s)), endpoints)
            s, v = galerkin.radius_quadrature(a, b, row_step, 8)
            outgoing = galerkin.physical(fine, s, dyadic, extent).T @ (
                v * galerkin.weighted_measure(s, LEVEL, ALPHA) * phase(s) / np.sqrt(s))
            j, p = galerkin.radius_quadrature(a*np.exp(-1/4)/2, b*np.exp(1/4)/2, row_step, 8)
            incoming = galerkin.physical(gated, j, dyadic, extent).T @ (p * phase(j) / np.sqrt(j))
            a_coarse, b_coarse = prolong.T @ outgoing, prolong.T @ incoming
            fine_value = np.vdot(incoming, solve(gram, outgoing))
            coarse_value = np.vdot(b_coarse, solve(coarse_gram, a_coarse))
            traces = [float(2*np.real(coefficient*v)) for v in (coarse_value, fine_value)]
            rows[window][place] = {"trace_128": traces[0], "trace_256": traces[1],
                                   "signed_change_128_to_256": traces[1]-traces[0]}
    changes = [entry["signed_change_128_to_256"] * (1 if place == "real_and_two" else -1)
               for places in rows.values() for place, entry in places.items()]
    root = Path(__file__).resolve().parents[1]
    inputs = ("tools/s_local_first_harmonic_nested.py", "tools/s_local_low_galerkin.py",
              "tests/lean/E2AGeometricTraceTest.lean")
    source_hashes = {name: sha256((root/name).read_bytes()).hexdigest() for name in inputs}
    if source_hashes[inputs[-1]] != galerkin.G1_SOURCE_SHA256:
        raise ValueError("the fixed G1 source differs from its pin")
    return {"evidence": "uncertified nested finite Galerkin diagnostic",
            "coefficient_real_imag": [float(coefficient.real), float(coefficient.imag)],
            "gram_radius": gram_radius, "gram_step": gram_step, "gram_order": gram_order,
            "theta_extent": extent, "row_step": row_step, "row_order": 8,
            "signed_change_in_schedule_difference": sum(changes),
            "sum_absolute_changes": sum(map(abs, changes)), "rows": rows,
            "numpy_version": np.__version__, "source_sha256": source_hashes}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refined", action="store_true")
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    report = diagnose(args.refined)
    with args.report.open("x", encoding="utf-8", newline="\n") as out:
        out.write(json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
