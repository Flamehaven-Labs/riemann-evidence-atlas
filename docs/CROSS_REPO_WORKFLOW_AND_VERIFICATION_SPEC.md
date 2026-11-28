# RH, NSRW, and Flamehaven TOE: Proof Dependency and Verification Specification

**Document ID** FH-E2A-CROSS-REPO-RFC-2026-11-23
**Version** 1.0 / DESIGN_AND_AUDIT_SPEC
**As of** 2026-11-23 (Asia/Bangkok)
**Scope** `D:\Sanctum\research-sidequests\riemann-lean-2026-11-22`, NSRW, and Flamehaven TOE
**Source material** `docs/idea1.txt`, `docs/idea2.txt`, `docs/ENGINEERING_RESEARCH_REPORT.md`, and `docs/unit_test_receipt.json`
**Authority** `claim_authority = NONE`. New Lean compilation, independent kernel checking, reproof of the original theorems, and physical validation of TOE are outside this design record.

> Credit the original results to their authors. Record the source, precise proposition, numerical calculation, expected output, execution environment, and failure conditions. Evaluate usefulness in a new domain as a separate empirical claim.

---

## 1. Scope of the verification design

The design combines the source pins, numerical cross-checks, and negative controls from IDEA1 with the observed MB-08 and TOE status, value-dependency analysis, and classical-choice audit from IDEA2.

1. **Source** records authors, papers, theorem and equation identifiers, pages, digests, and Lean and Mathlib pins.
2. **Formal proof** records the elaborated theorem type, definition closure, proof-value references, axioms, and typeclass dependencies.
3. **Numerical verification** records exact rational intervals, rigorous remainders, precision limits, and independent checks.
4. **Execution** records implementation, runtime, input and output digests, clean replay by a separate operator, and mutation tests.
5. **Transfer** records the target equation, units, baseline, testable failure criteria, and observations in NSRW or TOE.

Each link below requires its own direction and supporting evidence.

~~~text
PDF equation --[reviewed correspondence]--> Lean declaration type
Lean declaration --[value dependencies]--> actually used lemmas/defs
Numeric certificate --[independent checker]--> bounded inequality
Bounded inequality --[formal bridge]--> theorem precondition/consequence
Executable primitive --[domain adapter + baseline]--> NS or TOE application
~~~

For each result, identify where a new assumption, quantitative bound, nonconstructive selection, external computation, or change of interpretation enters the argument.

## 2. Inspected sources and evidence status

The following observations were made through Flamehaven MCP on 2026-11-23.

| Location | Direct observation | Scope |
| --- | --- | --- |
| RH side quest | Manifest for a 14-part archive, a record of 175,187 modules and 753,569 import edges, RH Main and Statements, Landau source, and a numerical verifier | No fresh archive hashing or proof-term closure run |
| NSRW `formal/p2/P2_MB06_NormalizedJ.lean` | `mbRepairRatio` and a conditional normalized angular moment theorem | Source inspection |
| NSRW `formal/p2/P2_MB08_TemplateJet.lean` and `P2_MB08_ResetAmplitude.lean` | Fixed reset and amplitude theorems conditional on derivative bound `hD` | Quantitative bound for the original chosen cutoff remains open |
| NSRW `src/nsrw/m5/lean_export.py` | Type-expression indexing and a `value_expression_id` field | The documented exporter does not traverse proof values |
| NSRW `docs/momentbound/FIXED_PROFILE_THRESHOLD_FINDING_2026-11-14.md` | Obstruction to an existing sufficient condition at the fixed tuple | The obstruction applies to that route |
| NSRW `docs/momentbound/MB08_SOURCE_CUTOFF_BOUND_DECISION_2026-11-14.md` | Missing explicit numerical jet bound for the chosen cutoff | Existence of a finite bound is a separate question |
| TOE `docs/PHYSICS_CONTRACTS.md` | Open gaps `C_prec` and `G3` | Dated document status |
| TOE `toe-scrutiny-suite` | Ricci tolerance of 0.5, Pontryagin rounding checks, and a Gödel discriminant threshold | HTTP regression and diagnostics |

Source identifiers
- Original draft in local outputs/document-sources/idea1.txt, before translation. SHA-256 5542a34dedebfa15345ef57065b3bf57f6bc6782dea96801f5381a52a1f3b472
- Original draft in local outputs/document-sources/idea2.txt, before translation. SHA-256 cd920555126d00af8d3cc9f50845e293858e080b0d06a98b1d2ae751827d727e
- Original report at `8192cf0923995e200185f271fba76b2387db9d67:docs/ENGINEERING_RESEARCH_REPORT_ko.md`. SHA-256 d8ba0f259861a0625b9481fea226ae20b10fa6127ebf5fb9e2d01347e867fe7c
- docs/unit_test_receipt.json SHA-256: b2727a2e59eae5ea33d4ae441c01cf41fefdf061cc2b0ff446705d0d63b3c768
- Archived merged RH SHA-256 `9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc`, as recorded in the archive manifest.
- RH uses `leanprover/lean4:v4.33.1`. NSRW uses a separate Lean v4.34.0-rc2 environment.
- NSRW upstream: openai/NavierStokesAndEuler commit 8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538.

**Evidence classes** include `OBSERVED_SOURCE`, `HISTORICAL_RECEIPT`, `SOURCE_DERIVATION`, `PROPOSED_DESIGN`, and `HYPOTHESIS`. Document creation alone supplies no OE-2 run. The 13/13 receipt from external Linux CPython 3.13.5 applies to that environment.

## 3. Findings and proposed changes

| ID | Finding | Proposed change | Status |
| --- | --- | --- | --- |
| F1 | Six `window_kernel.py run_cases()` cases versus five in `window-results.json`. Notebook outputs absent | Preserve the record and generate a versioned six-case result and run manifest | OBSERVED / OPEN |
| F2 | Some archived `rh-*.lean` extracts lack a consolidated source mapping | Index all archive member paths, digests, and source pins | OBSERVED / OPEN |
| F3 | `rh-proof-trace.json` records `kernel_dependency_closure = NOT_RUN`. Short import paths risk being overinterpreted | Keep `TYPE_CONST` and `VALUE_CONST` graphs | OBSERVED / OPEN |
| F4 | The finite Landau kernel bounds cover a limited calculation | Identify the RH experiment and the actual NSRW formal obligation | OBSERVED / OPEN |
| F5 | Numerical MB06 ratio lower bound exists with `formal_bridge = NOT_COMPILED_OR_ADMITTED` | Prove the lower bound against source `mbRepairRatio` in Lean | OBSERVED / OPEN |
| F6 | External 13-test `e2a_atlas` receipt lacks a matching implementation in the Windows worktree | Restore the exact source or pin a separate artifact location | OBSERVED / OPEN |
| F7 | RH and NSRW use different Lean toolchains | Pin each environment and compare with the corresponding toolchain | PREVENTION / OPEN |
| F8 | The 2026-10-05 E2A ledger and November MB-08 code and receipts reflect different dates | Check the newest dated receipt and append to the ledger | OBSERVED / OPEN |
| F9 | TOE numerical regression, heuristics, and exact invariants appear together | Label invariant, numerical approximation, and heuristic results explicitly | OBSERVED / OPEN |
| F10 | The MB-08 function selected by `Nonempty.some` lacks the quantitative derivative bound | Track the source proof and a constructive companion independently | OBSERVED / OPEN |

`OPEN` records work that is unrun, unconnected, quantitatively unresolved, or unreviewed. Preserve dated `HELD` and `FAIL` records when a later run passes.

---

## 4. Reading Lean artifacts backward from the theorem

### 4.1 Proof values and module imports

NSRW's `lean_export.py` normalizes theorem type expressions in a streaming two-pass offset index. It retains `value_expression_id` and documents that proof-value traversal remains unimplemented. The proposed extension follows.

**Pass A — Declaration index.** Index name, module, kind, type and value expression IDs, universe parameters, and source SHA. Stop without a pinned Lean export.

**Pass B — Expression traversal.** Traverse type and value subtrees separately. Record qualified CONST names and target declaration kinds. Preserve opaque, axiom, and external terminals.

**Pass C — Transitive closure.** Recover actual theorem and definition references in each closure. Mark missing declarations, cycles, duplicate entries, unsupported schema revisions, and exhausted traversal budgets `HELD`.

**Pass D — Statement comparison.** Compare PDF theorem and equation identifiers, quantifiers, domains, hypotheses, and constants against Lean binders, constructors, and conclusions. Review manually using `EXACT`, `ONE_WAY_IMPLICATION`, `CONDITIONAL`, `APPROXIMATION`, `NARRATIVE_ONLY`, or `UNMAPPED`.

**Pass E — Assumptions and selection.** Identify witnesses supplied only as hypotheses, missing quantitative bounds for data chosen by `Classical.choice` or `Nonempty.some`, conflicting definitions with the same notation, and explicit witnesses versus existential conclusions.

Proposed output fields

~~~json
{
  "schema": "flamehaven.e2a.proof_edge.v1",
  "source_identity": "sha256:<pinned archive or export>",
  "declaration": "A.B.theorem",
  "edge_kind": "VALUE_REFERENCES",
  "target_declaration": "C.D.lemma",
  "extraction_mode": "ELABORATED_VALUE",
  "status": "NOT_RUN"
}
~~~

**Test fixture.** Use one lemma referenced in a proof and one brought in only by an import. Graph centrality and minimum cuts can select paths for review. Mathematical necessity requires its own argument.

### 4.2 Quantitative obligations for classical choice

The MB-08 source theorem has this form.

~~~lean
theorem mb_fixed_reset_and_amplitude_of_template_derivative_bound
  (d : TailData) ...
  (hD : ∀ y : ℝ,
    |deriv AngularMomentReset.template y|
      ≤ (125 / 81 : ℝ) * 10 ^ (318 : ℕ)) :
  ∃ w : ResetWitness d 81162000,
    9 / 10 < CorrectedPulseAmplitude.amplitude
      d w.coefficients (1 / 1048576) := by
  ...
~~~

The theorem holds given `hD`. The available general interface supplies no specified numerical jet bound. A finite bound for the chosen function can still exist. Record the precise situation.

- `CLASSICAL_CHOICE_IN_PROOF` records ordinary classical reasoning.
- `NONCONSTRUCTIVE_DATA_SELECTION` records chosen data subject to a numerical requirement.
- `QUANTITATIVE_WITNESS_MISSING` records the absence of the required explicit constant in the available source evidence.
- `FORMAL_PREMISE_OPEN` records an unresolved application of hypothesis `hD`.

The absence of `sorry`, use of standard axioms, or inspection of a small Main file supports only the corresponding formal check.

### 4.3 Manuscript and Lean statement correspondence

The Alpöge–Buckmaster README reports that the paper was rewritten after formalization. Record the manuscript revision when aligning statements.

For each correspondence between a PDF locator and a qualified Lean declaration, preserve the following.

- hypotheses, domain, units, boundary conditions, quantifier order, implicit instances;
- strict < vs nonstrict ≤, weak vs smooth, closeness to candidate, blow-up rate, rate uniformity;
- PDF page, formula, original wording, and source category such as author statement, revised text, exposition, or secondary roadmap.
- Record absent pairs as `UNMAPPED` and one-directional implications as `ONE_WAY_IMPLICATION`.

Use text extraction and formula search to locate candidates. Inspect the rendered page and Lean declaration before marking a correspondence `EXACT`.

---

## 5. Mathematical review for RH and NSRW

### Track Formal: theorem identity → genuine proof

1. Pin the source archive and dependency digests.
2. Pair a Mathlib-only Challenge statement with the Solution and review the statement independently of its proof.
3. Run `#print axioms` per theorem. Record that theorem's dependencies separately from environment-wide axioms.
4. Run a clean pinned Lake build and record external kernel checker or comparator versions, modes, and outcomes.
5. Recover definitions, lemmas, and opaque or axiom boundaries from proof-value dependencies.
6. Review whether the Lean theorem matches the paper's actual claim.

### Analytic strategy and targeted checks

- RH. Test the proposed reading from finite-field Stepanov, forced divisibility, slope and theta lifts, and a one-sided Riesz mean bound through the Landau window to a zero-free region. Look for the actual declarations, constants, and uniformity in the proof closure. Treat Pei's exposition as a reading aid.
- NSRW. Record assumptions and conclusions for strict L2/L3, `DeltaM < 0`, repair-zero, local `J`, and global profile `J` under their respective claim IDs. Verify upstream assumptions where the proof uses them.
- TOE. Record physical equations, limiting connections to established theories, solver results, and independent observations as separate evidence.

### Numerical verdicts and counterexamples

- `PASS`. The certified interval separates the target region or sign within the precision budget.
- `FAIL`. A stated condition is violated or a counterexample is demonstrated. Rejection of a mutated certificate is an expected negative test.
- `UNRESOLVED`. The enclosure crosses the threshold or the remainder or precision budget is insufficient.
- `INVALID`. The schema, units, or mathematical domain are invalid.

Repeated calls to the same function test repeatability. A distinct rational series, rigorous interval library, or mathematical expression can reduce shared failure modes.

---

## 6. Proposed NSRW implementation

### 6.1 An exact ratio bridge for MB06

The inspected source defines

\[
R(\lambda)=\frac{e^{17\lambda/10}-1}{e^{2\lambda}-1}
\]

as `mbRepairRatio`. Its denominator is positive for \(\lambda>0\).

The following mathematical derivation had no new Lean run at the time of this record.

\[
0<\lambda<\frac12 \implies
R(\lambda)\ge\frac{17}{20}(1-2\lambda).
\]

Use \(e^{a\lambda}-1\ge a\lambda\) and \(e^{-2\lambda}\ge1-2\lambda>0\) to obtain \(e^{2\lambda}-1\le 2\lambda/(1-2\lambda)\).

At the fixed value \(\lambda=10^{-12}\),

\[
R(\lambda)\ge\frac{8499999999983}{10000000000000}.
\]

Proposed file `formal/p2/P2_RationalExpm1Bridge.lean`.

- State the theorem for source `mbRepairRatio`.
- Check `Real.add_one_le_exp` and related lemmas in pinned Mathlib, then prove the numerator and denominator estimates in Lean.
- Check the fixed-tuple lower bound with `norm_num`.
- Preserve `#print axioms` output and a clean source-build receipt.
- Use the Python mpmath interval cross-check to detect arithmetic errors independently of the formal proof.

The open obligations listed at the time were `SAME_SOURCE_PROFILE_F`, `F_AMP_ETA_GT_9_OVER_10`, `EXACT_FIRST_WINDOW_LOCAL_MASS_ZERO`, `LOCAL_J_NORMALIZATION_BRIDGE_NOT_COMPILED`, `SOURCE_PROFILE_FIXED_TUPLE_NOT_CONSTRUCTED`, and `COMBINED_SCALE_AND_RESET_K_UNRESOLVED`. Resolve each with the applicable Lean or execution receipt.

### 6.2 MB08 source and constructive companion

`FIXED_PROFILE_THRESHOLD_FINDING_2026-11-14.md` records that the upstream sufficient condition `combinedScale d K ≤ 1/1000` cannot be met at \(\lambda=10^{-12}\). It gives the necessary bound \(\lambda<1/(30000\cdot2^{120})\approx2.508\times10^{-41}\) for that sufficient-condition route.

**Original track (O).** Pin upstream `AngularMomentReset.template` and retain `hD`. Record `HELD[QUANTITATIVE_JET_WITNESS_MISSING]` while a bound for the chosen cutoff is unavailable.

**Constructive track (C).** For an explicit smooth cutoff, prove its support, plateau, smoothness, and derivative bounds. Recalculate the matrix, quadratic operator, reset, and energy polynomial. Use a separate artifact and claim ID until equality with the original function is proved.

An alternative is to prove the actual reset's small jets directly. Specify the argument that replaces the uniform derivative bound for the entire template.

### 6.3 Challenge and comparator

- Put source-defined objects and target theorem types in `P2_Challenge.lean`.
- Put proof terms in Solution and pin statements, hypotheses, and definitions.
- Compare target types and axioms externally. Record the local build separately.
- Use distinct claim IDs for the MB06 ratio lower bound, MB06 local `J`, MB08 source `hD`, and the MB08 constructive companion.

---

## 7. Proposed TOE investigations

### 7.1 C_prec: Eguchi–Hanson Pontryagin integral

The documented `C_prec` gap concerns quantitative error, for example \(|I+2|<0.1\) for \(h\) near \(10^{-4}\). The HTTP flag `is_2z_integer` and rounding \(\mathrm{round}(I/2)\cdot2\) provide diagnostics.

Proposed checks
1. Pin the metric, orientation, normalization, radial integrand, integration domain, and numerical tail and boundary conditions.
2. Use rigorous interval quadrature and bound the truncation remainder.
3. Record the exact interval \([L,U]\) and precision budget.
4. If a separate theorem gives integrality in \(2\mathbb Z\) and \([L,U]\subset(-3,-1)\), isolate the value \(-2\).
5. Report `NUMERIC_ENCLOSURE_ONLY` without an integrality theorem, and `UNRESOLVED` when domain or numerical requirements fail.

### 7.2 G3 — Gödel CTC

The `ctc_discriminant < 0.9` test in `toe_p3.py` is a regression heuristic. A closed timelike curve theorem requires the metric signature, \(\phi\)-periodicity, the tangent norm sign on the fixed-time curve, the coordinate domain, and global closure.

- Extract the exact proposition and hypotheses into an independent Lean Challenge.
- Compare `ctc_status`, `ctc_discriminant`, and `ctc_order_parameter` with the exact formal binders.
- Pin coordinate and gauge changes, boundary conditions, sign flips, and floating-point tolerance mutations.
- Use `CTC_DIAGNOSTIC_CANDIDATE` pending theorem compilation and semantic review.

### 7.3 RH1 as a research-only ANT1 model

Follow the ANT1 and `research_only_heuristics` pattern in `docs/ALGEBRAIC_NUMBER_THEORY_INTEGRATION.md`. Keep RH SmallClassNumbers and the finite Landau window outside physical vacuum acceptance criteria.

Example routing for a mixed TOE proposal

~~~json
{
  "proposal_type": "mixed",
  "primary_router": "ai-slop-detector",
  "secondary_router": "spar",
  "toe_scope": "optional_layer",
  "claim_authority": "NONE",
  "research_tag": "RH1_NON_GATING"
}
~~~

`ai-slop-detector` reviews integrity, wiring, and document drift. SPAR reviews mathematical and physical admissibility. Independent Lean checking, exact numerical certificates, and observation replay supply separate evidence.

### 7.4 Mathematical and empirical evidence

| Category | Examples | Supported claim |
| --- | --- | --- |
| MATHEMATICAL_CONTRACT | Precisely defined Ricci-flatness, integer charge, or theorem binder | The exact stated contract when supported |
| NUMERICAL_ENCLOSURE | Interval quadrature, remainder bounds, and fixed inputs | Containment at the stated input, precision, and scope |
| MODEL_HEURISTIC_BENCHMARK | `omega=(gs*b*si)^(1/3)`, tolerance scoring, and SPAR scores | Regression or diagnostic result |
| EMPIRICAL_CLAIM | Held-out observations and baseline comparisons | Empirical result within the preregistered measurements |

Dimensional consistency supplies a necessary check where applicable. Evaluate formal derivation, numerical evidence, and observation on their own terms.

---

## 8. Proposed files and acceptance checks

| Repository | Proposed file | Input and output | Minimum acceptance check |
| --- | --- | --- | --- |
| RH side quest | `tools/lean_value_dag.py` | Pinned export and theorem ID to type and value closures | Reject an import-only false positive |
| RH side quest | `tools/verify_case_inventory.py` | Window code and results to missing-case report | Six-case inventory and mutation tests |
| RH sidequest | registry/lean_extracted_manifest.json | archive member → SHA pinned records | 15 extracted files cross-check |
| RH side quest | `registry/semantic_bridges.yaml` | PDF equation, Lean type, and numerical claim | Reviewer, direction, assumptions, and limitations |
| NSRW | formal/p2/P2_RationalExpm1Bridge.lean | λ assumptions → exact ratio lower | clean Lean compile + #print axioms |
| NSRW | formal/p2/P2_Challenge.lean | proof-free source statement | comparator + lock |
| NSRW | `src/nsrw/m5/lean_value_dependencies.py` | NDJSON export to proof closure and choice sites | Deterministic output on an actual source fixture |
| TOE | `scrutiny/rigorous_pontryagin.py` | Integrand and interval certificate to enclosure | Separate tail and integrality checks |
| TOE | scrutiny/godel_scope_audit.py | code heuristic ↔ theorem binder | evidence-based gap report |
| TOE | `scrutiny/rh1_probe.py` | Finite arithmetic test to research-only result | Keep SPAR advisory |

These files were proposals at the time of writing. Record a receipt and hash upon implementation.

## 9. Verification and negative controls

**A — Identity.** Check archive part digests, original source, toolchain, Mathlib, and implementation identity before and after execution. Mark mismatches `STALE_ARTIFACT`.

**B — Formal and semantic review.** Compare Challenge and Solution statements, audit per-theorem axioms and proof-value closure, and review definitions and binders. Mark an unsupported checker `UNSUPPORTED`.

**C — Numerical independence.** Use exact rational production and an interval checker based on a different algorithm. Check denominator positivity, remainders, precision, and units.

**D — Negative controls.** Test a ratio shift of ±1e-9, an invalid numerical bound, precision exhaustion, a changed template identity, source digest replacement, removed hypotheses, a misleading Ricci tolerance pass, and documentation that promotes a CTC heuristic to a theorem.

**E — Clean replay.** Use a separate operator and clean checkout. Preserve stdout, stderr, exit status, manifest, and operator identity relative to the historical receipt.

Record each check as `PASS`, `FAIL`, `HELD`, `UNRESOLVED`, `NOT_RUN`, or `UNSUPPORTED`. All required checks must pass before promotion. A rejected mutation demonstrates the expected verifier behavior.

## 10. Implementation order and acceptance criteria

**M0 / Sidequest evidence repair**
- Preserve historical JSON. Generate a new `window-results-v2.json` and manifest covering six cases.
- Record complete origin digests for Lean extracts. Have the notebook call a single Python implementation.
- Obtain original implementation files for the earlier `e2a_atlas` receipt or record their external preservation location.
- DoD: pristine PASS, removed case/hash mutation FAIL, old files unchanged.

**M1 / Proof Atlas**
- Extend the type-only `lean_export.py` design to traverse actual proof values.
- Record lemma, definition, and axiom dependencies for five Main theorems, with source pins and output digests.
- Mark PDF correspondences `EXACT` only after review.
- Require actual proof-value extraction and a test for import-only false positives.

**M2 / MB06**
- pinned Lean ratio lower proof, fixed λ exact numeric bound, comparator, independent interval crosscheck.
- Keep the local-to-profile `J` step open until its assumptions are met.
- Preserve a scoped Lean compilation receipt for the bridge.

**M3 / MB08**
- Original hD conditional theorem type lock.
- Reverify support, derivatives, operators, reset, and energy for the explicit companion cutoff.
- Keep both results traceable. Require a proof of equality before promoting the source claim on the basis of its companion.

**M4 / TOE**
- Obtain a rigorous interval for `C_prec` and a separate integrality theorem.
- G3 exact CTC scope audit.
- RH1 research-only non-gating fixture.
- For each experiment, record inputs, assumptions, baseline, negative results, and a reproducible end-to-end run.

**M5 / Independent replay & translation**
- Run clean replay with a separate operator, execute mutations, and review for OE-4.
- After identifying a primitive at TR-0, check domain mapping at TR-1, a controlled regime at TR-2, and a preregistered baseline at TR-3.
- Keep unsupported claims `HELD` and limit application conclusions to the measured scope.

## 11. Evidence labels and public wording

`E2A_RESOURCE_STAGE_CROSSWALK` covers R0–R13, `OPERATIONALLY_EXPOSED` covers OE-0–4, and `ARTIFACT_TO_APPLICATION_TRANSFER_GATES` covers TR-0–6.

- R0 / OE-0 records a citation. R1 / OE-1 records a representation. R2 records a proposed falsification test.
- R3 / OE-2 requires a bounded run with exact environment details and a receipt.
- R4 / OE-3 requires clean replay by a separate operator.
- R5 / OE-4 requires observed failure under the declared mutation or violated assumption.
- R6 / TR-0 extracts a small primitive with recorded lineage, generally after OE-4.
- TR-1–6 cover domain relevance, controlled transfer, comparison, prototyping, domain validation, and deployment review.

Use the following labels with their stated scope.

- **REPRODUCED** means the specified calculation or result was obtained again under given conditions.
- **KERNEL_CHECKED** means the checker accepted a specified Lean proposition and proof term.
- **SOURCE_ALIGNED** means the PDF and Lean assumptions and conclusions received semantic review.
- **INDEPENDENTLY_REPLAYED** means the same scope was reproduced in an isolated environment by a separate operator.
- **TRANSFER_SUPPORTED** means a preregistered test found additional value in the target domain.

Semantic alignment, formal acceptance, numerical enclosure, and physical observation require their own evidence.

## 12. References

**Sidequest:** README.md, verify_lean_archive.py, trace_lean.py, rh-proof-trace.json, sources/rh-Main.lean, sources/rh-Statements.lean, sources/rh-landauWindowIneq.lean, window_kernel.py, window-results.json, RH_NSRW_Window.ipynb, docs/idea1.txt, docs/idea2.txt.

**NSRW:** formal/p2/P2_MB06_NormalizedJ.lean, P2_MB08_TemplateJet.lean, P2_MB08_ResetAmplitude.lean, docs/momentbound/FIXED_PROFILE_THRESHOLD_FINDING_2026-11-14.md, MB08_SOURCE_CUTOFF_BOUND_DECISION_2026-11-14.md, src/nsrw/m5/lean_export.py, src/nsrw/research_verification_cli.py, src/nsrw/verification_manifest.py.

**TOE:** Flamehaven-TOE(Theory of Everything)/docs/PHYSICS_CONTRACTS.md, ALGEBRAIC_NUMBER_THEORY_INTEGRATION.md, NEW_MODEL_TRIAGE_CHECKLIST.md, SPAR_vs_SLOP_DETECTOR.md, toe-scrutiny-suite/_scrutiny_common.py, toe_p1a.py, toe_p1e_p6.py, toe_p3.py, toe_p4_audit.py.

**Original sources** [Alpöge announcement](https://alpo.ge/remark.pdf), [MIT verification](https://math.mit.edu/~drew/grh/), [Lean community account](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/), [Lean RH source](https://github.com/leanprover-community/riemann-hypothesis/tree/40e56bab026552e089d7afcfeff08d2defb9c005), [OpenAI Navier–Stokes source](https://github.com/openai/NavierStokesAndEuler/tree/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538), and [Buckmaster Navier–Stokes source](https://github.com/tristanbuckmaster/navier-stokes).

### Scope of this specification

This specification traces a paper statement through the Lean object and proof dependencies to a certificate, reproducible result, failure test, and measured application. The status of each link remains visible.
