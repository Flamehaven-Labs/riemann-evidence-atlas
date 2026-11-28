# P0 Baseline Replay

Use this procedure for `v0.2.0`. The candidate baseline is `v0.2.0-rc.1`, with the earlier numerical baseline at `v0.1.0`. Keep the pinned asset cache separate from the checkout.

## Python Baseline

~~~sh
python -E -S tools/verify_baseline.py
~~~

`P0_PORTABLE_BASELINE_PASS` records Python regressions, ten window and ratio cases, prime-2 arithmetic, offline notebook cells, and saved JSON digests. Two of the ten cases are historical MB-06 ratio regressions. A fresh checkout replays offline without NSRW.

## Original Inputs and Lean

Extend the replay with the existing local cache. Substitute the actual paths in your environment.

~~~powershell
python -E -S tools/verify_baseline.py `
   --lean "<Lean 4.33.1 Windows installation>/bin/lean.exe" `
   --proof-assets "<preserved cache>/rh-proof-value" `
   --masullo-pdf "<original cache>/The_Music_of_the_Primes_Masullo_2026-11-20.pdf"
~~~

| Input | Location and pin |
| --- | --- |
| Lean | Version 4.33.1 from `lean-toolchain`. Use the Windows baseline host because the saved JSON includes the actual platform. |
| Five original modules | Cached `alp-oleans-Main-and-small.tar.gz` and `branch-inputs/{CritLine,MainConclusion,RhOfRight}.olean`. [Members and digests](rh-next-layer-module-set.json) · [Archive SHA-256](../tools/replay_rh_module_set.py) |
| Publisher's graph | Cached `verified-rh-graph.json.gz`. [SHA-256 and scope](../tools/replay_rh_frontier.py) |
| Masullo draft | [Source URL and digest](masullo/README.md) |

`P0_PINNED_SOURCE_REPLAY_PASS` records the Lean rational tail thresholds and two independent generations of the five modules' direct references and 378 classifications against pinned JSON bytes. CRLF is normalized to LF only for regenerated stdout. The Masullo PDF is digest-checked. Missing source files return `ENV_BLOCKED` and exit 2. Bad inputs or run failures return exit 1.

The [P0–P3 plan](PATCH_SEQUENCE_P0_P3.md) and [acceptance decisions](INSPECTOR_REVIEW_2026-11-23.md) define the scope. The full RH kernel check, actual Colab, and separate operator replay were unrun at this baseline.
