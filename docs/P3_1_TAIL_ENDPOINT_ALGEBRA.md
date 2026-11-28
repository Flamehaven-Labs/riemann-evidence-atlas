# P3.1a — Rational Endpoint Propagation for the Fixed Landau Tail

This record preserves the P3.1a run. The later real proof is in the [P3 report](P3_LANDAU_TAIL.md).

The patch checked rational endpoint algebra. Real exponential enclosures and the real integral link were HELD. The scope is this arithmetic step within the source result.

## Pinned Input

- Baseline — k=3, s=3, a=1, b=3, precision_bits=128.
- Numerical baseline — ../window-results-v2.json, SHA-256 ad3d31ceaf5a9a78e5f17f5c25ac087394eb57ebfb3cfdd977aa57c61ac66bf1.
- Calculator — exp_bounds in ../riemann_evidence/rational_intervals.py.
- Target real integral formula — (1 - 13 exp(-3) + 172 exp(-9))/81. The identity was outside this patch's Lean proof.

## Python 128-Bit Outward Enclosures

- exp(-3) lower bound — 132356730205244743173018186111025421 / 2658455991569831745807614120560689152
- exp(-3) upper bound — 16941661466271327126146327822211253889 / 340282366920938463463374607431768211456
- exp(-9) lower bound — 20997090117932310769386338569904347 / 170141183460469231731687303715884105728
- exp(-9) upper bound — 41994180235864621538772677139808695 / 340282366920938463463374607431768211456

For the lower bound, −13 uses the upper exp(-3) endpoint and +172 uses the lower exp(-9) endpoint. Reverse the selections for the upper bound.

## Replay Files

- ../tests/lean/E2ATailEndpointAlgebra.lean pins these Rat endpoints and the baseline bounds, checks the combined expressions and ordering, accepts 1/200, and rejects 1/300.
- ../tests/test_tail_endpoint_algebra.py matches Python exp_bounds, Lean constants, and both tail cases in the ten-case baseline. It includes controls for incorrect signs and endpoint choices.
- ../tools/verify_p3_1_endpoint_algebra.ps1 compiles with Lean 4.33.1 and runs additional Python 3.10 and 3.14 regressions.

## Execution Evidence

Lean 4.33.1 (commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6) compiled the rational algebra. Both audited equalities depend on propext, Classical.choice, and Quot.sound. No sorryAx appeared. Python 3.10.22 and 3.14.10 each passed 43 tests and the ten-case report digest was preserved. P3.1a receipt r_367f5c29-5d84-4dfb-8e45-5cea514eed40 and matrix receipt r_a2da68c7-3e5e-43e9-9891-d23dbf58d812. Actual Colab, full RH kernel replay, and Mathlib analysis proofs were NOT_RUN.

## Real Proof Obligations at P3.1a

1. REAL_EXP_ENCLOSURE_HELD — Prove in Lean/Mathlib that the four fractions enclose Real.exp(-3) and Real.exp(-9).
2. REAL_INTEGRAL_IDENTITY_HELD — Prove that the integral of u^3 exp(-3u)/3! on the positive real axis outside [1,3] equals the target formula, including integrability and endpoint limits.
3. REAL_TO_RAT_BOUND_HELD — Bind the real integral and exponential inequalities to the saved Rat endpoints and check the relevant hypotheses.
4. ORIGINAL_SOURCE_LINK_HELD — Separately review the relationship to the source landau_window_ineq hypotheses.

This run reached P3.1a/RAT_ENDPOINT_ALGEBRA_PASS. Full P3.1 GREEN or REAL_INTEGRAL_CERTIFIED requires Lean verification of items 1–3.
