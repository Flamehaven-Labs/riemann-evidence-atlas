# Lean Matching and Colab Replay Sequence

2026-11-24 · Lean 4.33.1, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`

| Stage | Environment | Completion criteria |
| --- | --- | --- |
| P0 | Fresh local checkout | Replay the Python baseline and pinned Windows receipt. Pin at `v0.2.0-rc.1`. |
| P1 local | Pinned local Lean | Compare both synthetic Choice routes, declaration kinds, TYPE/VALUE references, and original helper references. |
| P1 Colab | Colab Linux CPU | Python baseline and synthetic Lean receipt replayed. Original `RhOfRight.olean` matching remained a follow-up. |
| P2 | Local first, then Colab after P1 | Prime-2 rational checks and controls. Record source correspondence separately. |
| P3 | Local or Colab with pinned Lean and Mathlib | Compile Rat thresholds and real integrals separately. Preserve sources, declarations, axioms, logs, and results. |

Colab Linux CPU replayed Python, synthetic Lean, and rational and real Landau proofs in sequence. Pin a commit SHA for a new session. Original `.olean` matching needs separately hash-checked files. Record host and Lean version. Declaration matching uses the Lean commit, input and checker hashes, TYPE/VALUE references, and decisions.

## Colab Replay Procedure

Open the [research model notebook](../colab/Research_Model_Replay.ipynb) in Colab and set `ATLAS_COMMIT` to the full public commit SHA. Numerical cells cover the second Landau case, the prime-2 unit shell, and positive width. Turn on `RUN_LEAN` to prepare pinned Linux Lean and Mathlib and compare new proof results with the Windows and Colab baselines. Results go to `outputs/research-model-replay`.

The GitHub Actions model job runs the same notebook's numerical cells and checks repeated reports. The separate Lean job compares fresh proof output with saved Colab receipts. Job artifacts include the commit, input digests, results, and logs. [Workflow and runs](https://github.com/Flamehaven-Labs/riemann-evidence-atlas/actions/workflows/checks.yml)

Run from the root of the pinned checkout on CPU with `elan` available.

~~~sh
elan toolchain install leanprover/lean4:v4.33.1
LEAN_BIN="$(elan which lean)"
python -E -S tools/verify_baseline.py
python -E -S tools/verify_lean_match.py --lean "$LEAN_BIN" \
  --expect docs/rh-lean-fixture-match-v2.json > /content/rh-lean-fixture-match.json
~~~

For the original, pass `--rh-of-right /content/RhOfRight.olean` and expect `docs/rh-lean-helper-match-v2.json`. `--expect` compares declarations and pinned digests and preserves the separate platform strings. Record missing inputs, digest mismatches, and failures to load original `.olean` files on Linux. For P3.1 rational and real checks, use the [Landau replay commands](P3_LANDAU_TAIL.md#replay).

## Colab Results on 2026-11-24

The ZIP contains tracked files from `aff300de0b5a0be2affb3c89f1c7f5e5fddb704e`. ZIP SHA-256 is `d958058f9de18c4d1a79b7462c6213f47b8327fa9a68717fdb552a5ada620bbf`. Colab Linux x86-64 CPU with Python 3.13.18 passed 45 Python tests, ten cases, synthetic Lean matching, rational Landau, and five real theorems in pinned Mathlib.

Real proof receipt SHA-256 is `45fb8d94c5969278472f0c9b828d21dd7f97db81edf7ab898e989fed8cbd975e`. All fields except the host banner matched Windows. [Colab receipt](landau-tail-colab-replay.json) · [Windows receipt](landau-tail-lean-replay.json)

The first bundle omitted three tracked manifests, restored from the same commit. The Mathlib cache tool required `lean-toolchain` in the Lake working directory. Colab copied the root pin bytes and retried. Atlas added the [Lake project pin](../formal/landau/lean-toolchain) and a CI consistency check. Colab did not compare original RH `.olean` files or replay the full kernel check. [Workflow runs by commit](https://github.com/Flamehaven-Labs/riemann-evidence-atlas/actions/workflows/checks.yml)

## P1 Local Matching Results

- Synthetic Lean checks both definition-mediated and proof-only Choice. Bodyless axioms have `value_refs=null`, while a saved body without references has an empty list. [Synthetic baseline](rh-lean-fixture-match-v2.json)
- The original `rh_of_right._proof_1_1` and `_proof_1_2` have identical sets of 57 direct VALUE references. The first pass matched 53 in Lean `Init`. The four unresolved declarations were `Int.instLinearOrder`, `LinearOrder.toPartialOrder`, `PartialOrder.toPreorder`, and `Preorder.toLT`. [Original baseline](rh-lean-helper-match-v2.json)
- Preparing P3 matched the four in three compiled pinned Mathlib files. All 57 now match `Init` or pinned Mathlib. [Follow-up](rh-mathlib-frontier-match.json)
- USTAR, PAX, and GNU long-path tests passed. A bounded search of 36 compressed fragments left `VwinOfRow.olean` `HELD`. The original 14-part source archive yielded `theorem UpperTheory.One.vwin_of_row` at line 4 of `VwinOfRow.lean` with SHA-256 `d2df45a5cf337190ae6f885e8e43056ae4e804ae8da250a2ab0abd64b1ca7080`. Further compiled VALUE edges require the pinned `.olean`. [Source archive](evidence/source-index/lean-archive-manifest.json)

P1 matches saved expressions. The full RH kernel check and independent operator replay are separate.
