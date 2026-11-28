# Independent P0–P3 Audit · 2026-11-23

**Decision** — BOUNDED ACCEPT / GLOBAL ACCEPTANCE HELD.

This report preserves the November 23 observations. The [current P3 procedure](P3_LANDAU_TAIL.md) describes cache configuration and receipt comparison.

## 1. Audit Targets
- Local path — `D:\Sanctum\research-sidequests\riemann-lean-2026-11-22`.
- Local main HEAD — 74beab42c6dfb1b4096cf782c0fb46511c5227f9.
- [Public repository](https://github.com/Flamehaven-Labs/riemann-evidence-atlas).
- Public main HEAD — 360ba23f411b39c03b0cddb6d266816d93d5433c (initial commit).
- No Actions runs or releases, before synchronization and release approval.

## 2. Direct Replay Evidence
- Python 3.10.22 and 3.14.10 each passed **43/43** regressions and matched all ten historical cases. Receipt r_88779462-1670-42ab-9751-341f880458aa.
- Pinned Lean 4.33.1 compiled the Rat endpoint algebra. Axioms were propext, Classical.choice, and Quot.sound. Receipt r_88779462-1670-42ab-9751-341f880458aa.
- The five Mathlib real theorems have a **saved earlier PASS** in docs/landau-tail-lean-replay.json, SHA-256 a4bbb8951ec28fec7044e982c1df48f88e457edffe3bb865fe46b61b8590c828.
- **This independent real replay was ENV_BLOCKED.** The verifier returned exit 2 because formal/landau/.lake/packages/mathlib was missing. The proof check was not reached. Receipt r_6276bf3e-7c99-4cef-8fb6-177add530de3.
- Audit script — `tools/audit_p3_landau_tail_real_local.ps1`.

## 3. Acceptance by Stage
| Stage | Decision | Pending |
|---|---|---|
| P0 | LOCAL GREEN | Independent replay from a fresh remote checkout and CI. |
| P1.1 | BOUNDED GREEN | Full transitive closure of the original RH proof. |
| P1.2 | HELD | Pinned VwinOfRow.olean and direct proof VALUE references. |
| P1.3 | PARTIAL | Full Classical.choice reachability in the original RH proof. |
| P2 | LOCAL ARITHMETIC GREEN | Analytic equivalence of Masullo's principal value and the Euler factor. |
| P3.1 | SAVED LEAN PASS / CURRENT REPLAY ENV_BLOCKED | Restore pinned Mathlib and replay all checks. |
| P3.2 | HELD | Exact test function, Haar measure, principal-value cutoff, Mellin–Laplace and trace correspondence. |
| P3.3 | SCOPED GREEN | Separate operator or CI replay and verification of the full paper theorem. |

**Landau scope.** The integral of `u^3 exp(-3u)/3!` over `(0,∞)\[1,3]`. Pinned Lean and Mathlib give `J=(1-13 exp(-3)+172 exp(-9))/81` and `1/300<J<=1/200`. The full RH or GRH statements, remaining terms, and `2C0` prefactor are outside the check.

## 4. Improvements and Acceptance Criteria
1. **G0 P3 replay.** Pin Mathlib 0df444a360eaa60ab8c11dca51a86af692955474 and Lake lock SHA-256 799c3b1ddf8eeffc9ed81510f37d8d6beb5479dc261ce3b3c01a205cd6d27667. Restore the cache and compare the five real theorems and axioms using the same verifier. Keep ENV_BLOCKED distinct from PASS.
2. **G1 CI.** Separate the Windows/Linux Python 3.10/3.14 matrix from Lean 4.33.1 with pinned Mathlib. Preserve complete hashes and negative results.
3. **G2 GitHub.** Synchronize the reviewed commit. Public main still had only the initial commit and no Actions run. Check README links, workflow, and commit on GitHub before tagging or releasing.
4. **G3 P1.** Keep VwinOfRow.olean and transitive Classical.choice paths pending. A public graph candidate needs verification against compiled proof data.
5. **G4 P2/P3.2.** Track the test, measure, principal-value cutoff on pp. 519–520, and missing final statement on p. 522 separately from prime-2 arithmetic GREEN.
6. **G5 Documentation drift.** Update the README to reflect the fixed real Landau result. Preserve 23/23 and 43/43 in PATCH_SEQUENCE as observations from different runs.
7. **G6 Evidence scope.** Keep numerical arithmetic, Lean Rat, Lean Real, proof references, original kernel replay, and source theorem equivalence separate.

## 5. Local Commands
- Python: pwsh -NoProfile -File tools/validate_python_matrix.ps1
- Lean Rat: pwsh -NoProfile -File tools/verify_p3_1_endpoint_algebra.ps1
- Lean Real after Mathlib setup — `python -E -S tools/verify_landau_tail.py --lean <lean4.33.1> --mathlib-project formal/landau`.
- Audit tool — `pwsh -NoProfile -File tools/audit_p3_landau_tail_real_local.ps1`.

The report records reproducible verification and its limits. The source theorem and peer review are separate.
