# P3 — Landau Tail Integral Verification

The pinned inputs are $k=3$, $\sigma=5$ (decay $s=3$), $U=1$, and $V=3$. The target is the integral in the third summand on the right side of `Deduction.landau_window_ineq`. The factor $2C_0$, other terms, and full conclusion are separate. [Lean extraction pins](../lean-extract-manifest.json) · [Python results](evidence/baseline/window-results-v2.json)

$$J=\int_{(0,\infty)\setminus[1,3]}
 \frac{u^3e^{-3u}}{3!}\,du
 =\frac{1-13e^{-3}+172e^{-9}}{81}.$$

**Local replay PASS.** Lean compiled two audited rational endpoint declarations, eight rational series declarations, and five real declarations. Axiom output was within `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`. Python 3.10 and 3.14 each passed 43 regressions at this stage. [Execution and hashes](landau-tail-lean-replay.json)

## Proof Structure

- [Endpoint propagation](../tests/lean/E2ATailEndpointAlgebra.lean) reverses the endpoint for $-13e^{-3}$ and matches both rational bounds to the Python 128-bit record.
- [Rational arithmetic](../tests/lean/E2ALandauTailRational.lean) computes Taylor sums of orders 37 at $3/8$ and 34 at $9/32$. It puts the Python geometric and [Mathlib exponential](https://github.com/leanprover-community/mathlib4/blob/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Analysis/Complex/Exponential.lean#L523) remainders under 192-bit dyadic upper bounds. Powers 8 and 32 followed by reciprocal reversal give the 128-bit endpoints. Exact rational powers avoid intermediate rounding.
- [Real proof](../tests/lean/E2ALandauTailReal.lean) encloses both real exponentials using Mathlib series bounds, computes total mass $1/81$ from the gamma integral, and subtracts the $[1,3]$ integral by an antiderivative. Endpoint propagation proves $1/300<J\le1/200$.

## Replay

First replay the numerical results with `python -E -S tools/verify_baseline.py`. Set `LEAN_BIN` to Lean 4.33.1.

~~~sh
python -E -S tools/verify_landau_tail.py --lean "$LEAN_BIN"
~~~

The real stage uses the [pinned Lake project](../formal/landau/lakefile.toml) and [lock](../formal/landau/lake-manifest.json). With the full Lean distribution, prepare the cache from `formal/landau`.

~~~sh
lake exe cache get Mathlib.Analysis.Complex.Exponential \
  Mathlib.Analysis.SpecialFunctions.Gamma.Basic \
  Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus \
  Mathlib.Tactic.Positivity Mathlib.Tactic.NormNum Mathlib.Tactic.Ring Mathlib.Tactic.Linarith
~~~

An executable-only Windows Lean bundle can omit the headers needed to build the Mathlib cache tool. For a new environment use the full Lean 4.33.1 distribution. [Distribution and SHA-256](PROOF_DEPENDENCY_PILOT.md)

Return to the repository root to replay.

~~~sh
python -E -S tools/verify_landau_tail.py --lean "$LEAN_BIN" \
  --mathlib-project formal/landau --expect docs/landau-tail-lean-replay.json
~~~

The runner checks the Lean commit, Lake lock, dependency commits, and tracked files. Reuse a prepared cache via `--mathlib-project`. The Windows [audit runner](../tools/audit_p3_landau_tail_real_local.ps1) first checks the default project and can use a preserved cache. The verifier compiles three modules in a temporary directory and records proof hashes and axioms. Its scope is this fixed integral. Original RH kernel verification and Colab have separate records.

`--expect` checks the Lean commit on both hosts and compares every field except the platform banner. Exit 1 is check failure, 2 missing environment or unreadable dependency, 3 receipt mismatch, and 4 timeout. The November 23 missing `formal/landau/.lake` directory remains in the [audit record](P0_P3_INDEPENDENT_AUDIT_2026-11-23.md).

### Local Replay on 2026-11-24

A full Lean 4.33.1 distribution and new Lake project restored pinned Mathlib sources and 2,725 cache entries without changing the lock. Recompiling the five real theorems matched baseline SHA-256 `a4bbb8951ec28fec7044e982c1df48f88e457edffe3bb865fe46b61b8590c828`. Missing dependencies, a changed lock, and a receipt missing real proofs returned 2, 1, and 3, respectively.

This replay restored the cache within the same operating environment. A later Windows audit matched the real receipt digest. Python 3.10 and 3.14 each passed 45 tests. [Baseline receipt](landau-tail-lean-replay.json)

### Colab Linux Replay on 2026-11-24

A fresh Colab runtime restored pinned Lean and Mathlib and compiled five theorems. Input and source digests and axiom output matched Windows. [Environment restoration](LEAN_MATCH_AND_COLAB.md) · [Colab receipt](landau-tail-colab-replay.json)

### GitHub Actions Replay on 2026-11-24

At `v0.2.0` commit `5cea9571018fe94ccf760c00c7db6f7c72817646` all five jobs passed. Linux Lean took 82 seconds, including 55 for pinned Mathlib and cache restoration. The real CI receipt matched Colab SHA-256 `45fb8d94c5969278472f0c9b828d21dd7f97db81edf7ab898e989fed8cbd975e`. [Release CI](https://github.com/Flamehaven-Labs/riemann-evidence-atlas/actions/runs/45347096386)

## P3.2 Cross-Source Correspondence

Over `F=Q`, a norm-dependent test $\varphi(c)=h(|c|)$ with $h(1)=0$ removes the unit shell. With normalized Haar measure, the outside shell weight is $\log 2\,h(2^{-m})2^{-|m|/2}$. Compact support in the positive radial line leaves finitely many $m$. Comparing with the full P2 Euler logarithmic derivative series requires a family of tests, the relation between positive and negative shells, and a justified tail and limit exchange. This source link remains HELD. [Source locations and assumptions](masullo/P2_CHARACTER_COMPARISON.md)

## P3.3 Verification Scope

| Artifact | Applicable check | Open |
| --- | --- | --- |
| Alpöge Lean | Extract types and proof terms from pinned `.olean` files and check two paths. | Recover `VwinOfRow.olean` and replay the original RH kernel check. |
| Masullo manuscript | Compare formula locations, measures, and test hypotheses in the pinned PDF. | Analytic equivalence of the principal value and Euler factor. |
| Numerical code | Distinguish rational results, incorrect signs or conductors, precision exhaustion, and tampering. | Analytic generalization to other inputs. |
| Lean tail certificate | Link exponential enclosures and thresholds to the fixed real integral and replay on Windows, Colab, and GitHub Actions. | Replay by a separate operator. |
