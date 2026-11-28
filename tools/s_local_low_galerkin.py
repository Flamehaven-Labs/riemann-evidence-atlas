"""Numerical Galerkin diagnostic for the S-local lower frequency trace."""

import argparse
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import platform

import numpy as np


G1_SOURCE_SHA256 = "a3ec4fc5e93c99937315a55144822c477f4a4d7f2d35869b7d2ccb07cdb086c0"
LOG_TWO = np.log(2.0)


@dataclass(frozen=True)
class Spectrum:
    """Affine pieces on the positive half of an even spectrum."""

    edges: np.ndarray
    left: np.ndarray
    right: np.ndarray

    def cosine(self, radius: np.ndarray) -> np.ndarray:
        width = np.diff(self.edges)
        center = (self.edges[1:] + self.edges[:-1]) / 2
        theta = np.pi * radius[:, None] * width
        phase = 2 * np.pi * radius[:, None] * center
        slope_term = np.empty_like(theta)
        small = np.abs(theta) < 0.01
        z = theta[small]
        slope_term[small] = z * (1 / 3 - z**2 / 30 + z**4 / 840)
        z = theta[~small]
        slope_term[~small] = (np.sin(z) - z * np.cos(z)) / z**2
        return (
            (np.cos(phase) * np.sinc(theta / np.pi)) @ (width[:, None] * (self.left + self.right))
            - (np.sin(phase) * slope_term) @ (width[:, None] * (self.right - self.left))
        )

    def piece_values(self, samples: np.ndarray, interior: np.ndarray) -> np.ndarray:
        """Evaluate at possibly discontinuous endpoints from a specified side."""
        index = np.searchsorted(self.edges, interior, side="right") - 1
        active = (index >= 0) & (index < len(self.left))
        index = np.clip(index, 0, len(self.left) - 1)
        t = (samples - self.edges[index]) / (self.edges[index + 1] - self.edges[index])
        result = (1 - t[:, None]) * self.left[index] + t[:, None] * self.right[index]
        result[~active] = 0
        return result


def hat_basis(cells: int, low: float) -> Spectrum:
    layer = low / 2
    edges = list(np.arange(cells + 1) / cells)
    while layer < 1:
        edges.append(layer)
        layer *= 2
    knots = np.unique(edges)
    hats = np.eye(len(knots))[:, :-1]
    return Spectrum(knots, hats[:-1], hats[1:])


def low_spectrum(source: Spectrum, low: float, dyadic: bool) -> Spectrum:
    # (I - dilation_2) q T = q + (q-q(2·)) sum_{j>=1} dilation_2^j.
    # The second summand is on (low/2, low) and has finitely many nonzero pieces.
    dilations = [1]
    if dyadic:
        while dilations[-1] * low < 1:
            dilations.append(2 * dilations[-1])
    edges = {0.0, low / 2, low}
    for scale in dilations:
        floor = 0.0 if scale == 1 else low / 2
        edges.update(x for x in source.edges / scale if floor < x < low)
    knots = np.array(sorted(edges))
    center = (knots[1:] + knots[:-1]) / 2
    left = source.piece_values(knots[:-1], center)
    right = source.piece_values(knots[1:], center)
    shell = center > low / 2
    for scale in dilations[1:]:
        left[shell] += source.piece_values(scale * knots[:-1][shell], scale * center[shell])
        right[shell] += source.piece_values(scale * knots[1:][shell], scale * center[shell])
    return Spectrum(knots, left, right)


def physical(spec: Spectrum, x: np.ndarray, dyadic: bool, theta_extent: float) -> np.ndarray:
    values = spec.cosine(x)
    if dyadic:
        dilation = 2.0
        # Truncation scale is relative to the spectrum being transformed.
        while np.any(dilation * x * spec.edges[-1] <= theta_extent):
            keep = dilation * x * spec.edges[-1] <= theta_extent
            values[keep] += spec.cosine(dilation * x[keep])
            dilation *= 2
    return values


def gauss_on_panels(edges: np.ndarray, order: int) -> tuple[np.ndarray, np.ndarray]:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    half = np.diff(edges) / 2
    center = (edges[:-1] + edges[1:]) / 2
    return (center[:, None] + half[:, None] * nodes).ravel(), (half[:, None] * weights).ravel()


def radius_quadrature(a: float, b: float, step: float, order: int) -> tuple[np.ndarray, np.ndarray]:
    # Resolve the singular end with dyadic panels and the cosine phase with linear panels.
    edges = [a]
    edge = a
    while edge < min(b, 1.0):
        edge = min(2 * edge, 1.0, b)
        edges.append(edge)
    if edges[-1] < b:
        panels = int(np.ceil((b - edges[-1]) / step))
        edges.extend(np.linspace(edges[-1], b, panels + 1)[1:])
    return gauss_on_panels(np.array(edges), order)


def g1_kernel(t: np.ndarray) -> np.ndarray:
    d = t - LOG_TWO
    u = 2 - 32 * d**2
    h = np.where(u >= 1, 1.0, 0.0)
    second = np.zeros_like(t)
    # Below this distance from an endpoint the decaying factor underflows in float64.
    interior = (u >= 1e-4) & (u <= 1 - 1e-4)
    p = u[interior]
    a, b = np.exp(-1 / p), np.exp(-1 / (1 - p))
    transition = a / (a + b)
    slope = a * b / (a + b)**2
    log_first = 1 / p**2 + 1 / (1 - p)**2
    log_second = -2 / p**3 + 2 / (1 - p)**3
    h[interior] = transition
    second[interior] = slope * (
        ((1 - 2 * transition) * log_first**2 + log_second) * (64 * d[interior])**2
        - 64 * log_first
    )
    return second - h / 4


def kernel_quadrature(order: int) -> tuple[np.ndarray, np.ndarray]:
    edge = 1 / np.sqrt(32)
    # Split each transition again at u=1/2.
    middle = np.sqrt(3) / 8
    edges = LOG_TWO + np.array([-0.25, -middle, -edge, edge, middle, 0.25])
    t, w = gauss_on_panels(edges, order)
    return t, w * g1_kernel(t)


def weighted_measure(x: np.ndarray, y: float, alpha: float) -> np.ndarray:
    t = np.log(x / y)
    log_y = np.log(y)
    return np.exp(2 * alpha * (np.abs(t) - log_y)) * (1 + t**2) / (1 + log_y**2)


def weighted_gram(values: np.ndarray, weights: np.ndarray) -> np.ndarray:
    return values.T @ (weights[:, None] * values)


def solve_trace(gram: np.ndarray, form: np.ndarray) -> dict:
    scale = np.sqrt(np.diag(gram))
    normalized = (gram / scale[:, None]) / scale
    form = (form / scale[:, None]) / scale
    factor = np.linalg.cholesky(normalized)
    inner = np.linalg.solve(factor, form)
    orthogonal_form = np.linalg.solve(factor, inner.T).T
    return {
        "trace": float(np.trace(orthogonal_form)),
        "normalized_gram_condition": float(np.linalg.cond(normalized)),
        "trace_solve_residual": float(np.linalg.norm(factor @ orthogonal_form @ factor.T - form)),
    }


@dataclass(frozen=True)
class Quadrature:
    step: float
    order: int
    gram_min: float
    gram_radius_multiplier: float
    theta_extent: float
    test_order: int


def calculate_scale(level: int, cells: int, alpha: float, quad: Quadrature) -> dict:
    low = 1 / level**2
    basis = hat_basis(cells, low)
    t, wt = kernel_quadrature(quad.test_order)
    deformation = np.exp(-t)
    kernel_weights = wt * np.exp(-t / 2)
    maximum = quad.gram_radius_multiplier / low
    gx, gw = radius_quadrature(quad.gram_min, maximum, quad.step, quad.order)
    gram_weights = gw * weighted_measure(gx, level, alpha)
    results = {}
    for name, dyadic in (("real", False), ("real_and_two", True)):
        gated = low_spectrum(basis, low, dyadic)
        values = physical(basis, gx, dyadic, quad.theta_extent)
        gram = weighted_gram(values, gram_weights)
        results[name] = {}
        for schedule, spatial in (("balanced", level), ("quadratic", level**2)):
            x, w = radius_quadrature(level / spatial, level * spatial, quad.step, quad.order)
            values = physical(basis, x, dyadic, quad.theta_extent)
            applied = np.empty_like(values)
            for start in range(0, len(x), 128):
                take = slice(start, start + 128)
                samples = (x[take, None] * deformation).ravel()
                convolution = physical(gated, samples, dyadic, quad.theta_extent)
                convolution = convolution.reshape(len(x[take]), len(t), -1)
                applied[take] = np.einsum("t,itj->ij", kernel_weights, convolution)
            form = values.T @ ((w * weighted_measure(x, level, alpha))[:, None] * applied)
            results[name][schedule] = solve_trace(gram, form)
    differences = {
        key: results["real_and_two"][key]["trace"] - results["real"][key]["trace"]
        for key in ("balanced", "quadratic")
    }
    return {"level": level, "cells": cells, "dimension": len(basis.edges) - 1,
            "quadrature": quad.__dict__, "places": results, "trace_difference": differences}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--levels", nargs="+", type=int, default=[2, 4, 8])
    parser.add_argument("--cells", nargs="+", type=int, default=[8, 16, 32])
    parser.add_argument("--alpha", type=float, default=0.125)
    parser.add_argument("--refine", action="store_true", help="repeat the finest basis at tighter integration settings")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 0 < args.alpha < 0.5 or min(args.levels) < 2 or min(args.cells) < 2:
        parser.error("require 0 < alpha < 1/2, levels >= 2 and cells >= 2")
    source = Path(__file__).resolve()
    proof = source.parents[1] / "tests" / "lean" / "E2AGeometricTraceTest.lean"
    if sha256(proof.read_bytes()).hexdigest() != G1_SOURCE_SHA256:
        raise ValueError("the fixed G1 source differs from the pinned input")
    base = Quadrature(0.5, 6, 2.0**-27, 4, 512, 20)
    fine = Quadrature(0.25, 7, 2.0**-33, 8, 2048, 36)
    rows = []
    for y in args.levels:
        for n in args.cells:
            rows.append(calculate_scale(y, n, args.alpha, base))
        if args.refine:
            rows.append(calculate_scale(y, max(args.cells), args.alpha, fine))
    t, wt = kernel_quadrature(fine.test_order)
    report = {
        "evidence": "uncertified numerical diagnostic",
        "cutoffs": "sharp",
        "alpha": args.alpha,
        "source_sha256": sha256(source.read_bytes()).hexdigest(),
        "g1_source_sha256": G1_SOURCE_SHA256,
        "numpy": np.__version__,
        "python": platform.python_version(),
        "platform": platform.system(),
        "g1_controls": {
            "k_log_2": float(g1_kernel(np.array([LOG_TWO]))[0]),
            "moment_minus_half": float(wt @ np.exp(-t / 2)),
            "moment_plus_half": float(wt @ np.exp(t / 2)),
        },
        "results": rows,
    }
    result = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(result, encoding="utf-8", newline="\n")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()

