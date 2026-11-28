# Equation to Artifact: Proof Dependencies and Reproducibility Across RH, NSRW, and TOE

**As of 2026-11-22.** This report records research design and static inspection.

**Workspace inspected** `D:\Sanctum\research-sidequests\riemann-lean-2026-11-22`, read-only through Flamehaven MCP.
The evidence consists of directly observed workspace files, external primary verification records, and research proposals awaiting implementation and verification.

## 0. Initial findings

The workspace preserved 14 original RH Lean archive parts, pinned statements and entry points, an import graph with 175,187 modules, four PDFs, and NSRW-derived interval calculations. Three observations define the immediate work. `rh-proof-trace.json` records `kernel_dependency_closure: NOT_RUN`. `RH_NSRW_Window.ipynb` has no saved outputs. `window-results.json` records five of the six cases defined in `window_kernel.py`. Full proof verification and independent replay remain outside this record.

Organize the evidence around propositions, hypotheses, actual proof terms, certificates, calculated results, manuscript interpretation, and application experiments. Record the supported correspondences and remaining gaps.

## 1. Starting points in the RH proof

The preserved `sources/rh-Main.lean` imports `Statements` and `Supplements.Kernels.MainTheoremsAll` and assembles five top-level theorems. `riemannHypothesis` has Mathlib type `RiemannHypothesis`. The implementation is `rhOfAll : RiemannHypothesis := Formalism.VW.rh_of_every allChi`. `allChi` targets `UpperTheory.EveryCharacter`. Review theorem declarations, Mathlib definitions, imports, actual declaration references, kernel, and runtime as separate parts of the final result.

`rh-proof-trace.json` records 175,187 modules, 753,569 internal import edges, and an import path from `Main` to `landauWindowIneq`. To establish actual use, begin at the Main theorem and extract the declaration-level closure from `ConstantInfo.type`, `.value`, definition bodies, selected instances, and universe parameters. Candidate methods include single-declaration extraction with `lean4export` or `leagent` and AST and tactic-state extraction with LeanDojo.

### RH Bridge L1: `landau_window_ineq` vs `window_kernel.py`

Python computes a serialized exact rational enclosure for the following finite-interval integral.

\[
J_{k,r}(a,b)=\int_a^b \frac{u^k e^{-ru}}{k!}\,du,
\quad k\in\mathbb N,\ r>0,\ 0\le a<b.
\]

The integral has a closed form.

\[
J_{k,r}(a,b)=\frac{e^{-ra}P_k(ra)-e^{-rb}P_k(rb)}{r^{k+1}},
\qquad P_k(z)=\sum_{j=0}^{k}\frac{z^j}{j!}.
\]

RH's `landau_window_ineq_int` establishes integrability of `u^k exp((2-σ)u)/k!` for `σ>2` on the positive half-line. The candidate substitution is `r=σ−2`. Relating Python's `[a,b]` to Lean's `Ioi 0` and the `WindowHypU` interval `[U,(1+δ)U]`, pointwise bound `g≤R`, and weighted integral bound requires at least three checks.

1. Establish the exact correspondence for `r=σ−2`, variables, measure, factorial normalization, and intervals.
2. Prove a separate bridge showing how the numerical bound controls the analytic function `R(u)` or `g(u)`. This evidence was missing.
3. Preserve the infinite tail, weighting, quantifier order for `θ`, `δ`, `η`, `U`, and `γ`, and all integrability and sign conditions.

Use `RH-L1` through `RH-L5` to track the obligations from positive kernel mass on a finite window to exclusion of zeros of a complex function.

### RH Bridge L2: The proposed proof strategy

Yan Ru Pei's November 2026 reading guide interprets the proof as adapting Stepanov's auxiliary polynomial method over finite fields to arithmetic geometry and automorphic forms. The proposed structure uses forced divisibility at inert primes, the Bost slope inequality to bound global cost, and iterated theta lifts to accumulate the signal and distribute the cost. A one-sided Riesz mean error is then passed to a windowed Landau theorem. This account is attributed to Pei.

Review the forced-divisibility steps `adm2` and `SelectionServed`, mean slope with frame defect, precise archimedean and main-term cancellation, uniform Selmer bound `WWin`, covolume `VolumeTheoremX`, and the interface between the weaker statements `RecTExists` and `RowOb` and their uses. Extract declaration types, instances, and proof terms to check denominators, constants, uniformity, and satisfiable hypotheses.

The abstract cost model `E(m)=Ax/m+Bm` balances around `m≈√(Ax/B)`. Use this as a heuristic for NSRW proof-search budgets, partitioning dependency checks, and allocating fixed and recurring costs. `math_patterns.py` implements the exact rational integer optimization. Its interpretation is limited to this cost model.

## 2. Gaps and verification checks

| ID | Risk | Consequence | Independent check | Status |
| --- | --- | --- | --- | --- |
| B01 | Reading imports as proof dependencies | Unused modules can be marked as essential | Elaborated `.type` and `.value` or export closure | `NOT_RUN` confirmed |
| B02 | Treating manuscript exposition as the Lean statement | The PDF may postdate the formalization | Reviewed correspondence of wording, quantifiers, units, hypotheses, and conclusions | OPEN |
| B03 | Missing bridge from finite kernel arithmetic to `WindowHypU` | Positivity only establishes a property of the integral | Lean bridge lemma and source-to-code fixture | OPEN |
| B04 | Counting `sorry` as a completeness check | Axioms present in an environment can differ from the theorem's dependencies | `#print axioms`, independent kernel, statement comparator | Some external runs, local check unrun |
| B05 | Unsatisfied assumptions of a conditional theorem | `P→Q` can hold without a constructed witness to `P` | Actual witness type and required constants | OPEN |
| B06 | Verifier uses the producer's algorithm | Both can share an error | Independent expression, alternate backend, and mutations | OPEN |
| B07 | High precision without error provenance | The 128, 200, or 320 bit setting gives only a precision budget | Rigorous remainder, outward dyadic rounding, and sign check | OPEN |
| B08 | A source update or patch lacks a rebuild | An older PASS can be attributed to new bytes | Rebuild each patch and run clean CI | OPEN |
| B09 | Six code cases and five saved results | Coverage drift | Python AST inventory versus JSON result keys | Discrepancy confirmed |
| B10 | Missing notebook execution counts and outputs | Reproduction instructions lack run evidence | Clean-run command, stdout, and digest receipt | Confirmed |
| B11 | Missing Git identity | Byte identity and commit provenance establish different facts | Git commit and clean checkout or content manifest | MCP Git unavailable |
| B12 | Transfer to physics without evidence | Similar equations do not establish domain validity | Units, baseline, experiment, and held-out test | Transfer unverified |

### B05. Satisfiability and hidden assumptions

The Lean kernel verifies the exact declared proposition. To apply `∀x, H(x)→Q(x)`, establish `H(x)` for the intended `x`. Record explicit and implicit binders, typeclass instances, witnesses to hypotheses, and documentation that omits a conditional. An impossible hypothesis can still yield a valid implication and prevent the desired application.

### B06. Levels of independence

- Repeating a function tests regression and repeatability along the same computation path.
- Reimplementing the same formula independently reduces implementation dependence and can share formula interpretation errors.
- A mathematically equivalent expression and a different numerical method reduce common failure modes further.
- Lean type and kernel replay checks formal consistency within its scope. Manuscript semantics and physical relevance require further review.
- Have a separate mathematician or domain expert assess the assumptions and correspondence to the intended application.

## 3. Mapping manuscript equations to formal claims

**Three connected sources of evidence**

```text
Original archive / Lean declaration --(term dependency, kernel replay)--> exact formal claim
            |                                                      |
            | source / line / hash                                | explicit assumptions
            v                                                      v
       PDF page & equation --(human checked semantic map)--> bridge-obligation graph
            |                                                      |
            | narrative / intuition                                | executable witness
            v                                                      v
        hypothesis registry --(falsifiers & counterexamples)--> runtime receipt
```

Assign an `Equation ID` that preserves symbols, formulas, quantifiers, and citation locations. Link the rendered page and equation to the Lean declaration type. A reviewer records `EXACT`, `ONE_WAY_IMPLICATION`, `CONDITIONAL`, `APPROXIMATION`, `NARRATIVE_ONLY`, or `UNMAPPED`. A proposed `EXACT` match is `UNVERIFIED` without a review record.

Read backward from the Lean goal to a small cut in the observed proof graph, the most substantial intermediate reduction, units and definitions, the relevant manuscript passage, any unsupported intuition, and a small counterexample or stress test.

**Research hypothesis.** Prioritize intermediate Lean lemmas whose removal disconnects the observed proof path and whose justification is short or absent in the manuscript. Use `MISSING_EXPLANATION_CANDIDATE` to mark a passage requiring human review.

### 3.1 Review priority

An example priority score is `4×semantic gap + 3×certificate absence + 2×dependency centrality + 2×fragile precision + 1×unreviewed assumptions`. Publish the weights and use the score solely for triage.

## 4. Verification plan for the original RH proof

### Track A: Formal verification

1. Pin the 14 original archive parts and merged digest, Lean v4.33.1, and the exact Mathlib revision.
2. Build a Mathlib-only `Challenge` statement and use an independent comparator against the `Main` result.
3. Collect `#print axioms` per theorem and check the declared dependencies against the allowlist. Record environment-wide `sorryAx` separately.
4. Run a clean Lake build, export declaration and term closures, and try `leanchecker` and `nanoda`. Record tool commits, host, exit code, memory, and output digests.
5. Check compiler trust dependencies such as `native_decide` where relevant. Record `noncomputable` separately.
6. Review the semantics of the types and faithfulness of Mathlib statements. Retain signed correspondence records.

Record the statement comparator and full proof checker as distinct modes. MIT's record includes declined or unsupported checks attributable to checker coverage.

### Track B: Mathematical strategy

1. Extract the actual declaration closure from `rhOfAll`.
2. Review the number-theoretic argument from the Riesz mean through a one-sided window inequality and a zero-free half-plane to GRH.
3. Compare the precise source assumptions for forced divisibility, slope bounds, quantitative theta lifts, Selmer bounds, and covolume.
4. Record uniformity ranges, signs, strict or non-strict inequalities, and limit order for small and large parameters.
5. Record the weakest assumptions supported by the argument and check where the proof supplies them.
6. Record `PROOF_STRUCTURE_RECONSTRUCTED`, `SOURCE_AGREEMENT_REVIEWED`, and `INDEPENDENT_MATHEMATICAL_ARGUMENT` only with evidence for each.

### Track C: Negative tests

- Statements. Change `≤` to `<`, remove denominator positivity, and try `k=0`, maximal `k`, and boundary parameters.
- Certificates. Lower precision, give a denominator interval containing zero, shift an endpoint, or flip an output bit.
- Sources. Change a digest pin or Mathlib version, or regenerate an import graph with a mismatched witness.
- Semantics. Extend a finite interval improperly to `Ioi 0`, or change a weak conclusion to a smooth one.
- Evidence. Attach an old success log to new code or mark an output-free notebook as executed.

Count a negative test as OE-4 evidence when the expected failure was fixed before execution and observed.

## 5. Potential NSRW applications

The 2026-10-05 E2A ledger recorded `strict L2` without a confirmed clean compile, `L3` open, and `DeltaM<0` and the repair zero held on upstream dependencies. Check the latest receipts before using these statuses for 2026-11-22.

- `C1`. Link paper or LaTeX equations, Lean theorem declarations, and NSRW numerical records in both directions.
- `C2`. Supplement `statement.lock` with `hypothesis.lock`, definition fingerprints, and local evaluator provenance. A changed definition or coercion needs a new identity even if the statement looks unchanged.
- `C3`. A high-precision witness for local `J` has local scope. Track `SAME_SOURCE_PROFILE_F`, `F_AMP_ETA_GT_9_OVER_10`, `EXACT_FIRST_WINDOW_LOCAL_MASS_ZERO`, and the missing Lean wrapper individually.
- `C4`. Connect rigorous remainder, exact dyadic enclosure, and Lean bound proof. A numeric record alone leaves the transcendental remainder obligation open.
- `C5`. Test a regular benchmark such as Taylor–Green and check precision and resolution drift before extending a local experiment. At TR-3 compare equal-cost baselines such as residual, CFL, and divergence tests.

The Alpöge–Buckmaster 2026 Navier–Stokes project and NSRW's OpenAI 2026 source use different problems, materials, and methods. The authors' README says the public Lean package omitted Appendix B certificate data and the 128-bit Arb/FLINT verifier, and a full rebuild after a cell-layer patch was unconfirmed at that time. Some aspects of the stronger paper conclusion, including closeness to a candidate and smoothness of the profile, fall outside the formal statement. For NSRW, study the conditional proof interfaces `CertificateChallenge → ExtendedCertificateChallenge → CellLayerChallenge → Solution`.

## 6. Mathematical models and physical predictions in TOE

The workspace did not contain the complete TOE scrutiny suite. The following work is proposed.

Evaluate each TOE hypothesis through five independent checks.

1. **Formal theory.** Pin the action, field equations, parameters, symmetries, admissible domain, dimensions, units, gauge, and coordinate conventions.
2. **Limiting theory.** Derive the claimed Newtonian, SR, GR, or QM predictions with the relevant cross terms, limit order, and singular limits.
3. **Computational prediction.** Derive the observable, uncertainty budget, and solver validity from the theory. Measure convergence separately from physical agreement.
4. **Empirical comparison:** measured dataset ID, instrument/selection assumptions, likelihood, residual, named baseline, held-out data, prior registration.
5. **Falsification.** Test gauge and unit changes, perturbations, instrument systematics, out-of-domain inputs, degeneracy, and identifiability.

`navier_stokes_unit_guard` in `math_patterns.py` checks that `u_t`, convection, the kinematic pressure gradient, and `ν Δu` each have units `L/T²`. It detects a viscosity dimension mutation. A TOE adaptation could use an SI dimension vector per argument and a gauge-invariance check.

Choose one concrete model, equation, and parameter set. Test dimensions, a limiting case, reproducible numerics, a baseline comparison, and falsification end to end.

## 7. Implemented package and test scope

`e2a_proof_atlas.zip` uses the Python standard library, supports Windows, and reads the source root without changing it. Outputs go elsewhere.

- `e2a_atlas/audit.py` checks source digests, PDF catalog identity, optional 14-part archive replay, Lean lexical content, optionally reachable nodes in the 85 MB import DAG, open obligations, and case inventory.
- `e2a_atlas/semantic_graph.py` analyzes declaration-level type and value graphs produced by an external elaborator or exporter. The provided example is synthetic.
- `e2a_atlas/math_patterns.py` implements exact rational integer optimization for `Ax/m+Bm` and a minimal Navier–Stokes dimensional check.
- `spec/riemann_nsrw_toe_2026-11-22.json` covers RH, NSRW, the new NS2026 project, and TOE with open obligations and observed local source pins.
- `tests/test_audit.py` covers digest drift, misleading tokens in comments, static and kernel evidence, archive mutation, open bridges, path traversal, case discrepancies, exact budgets, and dimension mutation.
- `README.md` provides commands to copy, test, and run the package.

The package passed **13/13 unit tests** in a separate environment. The complete runner in the Windows workspace, Lean build, and human review of PDF equations were unrun. The recorded OE evidence covers package development tests.

### PowerShell commands

```powershell
# Run in the extracted e2a_proof_atlas directory.
python -m unittest discover -s tests -v
$Root = 'D:\Sanctum\research-sidequests\riemann-lean-2026-11-22'
python -m e2a_atlas --root $Root --spec spec/riemann_nsrw_toe_2026-11-22.json --out .\audit-preflight.json
# Hashing all archives rereads about 239 MB without modifying the source.
python -m e2a_atlas --root $Root --spec spec/riemann_nsrw_toe_2026-11-22.json --archive-manifest docs/evidence/source-index/lean-archive-manifest.json --import-graph rh-import-graph.json --out .\audit-fullstatic.json
```

The audit preflight writes one file. `source_pin_ok` records byte identity, `HELD` under `bridges` records an unsupported or unconfirmed connection, and `case_inventory` records test coverage status.

## 8. Three proposed experiments

### Experiment E1 — Landau finite-window correspondence

Inputs are the pinned `landau_window_ineq` declaration, `window_kernel.py` integral, and PDF page. Produce a variable correspondence, one Lean bridge goal, a proof-free `Challenge.lean`, an independent analytic remainder, and a three-way test. Require a kernel-checked finite-integral bound with the necessary `σ>2`, `a<b`, and `rate*b≤16` assumptions. Scope the result to that bridge.

### Experiment E2 — NSRW MB06 Falsifier Gate

Use fixed `λ`, the reference ratio record, and an exact rational bracket. Produce an independent expm1 interval algorithm or equivalent expression, ±1e−9 mutation tests, a receipt, a one-command verifier, and a statement of the local `J` boundary. Require clean secondary reproduction of baseline PASS, shifted FAIL, and exhausted-precision UNRESOLVED. Source profile existence, strict L2/L3 closure, and the PDE theorem remain separate obligations.

### Experiment E3 — TOE one-observable vertical slice

Pin one TOE equation or action, field and unit schema, source or commit, and baseline. Produce a limiting-case derivation, dimension and gauge checks, numerical verification, held-out observable comparison, and negative result. Require a reproducible advantage over the named baseline under preregistered criteria or record failure.

## 9. E2A decision rules

Use the status conventions in `E2A_RESOURCE_STAGE_CROSSWALK.md`.

- `R0/R1` pins the original source and exact hypotheses and statement.
- `R2` defines the bridge, expected failures, and counterexamples.
- `R3/OE-2` records a bounded executed artifact with exact environment and receipt.
- `R4/OE-3` requires clean replay by a separate operator.
- `R5/OE-4` requires observed failure under the declared mutation or assumption change.
- `R6/TR-0` extracts a reusable primitive with its upstream provenance.
- `TR-1` through `TR-6` cover domain mapping, controlled transfer, preregistered comparison, prototype, domain validation, and operational feasibility.

Record formal acceptance, mathematical understanding, numerical verification, and application validity with their own evidence.

## 10. Primary and directly inspected sources

- Levent Alpöge, announcement: https://alpo.ge/remark.pdf (2026-11-20)
- Lean/Mathlib joint statement: https://leanprover-community.github.io/blog/posts/riemann-hypothesis/ (2026-11-21)
- Andrew Sutherland's MIT verification log records status by checker mode. https://math.mit.edu/~drew/grh/
- RH community comparator: https://github.com/leanprover-community/riemann-hypothesis
- Yan Ru Pei's roadmap provides an expository analysis. https://peabrane.github.io/files/pei-2026-claimed-lean-proof-rh-roadmap.pdf
- Alpöge–Buckmaster NS source & Lean README: https://github.com/tristanbuckmaster/navier-stokes
- Source pin in project: `sources.json` + `lean-archive-manifest.json` + `rh-proof-trace.json`
- NSRW existing source ledger: `E2A_RESOURCE_CLAIM_LEDGER.yaml`, `E2A_RESOURCE_STAGE_CROSSWALK.md`

### Scope of the study

Trace the exact Lean type, mathematics explained in the PDF, Python interval, externally certified inequality, and measured phenomenon, and identify the evidence and assumptions at each step. A transferable computational idea must survive a comparison in its target setting.
