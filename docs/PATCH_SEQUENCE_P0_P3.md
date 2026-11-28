# Riemann Evidence Atlas P0–P3 Patch Sequence

2026-11-23 · Execution order and acceptance criteria

This document records the implementation context and criteria for P0–P3. The [research roadmap](ROADMAP.md) tracks later priorities.

Pin the P0 baseline, then trace original Lean references in P1 and verify the common local term in P2. P1 and P2 can proceed in parallel after P0. P3 connects the formal results and evaluates the verification tools in Atlas. Transfer back to NSRW is a later study.

See the [Inspector review](INSPECTOR_REVIEW_2026-11-23.md) for acceptance evidence and held items.

## Integrated Review Results

| Evidence | Accepted result | Remaining scope |
| --- | --- | --- |
| [v0.1.0 baseline](REPOSITORY_BASELINE.md) | Local tag and HEAD at `8192cf0`. Ten numerical cases replayed. | Standalone numerical baseline. |
| [Original Lean references](rh-next-layer-module-set.json) | Five modules, seven declarations, six VALUE edges. Two replays matched. | Full transitive closure and RH kernel recheck unrun. |
| [Unresolved VALUE classification](rh-frontier-classification.json) | Of 378 references, 76 in Lean `Init` and 2 in RH compiled data were checked directly, 10 were graph candidates, and 290 were unconfirmed. `propext` is an `Init.Core` axiom. Both helpers have 57 direct VALUE references. | `Classical.choice` transitive paths remain unconfirmed. Candidate declaration kinds and axiom status need compiled evidence. |
| [Landau tail cap](E2A_TAIL_CAP_VERIFICATION.md) | The same rational interval accepts `1/200` and rejects `1/300`. Lean checks implications assuming the interval. | Formal connection to the real integral was pending at this stage. |
| Pinned Masullo manuscript and comparison | 940-page 2026-11-20 PDF, cutoff note on p. 514, trace formula pp. 519–520, missing final statement 13.3.1.2 p. 522. Basic `p=2` rational checks replayed. | Local source correspondence, test hypotheses, and validity of the trace formula remain open. Objections beyond prime 2 require exact hypotheses. |

On November 23, the Lean 4.33.1 classification replayed 2/2. Python 3.10.22 and 3.14.10 each passed 23/23 and local notebook output matched. P3.1 below records later Colab and GitHub Actions evidence.

## P0 — Pin the Baseline and Input Locations

- [x] **P0.1 Compare pinned inputs and outputs.** `tools/verify_baseline.py` checks the Python baseline and pinned Lean and original source cache. Normalize only regenerated comparison output to UTF-8/LF. Preserve original hashes and check the following digests before and after.

   | Input or record | SHA-256 |
  | --- | --- |
  | `rh-branch-module-set.json` | `f213bd94da41795a8bf8dff610312679cdb32347e08ab8420f4bddb39f7bf90c` |
  | `rh-next-layer-module-set.json` | `de121ac9ac426cc666410147abe107ab41e2d06effc01e4e2c480e88a1a1e582` |
  | `rh-frontier-classification.json` | `1d38bce4b88b68c1979ac9889a25873de321070523ac7306b2583b1bce0b5e99` |
  | `window-results-v2.json` | `ad3d31ceaf5a9a78e5f17f5c25ac087394eb57ebfb3cfdd977aa57c61ac66bf1` |
  | `The_Music_of_the_Primes_Masullo_2026-11-20.pdf` | `e039d3f6cf0a4b14f03c7edb85097752dd65c0a2fe543c76fe992be234f97bf5` |

- [x] **P0.2 Check docs and a fresh checkout.** The Masullo PDF and audit inputs under `sources/` are local. Tracked documents link the source URL, hash, required artifacts, and replay procedure. Check README links to local-only paths. Preserve different test counts as dated run results.
- [x] **P0.3 Fix claim scope.** Cite Alpöge's twenty items as research progress. Record Lean's RH and Dirichlet zero statements and Masullo's number-field Hecke claims separately with their own definitions. Preserve the missing statement on p. 522 as a held final theorem. Distinguish the p. 514 note from the pp. 519–520 argument.

**Completion criterion.** Replay portable arithmetic from a clean checkout and pinned sources using a separate cache. Report missing assets as `ENV_BLOCKED`. The local release candidate pins this baseline. P1 has separate acceptance. [Replay procedure](P0_BASELINE_REPLAY.md)

## P1 — Extend Verified Original Lean Paths

Local matching passed. The BFS join, v2 declaration matching, and long tar path controls passed. Of 57 direct helper references, 53 matched Lean `Init` and four matched pinned Mathlib. [Mathlib follow-up](rh-mathlib-frontier-match.json) Colab Linux replayed synthetic declarations and Python. Original `.olean` matching requires separate pinned files. [Run sequence and results](LEAN_MATCH_AND_COLAB.md)

- [x] **P1.1 Check direct helper references.** Deduplicate the existing reference lists for `rh_of_right._proof_1_1` and `rh_of_right._proof_1_2` while preserving each origin. Their sets of 57 are identical and include `Lean.Omega.*`. Classify once and link back to both. No direct `Classical.choice` was observed. Transitive reachability stays open. Prioritize declarations in the same `.olean` or a bounded Lean module set. Record module, declaration kind, TYPE or VALUE, and direct verification status.
- [ ] **P1.2 `HELD` — Verify the original `vwin_of_row`.** The target module is `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.VwinOfRow`. The publisher lists `VwinOfRow.olean` SHA-256 `d0beb229db7511a87434172b7d2af0e1830fa0d2585777f7c71badd06ac04d6a`. Synthetic USTAR, PAX, and GNU tests exercise long paths. `tools/tar_fragment.py` and `tools/recover_pinned_member.py` handle prefixes and PAX paths. A bounded search of 36 cached fragments for the 143-byte path returned `NOT_RECOVERED`. The 14-part source archive contains the theorem declaration. [Source digest](LEAN_MATCH_AND_COLAB.md#p1-local-matching-results) Once the member is available, check its digest and Lean 4.33.1, then read the target and direct TYPE/VALUE references for `everyCharacter_of_row → vwin_of_row`. If recovery or digest validation fails, retain the held status and continue P1.1 and P2.
- [ ] **P1.3 Verify axioms and Choice paths.** Use the checked `riemannHypothesis → rhOfAll → rh_of_every → rh_of_right → propext` path as a control. If the extended graph exposes a path to `Classical.choice`, record the path and declaration kinds. BFS keeps `(node, via_definition)` and tests both routes through a shared node. `ProofRefs` and `ProofFrontier` record declaration kind, TYPE references, and missing VALUE bodies. Version the extended schema. Verify definition-mediated VALUE dependencies separately from evaluation requirements.

**Completion criterion.** Tie each new edge to an actual declaration in a pinned compiled module or Lean environment and reproduce twice. Preserve the original 378-entry baseline and record new edges and unresolved boundaries separately. A count of new declarations is not an acceptance criterion.

## P2 — Compare the Local Term in Both Sources

Exact arithmetic GREEN. Analytic correspondence HELD. Baseline checks cover four prime-2 cases and reject wrong signs, wrong ramified factors, and wrong conductors. Compare pinned pp. 514, 519–520, and 522 with `ClaimStrip`. Principal-value/Euler-factor correspondence remains in P3.2. [Results and source locations](masullo/P2_CHARACTER_COMPARISON.md)

- [x] **P2.1 Pin a source term.** Over $F=\mathbb Q$ at $p=2$, start from Masullo's finite-place term (12.5.1.2) on p. 519. Locate the actual Alpöge source or Lean declaration for the prime-power weights. Record each location, variable, character value, conductor, modulus, ramification factor, measure, and logarithmic normalization. If either location or hypothesis is unconfirmed, report arithmetic separately and hold source correspondence.
- [x] **P2.2 Compare exact rational values at $s=2$.** For $L_2(s)=(1-\chi(2)2^{-s})^{-1}$, also check $-L_2'(s)/(L_2(s)\log 2)$. Cases are the trivial character, unramified nontrivial character modulo 3, primitive character modulo 4 ramified at 2, and the imprimitive principal character modulo 4. Alpöge references include `prim_zero` and `LFunction_changeLevel` in `ClaimStrip.lean`.

   | Case | $L_2(2)$ | Logarithmic derivative coefficient |
  | --- | ---: | ---: |
   | Trivial character | $4/3$ | $1/3$ |
   | Nontrivial modulo 3, $\chi(2)=-1$ | $4/5$ | $-1/5$ |
   | Primitive modulo 4, ramified at 2 | $1$ | $0$ |
   | Imprimitive principal modulo 4 | $1$ (modulus 4), $4/3$ (primitive character at conductor 1) | $0$ (modulus 4), $1/3$ (conductor 1) |

   Reject inputs with a flipped character sign or a finite factor at a prime ramified at 2. Primality checks would be needed for an interface accepting a general prime. The current pilot pins $p=2$ and its report.
- [x] **P2.3 Check source hypotheses and the held decision.** Determine how the p. 514 cutoff note affects the finite-place term, how p. 519 uses $\varphi(C_F^1)=0$, and what p. 520 actually uses. For $g_2=2^m u$ and $m\ne0$, $|1-2^m u|_2=\max(1,2^{-m})$. For $m=0$, $|1-u|_2\le1/2$ for every 2-adic unit. Check dependence on $u$ before applying ramified character cancellation. Match Haar normalization and test hypotheses before deciding principal-value correspondence. Evaluate external objections when their sources and hypotheses are fixed.

**Completion criterion.** Replay exact inputs, assumptions, formulas, and rejection controls, and locate each in both sources. If source correspondence is unresolved, state the tested arithmetic scope and missing connection. Record the p. 522 gap separately.

## P3 — Real Enclosures, Formal Connection, and Tool Evaluation

**P3.1 GREEN · P3.2 HELD · P3.3 scope-limited GREEN.** Lean 4.33.1 and pinned Mathlib checked the two real exponential enclosures, tail integral identity, 128-bit inclusion, and both thresholds. The `v0.2.0` Windows/Linux Python 3.10/3.14 jobs each passed 45 tests. The Linux Lean real receipt matched Colab byte for byte. [Replay and scope](P3_LANDAU_TAIL.md) · [Release CI](https://github.com/Flamehaven-Labs/riemann-evidence-atlas/actions/runs/45347096386)

- [x] **P3.1 Close the analytic gap in the Landau pilot.** Reuse the rational threshold proof. For $k=3$, $s=3$, and $[1,3]$, prove that the real tail lies within the saved interval. The target is $J_{\mathrm{tail}}=(1-13e^{-3}+172e^{-9})/81$. The Rat stage verifies series arithmetic and outward rounding at 128 bits for $3/8$ and $9/32$ with three and five squarings. The real stage uses an antiderivative and endpoint limits and connects the series enclosure to $\exp$. Reverse the endpoint for $-13$. Apply both positive and negative thresholds to the real integral. The Landau check can proceed while P2 source correspondence is held.
- [ ] **P3.2 `HELD` — Analytic connection across sources.** Prove the Mellin–Laplace substitution, Haar measure correspondence, and support and vanishing conditions for $\varphi$ at the term pinned in P2. Treat sum/integral exchanges and limits from a finite place to the global trace as separate obligations when needed. Hold an individual claim when it lacks a required source definition or conclusion.
- [x] **P3.3 Evaluate the tools within Atlas.** Apply the shared functions in the table below to Alpöge's compiled declarations, Masullo's manuscript, and local numerical cases. Test missing assumptions, source mismatches, and inconclusive error intervals as well as successful inputs. Distinguish source compilation, reading an original proof term, kernel checking, and execution of a separate checker. Credit operator or implementation independence only when observed.

   | Component | Use in Atlas | Distinction to verify |
  | --- | --- | --- |
   | Exact rational and interval arithmetic | Landau calculation and finite Euler factors | Input uncertainty versus computational error bounds. |
   | Lean tools | Trace Alpöge's types, proof terms, and imports and check small numerical proofs. | Assumptions, definitions, and proof kinds under similar names. |
   | Verification runner | Fixed inputs, positive/negative controls, and inconclusive results under resource limits. | Valid refutation versus missing evidence or an unrun check. |
   | Research records | Link manuscript version, page, formula, compiled file, declaration, and run. | A local arithmetic pass with p. 522 unresolved does not accept the final theorem. |

   Score the source correspondence at $F=\mathbb Q,\ p=2$ separately from
   formal inclusion of the Landau integral. Shared code runs independently in Atlas.
   Later projects can use the evidence here to test applicability in another domain.

**Completion criterion.** Preserve the assumptions and implications between numerical records and source definitions, and reproduce passing and rejected cases in pinned environments. A full RH kernel check, Masullo's final theorem, and scientific utility each require evidence at their own scope.
