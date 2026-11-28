"""Audit nested finite compressions of the lower S-local frequency trace."""

import argparse
from dataclasses import asdict, replace
from hashlib import sha256
import json
from pathlib import Path
import platform

import numpy as np

import s_local_low_galerkin as low


def coarse_coordinates(coarse: low.Spectrum, fine: low.Spectrum) -> np.ndarray:
    """Expand the coarse continuous hats in the fine nodal basis."""
    if not np.all(np.isin(coarse.edges, fine.edges)):
        raise ValueError("the frequency meshes are not nested")
    knots = fine.edges[:-1]
    return coarse.piece_values(knots, knots)


def nested_traces(gram: np.ndarray, form: np.ndarray, inclusion: np.ndarray) -> dict:
    scale = np.sqrt(np.diag(gram))
    gram = (gram / scale[:, None]) / scale
    form = (form / scale[:, None]) / scale
    factor = np.linalg.cholesky(gram)
    orthogonal = np.linalg.solve(factor, np.linalg.solve(factor, form).T).T
    rotation, _ = np.linalg.qr(factor.T @ (scale[:, None] * inclusion), mode="complete")
    diagonal = np.diag(rotation.T @ orthogonal @ rotation)
    size = inclusion.shape[1]
    coarse = float(np.sum(diagonal[:size]))
    added = float(np.sum(diagonal[size:]))
    fine = float(np.trace(orthogonal))
    return {"coarse": coarse, "orthogonal_increment": added, "fine": fine,
            "split_residual": abs(fine - coarse - added),
            "normalized_gram_condition": float(np.linalg.cond(gram))}


def gram_matrix(spec, level, alpha, quad, dyadic):
    upper = quad.gram_radius_multiplier * level**2
    x, w = low.radius_quadrature(quad.gram_min, upper, quad.step, quad.order)
    weights = w * low.weighted_measure(x, level, alpha)
    size = spec.left.shape[1]
    gram = np.zeros((size, size))
    for start in range(0, len(x), 512):
        sl = slice(start, start + 512)
        cols = low.physical(spec, x[sl], dyadic, quad.theta_extent)
        gram += low.weighted_gram(cols, weights[sl])
    return gram


def spatial_form(spec, gated, a, b, level, alpha, quad, dyadic):
    x, w = low.radius_quadrature(a, b, quad.step, quad.order)
    weights = w * low.weighted_measure(x, level, alpha)
    t, wt = low.kernel_quadrature(quad.test_order)
    dilation, test_weights = np.exp(-t), wt * np.exp(-t / 2)
    size = spec.left.shape[1]
    form = np.zeros((size, size))
    for start in range(0, len(x), 96):
        sl = slice(start, start + 96)
        r = x[sl]
        cols = low.physical(spec, r, dyadic, quad.theta_extent)
        y = (r[:, None] * dilation).ravel()
        acted = low.physical(gated, y, dyadic, quad.theta_extent)
        acted = np.einsum("t,itj->ij", test_weights, acted.reshape(len(r), len(t), size))
        form += cols.T @ (weights[sl, None] * acted)
    return form


def audit(quad: low.Quadrature) -> dict:
    level, alpha = 4, 0.125
    radius = 1 / level**2
    coarse, fine = low.hat_basis(64, radius), low.hat_basis(128, radius)
    inclusion = coarse_coordinates(coarse, fine)
    places = {}
    for name, dyadic in (("real", False), ("real_and_two", True)):
        gate = low.low_spectrum(fine, radius, dyadic)
        gram = gram_matrix(fine, level, alpha, quad, dyadic)
        floor = spatial_form(fine, gate, 1 / level, 1, level, alpha, quad, dyadic)
        common = spatial_form(fine, gate, 1, level**2, level, alpha, quad, dyadic)
        top = spatial_form(fine, gate, level**2, level**3, level, alpha, quad, dyadic)
        places[name] = {
            "balanced": nested_traces(gram, common, inclusion),
            "quadratic": nested_traces(gram, floor + common + top, inclusion),
        }
    real, both = places["real"], places["real_and_two"]
    differences = {
        schedule: {key: both[schedule][key] - real[schedule][key]
                   for key in ("coarse", "orthogonal_increment", "fine")}
        for schedule in ("balanced", "quadratic")
    }
    return {"quadrature": asdict(quad), "places": places, "trace_differences": differences}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve()
    proof = source.parents[1] / "tests/lean/E2AGeometricTraceTest.lean"
    if sha256(proof.read_bytes()).hexdigest() != low.G1_SOURCE_SHA256:
        raise ValueError("the fixed G1 source differs from the pinned input")
    baseline = low.Quadrature(0.25, 7, 2.0**-33, 64, 2048, 36)
    settings = {
        "baseline": baseline,
        "extended_gram": replace(baseline, gram_radius_multiplier=128),
        "refined": replace(baseline, step=0.125, theta_extent=4096, test_order=72),
    }
    report = {"evidence": "uncertified numerical diagnostic", "level": 4, "alpha": 0.125,
              "cells": [64, 128], "platform": platform.system(), "python": platform.python_version(),
              "numpy": np.__version__, "g1_source_sha256": low.G1_SOURCE_SHA256,
              "source_sha256": sha256(source.read_bytes()).hexdigest(),
              "driver_sha256": sha256(Path(low.__file__).read_bytes()).hexdigest(), "results": {}}
    for label, quad in settings.items():
        row = audit(quad)
        report["results"][label] = row
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
                               encoding="utf-8", newline="\n")
        print(label, row["trace_differences"], flush=True)


if __name__ == "__main__":
    main()

