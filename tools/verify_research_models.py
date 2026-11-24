"""Replay bounded research models and record the scope of each check."""

from __future__ import annotations

import argparse
import hashlib
import json
from math import exp, fsum, isclose, sin, sqrt
from pathlib import Path

from verify_baseline import ROOT, run_python


def strip_sample(panels: int) -> dict:
    """Sample the fixed-width model with composite Simpson quadrature."""
    alpha = 0.25
    limit = 80.0
    gaps = (1e-2, 1e-4, 1e-6)
    step = limit / panels

    def integral(f):
        total = fsum((4 if i % 2 else 2) * f(i * step) for i in range(1, panels))
        return (f(0) + total + f(limit)) * step / 3

    def weight(x):
        return exp(-2 * alpha * x) / (1 + x * x)

    mass = 2 * integral(weight)
    moment = 2 * integral(lambda x: x * x * weight(x))
    # An independent identity from x^2/(1+x^2) = 1 - 1/(1+x^2).
    if not isclose(mass + moment, 1 / alpha, abs_tol=1e-9, rel_tol=0):
        raise ValueError("positive-strip moment identity disagrees with quadrature")
    moment2 = moment / mass
    linear_limit = 1 / sqrt(moment2)
    rows = []
    for gap in gaps:
        deficit = 4 * integral(lambda x: sin(gap * x / 2) ** 2 * weight(x)) / mass
        scale = sqrt(deficit * (2 - deficit))
        jump = (1 - deficit) / scale
        rows.append({
            "gap": gap, "scaled_deficit": deficit / gap**2,
            "linear_entry": gap * jump, "fixed_jump_entry": jump,
        })
    return {
        "alpha": alpha, "positive_half_line_cutoff": limit, "panels": panels,
        "moment2": moment2, "linear_limit": linear_limit, "samples": rows,
    }


def verify_strip_sample() -> dict:
    coarse = strip_sample(16_000)
    fine = strip_sample(32_000)
    if not isclose(coarse["moment2"], fine["moment2"], abs_tol=1e-9, rel_tol=0):
        raise ValueError("positive-strip moment did not agree under mesh refinement")
    for first, second in zip(coarse["samples"], fine["samples"], strict=True):
        for field in ("scaled_deficit", "linear_entry", "fixed_jump_entry"):
            if not isclose(first[field], second[field], rel_tol=1e-9, abs_tol=1e-10):
                raise ValueError(f"positive-strip {field} did not agree under mesh refinement")
    previous, last = fine["samples"][-2:]
    if (
        not isclose(last["scaled_deficit"], fine["moment2"] / 2, abs_tol=1e-8, rel_tol=0)
        or not isclose(last["linear_entry"], fine["linear_limit"], abs_tol=1e-8, rel_tol=0)
        or last["fixed_jump_entry"] <= 50 * previous["fixed_jump_entry"]
    ):
        raise ValueError("positive-strip small-gap predictions did not match the sample")
    return {"scope": "numerical diagnostic without certified integral bounds", "status": "PASS", **fine}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run_python("landau_second_case.py", "--verify-report", "docs/landau-second-case.json")
    run_python("tools/prime_two_unit_shell.py")
    report = {
        "landau_second_case": {
            "status": "PASS", "scope": "exact rational replay and threshold decisions",
            "report_sha256": hashlib.sha256((ROOT / "docs/landau-second-case.json").read_bytes()).hexdigest(),
        },
        "prime_two_unit_shell": {"status": "PASS", "scope": "exact rational sums", "inputs": 5, "depths": 8},
        "positive_strip": verify_strip_sample(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    print("Research model replay passed", flush=True)


if __name__ == "__main__":
    main()
