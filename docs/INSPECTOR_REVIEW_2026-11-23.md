# Inspector Review and P0–P3 Acceptance Decisions

| Review | Evidence identifier | Focus |
| --- | --- | --- |
| INSP-01 | Attachment `1aa46712-df13-415a-8aeb-7de0b3756b79` | Repository name, independence, and criteria. |
| INSP-02 | Attachment `ece9e921-c950-42f7-9b23-3bb3e9de6b89` | Code, Lean extraction, numerics, and manuscript. |
| FOLLOWUP-01 | Task `7dc0a3eb-a72c-474a-8202-011bc50041b0` | Long archive paths, helper proofs, prime 2, and tail integral. |

`INSP-01` and `INSP-02` identify the reports. The attachments did not establish the reviewers' accounts or legal names. INSP-02 read receipts are `r_23a32497-1feb-4bf0-80bb-cf68959ee040`, `r_13b09e8f-d007-4ef5-a904-90e57a07edb4`, `r_2eb6969f-3fa3-4ab7-b286-b79a0c0255e3`, `r_22fae20b-0970-495c-a12e-cecec718a27b`, `r_b4c18468-ff03-4594-be2c-86aaf913ae5c`, and `r_955a5d19-81ad-4689-b8c3-bcc6ad8caab0`. Follow-up receipts are `r_c9e8f413-874b-4600-bf2f-7f290929081a`, `r_2d7a5389-fc75-4c33-a9f7-dc4d3c9d75dc`, `r_2ccbd5c8-a400-47e6-81dd-534f22645857`, and `r_32efaf80-ca64-449e-b513-2521e5ba6c11`.

| Stage | Decision | Evidence and accepted scope |
| --- | --- | --- |
| P0 naming and baseline | **ACCEPT** | Adopt Riemann Evidence Atlas (`riemann-evidence-atlas`). Keep the `riemann_evidence` import, historical formats, and `v0.1.0`. The next local candidate is `v0.2.0-rc.1`. |
| P0 documentation and pins | **ACCEPT** | The plan contained two U+000B characters and missing TeX commands. Replay arithmetic and documentation in a fresh checkout and check originals from a separate cache. Missing originals give `ENV_BLOCKED`. Digest mismatches fail. |
| P0 history and large assets | **REJECT / AMBER** | Reject rewriting historical results and tags. Review full automatic downloads and remote Lean CI once inputs, compute, and the remote are available. |
| P1 paths and Lean extraction | **ACCEPT** | The earlier BFS lost a definition-mediated path at a node shared with a proof-only path. Track `(node, via_definition)` and test both paths. Add declaration kinds to `ProofRefs` and `type_refs` to `ProofFrontier`. |
| P1 `omega` helpers | **ACCEPT / AMBER** | Both have the same 57 direct VALUE references, including `Lean.Omega.*` and no direct `Classical.choice`. Check transitive dependencies and module ownership in a follow-up. |
| P1 long tar paths | **ACCEPT / AMBER** | A 143-byte USTAR path splits into prefix and name. `seek_member.py` reads only the first 100 bytes and omits PAX paths. The real archive failure and recovery from cache remain held pending member digest and declaration checks. |
| P2 prime 2 | **ACCEPT / AMBER** | Exact rational checks cover trivial, nontrivial, and ramified characters. Located `prim_zero` and `LFunction_changeLevel` in `ClaimStrip`. The imprimitive character modulo 4 needs both modulus 4 and conductor 1 factors. The Masullo principal value, measure, and test function connection remain held. |
| P2 automatic cancellation or equivalence | **REJECT** | A ramified character's unit average can vanish while the remaining weight depends on the unit. The local uncompleted Euler-factor check does not certify the completed $L$-function, trace, RH, or GRH. |
| P3 Landau tail | **ACCEPT** | The gamma tail polynomial takes values 13 and 172 at 3 and 9. Verify the rational series and outward rounding separately from the real exponential and integral proofs. |
| P3 integral with `Init.Data.Rat` alone | **REJECT** | Rational procedures check supplied rational inequalities. Analytic theorems connect the bounds to the real integral and `Real.exp`. |

See the [P0–P3 plan](PATCH_SEQUENCE_P0_P3.md) for sequencing and completion criteria.
