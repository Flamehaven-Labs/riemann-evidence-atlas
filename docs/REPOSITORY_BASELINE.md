# Standalone Repository Baseline v0.1.0

2026-11-23 · Numerical replay scope

## Baseline Decision

Commit `8192cf0923995e200185f271fba76b2387db9d67` on local `main` was
accepted as `v0.1.0`. The command `git cat-file -t refs/tags/v0.1.0`
returned `tag`, and the tagged commit matched. The working tree was
clean. Ten numerical cases and seven regression tests passed, and the
recomputed report matched. This acceptance covers local numerical replay.

| Evidence | Status |
| --- | --- |
| `window-results.json` | Preserves the bytes and SHA-256 of the earlier Colab result for ten cases. |
| `window-results-v2.json` | Regenerated with the standalone arithmetic and runner. Input digests, rational endpoints, and decisions match the earlier Colab baseline for all ten cases. |
| `lean-extract-manifest.json` | Records SHA-256 for 14 archive parts and matches for 15 local extracts. |
| `unit_test_receipt.json` | Historical receipt for 13 tests in a separate Proof Atlas development environment. The executable package source was unavailable in this working directory. |
| Lean review at this baseline | Byte comparison and static source tracing. Proof-value closure, kernel execution, and replay by an independent operator were unrun. |

The missing-case finding in the [verification specification](CROSS_REPO_WORKFLOW_AND_VERIFICATION_SPEC.md)
describes an earlier five-case snapshot. The Colab and standalone
implementations now have ten cases each. The [regression tests](../tests/test_replay.py)
reject missing or altered cases. Earlier versions remain in repository history.

MB-06 is an arithmetic case with a historical comparison. The transfer
documents record planned NSRW and TOE work. The standalone calculation and
regression suite require neither checkout nor either project's Lean environment.

Direct extraction of original RH declaration references has its [own record](PROOF_DEPENDENCY_PILOT.md).
That verification follows the pinned v0.1.0 numerical baseline.

## Acceptance Criteria for Later Versions

| Version | Criterion |
| --- | --- |
| v0.1.0 | Reproduce input digests, rational bounds, and decisions for the ten prior numerical cases and pass regression tests. |
| v0.2.0 | Extract references separately from elaborated theorem types and proof values. Check that imports alone do not become reference edges. |
| v0.3.0 | Prove a small inequality in a pinned Lean environment and replay the correspondence between the exact declaration, its assumptions, and the numerical result. |

The axiom audit records whether `Classical.choice` occurs in a proof path.
Separately check whether a definition used in a numerical evaluation depends on a chosen object.
For example, the original NSRW MB08 cutoff requires a quantitative bound
applicable to the actual chosen function or equivalent evaluation evidence.
