# E2A Tail Mass Cap Verification Record

On 2026-11-23 we replayed one numerical report and checked two thresholds in Lean. The quantity is the mass of `u³ exp(-3u) / 3!` on the positive real axis outside `[1, 3]`. Python uses `outside_window`, `k=3`, `rate=3`, `a=1`, `b=3`, and 128-bit precision.

| Stage | Result | Scope |
| --- | --- | --- |
| Python replay | `REPRODUCED`, 22/22 overall, `REPORT MATCH` | Recomputes the model and checks inputs, enclosure, and decisions. |
| Numerical binding to Lean | `REPLAY_BINDING_MATCH` | Compares two input digests, precision, decisions, endpoints, and thresholds against the replay. |
| Lean source check | `LEAN_SOURCE_CHECK`, exit 0 | Lean 4.33.1 checks rational inequalities and implications assuming the interval. |
| Independent checker | `NOT_RUN` | Needs pinned module resolution, dependency closure, and bounded resources. |
| Source correspondence | `REVIEW_PENDING` | Review real integral inclusion and its connection to the source theorem. |

## Positive and Negative Cases

| Case | Threshold | Python result | Lean comparison | Input SHA-256 |
| --- | --- | --- | --- | --- |
| `landau_tail_valid_cap` | `1/200` | `PASS` | Upper endpoint ≤ threshold | `ea5ed7211fb86cf13903c773fce203bd6fed318701bf4a98ffa2cc3067b65ede` |
| `landau_tail_violated_cap` | `1/300` | `FAIL` | Threshold < lower endpoint | `c6dc828a961aa6ccb3741da57c17245d336f78ccf2577f960806bd8ec4425337` |

The lower endpoint is `127263766859979925728141246211069006267/27562871720596015540533343201973225127936`. The upper endpoint is `10605313904998327144011770517589083871/2296905976716334628377778600164435427328`.

The [Lean source](../tests/lean/E2ATailCapCertificate.lean) orders the endpoints. For rational `mass`, it proves `mass ≤ 1/200` assuming `mass ≤ upper` and `1/300 < mass` assuming `lower ≤ mass`. Lean accepted a proof of `¬ (upper ≤ 1/300)` and rejected that proof term for `upper ≤ 1/300` with a type mismatch. The axioms are `propext`, `Classical.choice`, and `Quot.sound`. No `sorryAx` was observed.

The pilot covers threshold decisions for a rational interval. The real integral, the formal outward error bound, and independent source review are separate obligations. RH and the preserved `Main.olean` are outside the pilot scope.

The later P3 work connected the real exponential enclosures and tail integral in Lean. [P3 replay](P3_LANDAU_TAIL.md)

## Local MCP Evidence

The primary Flamehaven-MCP checkout ran FH-MCPd 0.3.6 over local stdio with temporary settings. `fh_verify_profile` used host-pinned Python 3.12.16 and Lean 4.33.1. One receipt lists 8/8 replay checks, `LEAN_SOURCE_CHECK`, `evidenceComplete=true`, and `checkedSource.unchanged=true`. The experiment ran separately from the operational daemon.

| Item | Value |
| --- | --- |
| Gateway generation | `78e11d321232d62f21ab3007deffa44facd356dcfc37b68988aeaa5bccd7965f` |
| Verification receipt | `r_63a9863f-d031-4ac5-84f6-e7eb9cae9440` |
| Input digest observation before / after | `r_7f87befe-2c44-42bd-83a7-8ad5550d1df2` / `r_8e014966-09eb-4845-a291-5ceab00ce839` |
| Python binary SHA-256 | `246221b571e7a692a8b26818b628cac4c163e836de9897812eaebc2a8e1efa90` |
| Lean binary SHA-256 | `af49bacfabaa1fea71332ca0feae0fa1a60912219d5902291adc79f905bffb8d` |
| `window_kernel.py` SHA-256 | `9c7c14b2fb5539ff450fed8ee8c8d65117396c1389d5cc2a074891854881502f` |
| `window-results-v2.json` SHA-256 | `ad3d31ceaf5a9a78e5f17f5c25ac087394eb57ebfb3cfdd977aa57c61ac66bf1` |
| `tests/test_replay.py` SHA-256 | `450b44f506235c11aeaa820cf9806b4e93177bc0c487ff331aad96605cc60818` |
| `E2ATailCapCertificate.lean` SHA-256 | `419f3d44c7be96a700dd7d5a790bddd220e3144044ea0f5df889f28aeac18a47` |
