# NSRW MB-06 cross-check records

These five JSON files preserve a historical cross-check of the fixed
Navier–Stokes Research Workbench (NSRW) MB-06 ratio
`expm1(17λ/10) / expm1(2λ)` at `λ = 10^-12`. Atlas includes the ratio as an
arithmetic regression case alongside its Landau integral examples.

The original input was
[`examples/research-verification/mb06-ratio-20261113.json`](https://github.com/flamehaven01/NavierStokes-Research-Workbench/blob/6119a2208e1992c1ecea5c9862eac712d604e77f/examples/research-verification/mb06-ratio-20261113.json)
at NSRW commit `6119a2208e1992c1ecea5c9862eac712d604e77f`. Its SHA-256 is
`c4d28daf7b44ef4ab0d7d90c74c1b942b181ddc9901e50a3a8a4beaf78a674e8`,
which matches the input digest in both baseline records. The upstream
[`mb06_ratio_crosscheck.py`](https://github.com/flamehaven01/NavierStokes-Research-Workbench/blob/6119a2208e1992c1ecea5c9862eac712d604e77f/src/nsrw/mb06_ratio_crosscheck.py)
used `mpmath.iv` to check containment independently of the rational enclosure
algorithm. The saved baseline identifies the run as an algorithm cross-check
with `independent_operator: false`.

| File | Role |
| --- | --- |
| [`nsrw-mb06-baseline.json`](nsrw-mb06-baseline.json) | `PASS` report for containment of the independently enclosed ratio. |
| [`nsrw-mb06-baseline-manifest.json`](nsrw-mb06-baseline-manifest.json) | Baseline input and report digests, upstream implementation hashes, and execution environment. |
| [`nsrw-mb06-shifted-input.json`](nsrw-mb06-shifted-input.json) | Negative control with a shifted recorded ratio interval. |
| [`nsrw-mb06-shifted-result.json`](nsrw-mb06-shifted-result.json) | Expected `FAIL` because the shifted interval excludes the independent enclosure. |
| [`nsrw-mb06-shifted-manifest.json`](nsrw-mb06-shifted-manifest.json) | Input and report digests, upstream implementation hashes, and environment for the negative control. |

The file names and bytes are preserved from the Atlas baseline. The
[portable baseline checker](../../../tools/verify_baseline.py) checks their
SHA-256 digests. Replaying the historical `mpmath.iv` computation requires its
pinned upstream environment. Atlas's standalone checks use the local
[`rational_intervals.py`](../../../riemann_evidence/rational_intervals.py) and
[`verification.py`](../../../riemann_evidence/verification.py) modules under
the Python standard library. [Code attribution and license](../../../NOTICE.md)

The recorded outcomes concern containment of a fixed ratio. The source
profile, numerical certification of the full angular moment, and the formal
bridge have their own proof obligations.
