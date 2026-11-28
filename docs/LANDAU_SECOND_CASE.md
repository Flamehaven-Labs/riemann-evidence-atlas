# Second Landau Tail Case Within the RH Study

Lean proves the real integral for the second Landau case. Windows and Colab Linux checked it against the saved numerical enclosure.

## Source and Scope

The source quantity is the positive tail integral in the third summand on the right side of Deduction.landau_window_ineq, with the factor 2*C0 omitted.
The source is sources/rh-landauWindowIneq.lean, SHA-256 e3d5d760bcefe1242d4f5b0ced44fc055f1fa8dfe048a2222cf2c39ae812e59c.
The new values specialize the same kernel at independently chosen parameters. [Extraction manifest](../lean-extract-manifest.json)

| Item | Fixed v0.2.0 certificate | Second case |
|---|---|---|
| k | 3 | 1 |
| rate = sigma - 2 | 3 | 2 |
| Excluded window [a,b] | [1,3] | [1/2,2] |
| Real integral | (1-13 exp(-3)+172 exp(-9))/81 | (1-2 exp(-1)+5 exp(-4))/4 |
| Lean real certificate | PASS (Windows/Colab/CI) | PASS (Windows/Colab) |

## Component Boundaries

- `riemann_evidence/rational_intervals.py` takes exact Fraction inputs and a supported precision of 128, 256, or 512 fractional bits and returns two Fraction endpoints. It is independent of Landau, cap decisions, provenance, and receipts.
- `window_kernel.py` owns the Landau polynomial, total mass, window and tail formulas, and `decide_upper_cap`.
- `landau_second_case.py` calls the existing `CHECK` and records provenance, code and manifest hashes, and the result receipt.
- `riemann_evidence/verification.py` records the input byte digest, status, evidence, and `claim_authority=NONE`.

The case reuses the existing interval calculator and decision function. Earlier regressions already used this path. It is the second Landau specialization with its own provenance, comparison, and pinned receipt. Its implementation lives inside Atlas.

## Fixed Decisions and Negative Controls

The integral $J$ is approximately 0.08895482802519657. [Exact rational endpoints and report](landau-second-case.json)

| Comparison | Precision | Expected status |
|---|---:|---|
| cap = 1/10 | 128 | PASS |
| cap = 1/20 | 128 | FAIL |
| Close cap, fixed rational in the receipt | 128 | UNRESOLVED |
| Same close cap | 256 | PASS |

For a valid `[L,U]`, return PASS if `U <= cap`, FAIL if `L > cap`, and UNRESOLVED if `L <= cap < U` when the precision budget is exhausted. The CLI also labels rejected input FAIL and uses the reason to distinguish it from refutation. An inverted interval or non-Fraction endpoints are computation errors.

Alternating Taylor sums of orders 180 and 181 give an exact cross-check. At $x=1,4$, term magnitudes decrease to zero after those orders. The verifier rejects tampered ordered endpoints, changed precision types and caps, and UNRESOLVED relabeled as PASS.

The internal 1024-iteration limit in `_small_exp` appears unreachable in the supported domain. For `y<=1/2` and at most 576 work bits, the geometric remainder after term 1024 is below `2^(-1024)` and hence below tolerance `2^(-580)`. The historical calculator was reused as-is. If the limit or input domain changes, distinguish internal budget exhaustion from input errors. Here UNRESOLVED exhausts the decision budget while the valid interval straddles the cap.

## Replay

~~~sh
python -E -S landau_second_case.py --verify-report docs/landau-second-case.json
python -E -S -m unittest discover -s tests -p test_landau_second_case.py -v
python -E -S tools/verify_baseline.py
~~~

The ten original cases and their Lean and Colab evidence were preserved. The additional numerical receipt has SHA-256 1e2ba00fd1ff34bf13145ad1838f12b01029ada14a0baac670a6bd7758d15121.

On 2026-11-24, Python 3.10.22 and 3.14.10 each passed 51 tests, the ten original cases, and the local notebook smoke test. The numerical receipt records the real Lean proof as unrun at that snapshot. Receipt r_a9265237-bbae-48be-b902-5bf99fdf4458.

## Lean Proof of the Real Integral

The gamma integral gives total mass $1/4$ on the positive half-line. An antiderivative gives the contribution of $[1/2,2]$ to subtract. Mathlib's Taylor remainder theorem encloses $e$. Reciprocals and fourth powers bound $e^{-1}$ and $e^{-4}$. Use the opposite endpoint for the coefficient $-2$. The resulting bounds fit the saved Python 256-bit interval. [Lean source](../tests/lean/E2ALandauSecondCase.lean)

Pinned Lean 4.33.1 and Mathlib compiled the integral identity, enclosure of $e$, 256-bit inclusion, and threshold comparisons. The integral is greater than $1/20$ and at most both the close cap and $1/10$. The four declarations use `propext`, `Classical.choice`, and `Quot.sound`. [Formal receipt](landau-second-case-lean-replay.json)

The numerical endpoints and close cap remain pinned. The verifier compares three rational constants in Lean with the receipt and compiles dependencies and the real proof in a temporary directory. For Mathlib setup, see the [Landau replay procedure](P3_LANDAU_TAIL.md#replay).

~~~sh
python -E -S tools/verify_landau_second_case_lean.py --lean "$LEAN_BIN" \
  --mathlib-project formal/landau --expect docs/landau-second-case-lean-replay.json
~~~

Two Windows runs yielded identical receipts with SHA-256 `8524abfecbbde27117d3ebbe4dcd8caba2bd0667bd7a5f17e2f648ca71f0fa12`. On 2026-11-24, Colab Linux recompiled four declarations with pinned Lean 4.33.1 and Mathlib. All fields except the host banner matched. The Linux receipt SHA-256 is `d4eab82887fa2d7f70414da71de6b74457a1a1dca84a552a532ba4fe1f5c1d93`. CI for the second case was still pending at that replay. [Original Colab receipt](landau-second-case-colab-replay.json)
