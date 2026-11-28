# When Verification Hits a Wall: From Equation to Artifact to Proof Composition

Research methodology and case study, first recorded November 27, 2026.

**November 28 replay update.** Colab recompiled the pinned Masullo theorem and applied
it to the archived GRH premise under Lean 4.36.0. The premise also matched under
4.33.1. The full composition with Alpöge's proof remains AMBER at the shared
import closure. The sections below preserve the original investigation and proposed
methodology. [Current source, Lean output, and blockers](masullo/RH_PROOF_COMPOSITION_REPLAY.md)

## Abstract

A reproducible calculation can be correct, well tested, and rigorously enclosed without resolving the mathematical obligation that motivated it. The Riemann Evidence Atlas encountered precisely this distinction in its investigation of weighted S-local traces in Alessandro Maria Masullo's alternative approach to the generalized Riemann hypothesis (GRH). A sequence of increasingly disciplined Galerkin, primal–dual, and ball-arithmetic experiments established local bounds but did not certify the infinite-dimensional trace ordering or the joint cutoff limit. The first nonconstant Fourier pair alone produced a valid error bound more than 86 times the remaining budget.

Rather than treating further numerical refinement as the default next step, we examined existing formal proofs as reusable mathematical artifacts. The archived Alpöge Dirichlet GRH theorem and an independently developed rational exterior-zero reduction in the RiemannMasullo repository expose matching proposition-level interfaces. Their composition would discharge a specific exterior-zero obligation over the rational field, without resolving the unrelated geometric trace comparison. A local conditional Lean bridge has already replayed; a common-environment composition has not.

This case motivates a custody-first research workflow: discover verified proof assets, match their mathematical interfaces, prove any missing adapters, compose the proof terms, and certify the original target under an audited dependency closure. This is an extension of Equation to Artifact, not a claim of a new RH proof or a new invention of theorem reuse.

## 1. The research wall: correct evidence is not sufficient evidence

The original research question was not whether a finite matrix could be evaluated accurately. It was whether the weighted quotient trace and its unfolded geometric expression could be compared under simultaneous spatial and frequency cutoffs, with the missing limiting and diagonal steps made explicit.

The investigation delivered several results worth preserving:

- NR-01: schedule dependence of a specified **unfolded two-sided Fourier integral**, not of the actual weighted quotient trace.
- NR-02: failure of a product-norm frequency mask to preserve the full Schwartz–Bruhat space for a concrete input.
- An analytic construction of the fixed-cutoff weighted trace, a characterization of the surviving origin condition, and a decomposition of the upper/lower frequency and rank-one correction terms.
- Reproducible finite-space diagnostics and certified bounds for selected projection residuals.

The evidence is recorded in [1–5]. The later numerical path, however, encountered a quantitative obstruction to the *sufficiency of its certificate*.

| Fixed model: L = 4, α = 1/8, 128 cells, period 2 | Evidence |
| --- | ---: |
| Observed finite-matrix difference between schedules | 1.2054450173 |
| Certified constant Fourier term error bound | 0.4503 |
| Remaining budget scale before other errors | 0.7551450173 |
| Certified first conjugate Fourier pair error bound | 65.23790 |
| First-pair bound / remaining budget | approximately 86.39 |
| Signed 128→256-cell change, base quadrature | +0.038461 |
| Signed 128→256-cell change, refined quadrature | +0.041547 |

The coefficient enclosure 2.02129 < |c₁| < 2.02253 and the first-pair bound are accepted within the recorded model. The 160-bit python-flint 0.9.0 result replayed byte-identically on Windows and Colab Linux. The signed finite-space diagnostic also replayed across platforms. The two numerical environments used the same algorithmic method; this is not independent mathematical validation by a different algorithm. The accompanying Lean declarations verify selected projection and arithmetic implications, not the whole Arb integration or infinite-dimensional trace.

The bound is much larger than the budget, but it is **not a lower bound on the actual error**. The signed finite-space changes show cancellation, but do not certify cancellation beyond 256 cells. The finite-matrix gap itself also has numerical uncertainty. Neither a false trace theorem nor a failed RH claim follows from these observations.

This is the turning point: the checked implementation and its narrow certificates were functioning as intended, yet the chosen sufficient-condition strategy did not close the target. We should not describe an incomplete mathematical model as perfect merely because all regression tests pass.

**Research decision:** preserve the results and suspend indiscriminate Galerkin enlargement. Resume numerical experiments when they test a precise new lemma, counterexample, or demonstrably tighter certificate. Before committing more computation, search the existing proof corpus for a route to the specific remaining obligation.

## 2. The conceptual shift: proofs as typed, reusable assets

Equation to Artifact originally emphasizes custody of a checkable claim: its source, computation, expected output, environment, and boundary. The next step is to treat a formally checked theorem as an asset with an explicit mathematical interface.

Under the propositions-as-types interpretation, a proof of A is a term of type A, and a proof of A → B is a function on proof terms. Given a : A and f : A → B, the application f a has type B. More generally, the following illustrates proof composition:

~~~lean
theorem proofComposition {A B C : Prop}
    (a : A) (f : A → B) (g : B → C) : C :=
  g (f a)
~~~

This small example is explanatory, not a new replay receipt.

The engineering analogy is useful but must remain precise:

| Software engineering | Formal mathematical engineering |
| --- | --- |
| External library | Checked theorem and its dependency closure |
| Function signature | Elaborated proposition, parameters, and hypotheses |
| Interface adapter | A proved implication, equivalence, or transport lemma |
| Dependency resolution | Definitions, instances, proof-value references, axioms |
| Patch | A proof term discharging an unchanged obligation |
| Compilation and validation | Elaboration, kernel checking, and custody audit |
| Regression control | Rejection of altered goals, missing hypotheses, or forbidden dependencies |

A proposition may be proved using classical choice without supplying an executable numerical witness. Proof terms in Prop are generally erased in ordinary runtime computation. Therefore a Lean theorem is not automatically a numerical algorithm, a simulator, or a deployable application. It is a reusable logical asset. Extracting a constructive algorithm or transferring a result to a physical model requires separate evidence.

The proposed extension is **Artifact to Proof Composition (A2PC)**: convert a verified source theorem into an audited dependency of another mathematical result. The phrase *Proof Artifact Custody* describes the supporting discipline, not a claim to invent Curry–Howard, premise selection, or library-based theorem proving.

## 3. The RH case: a concrete interface match

### 3.1 Preserve the two source roles

Source A is the archived Alpöge RH/Dirichlet GRH formalization, with external verification records from MIT and the Lean/Mathlib community [6–8]. The theorem of interest is not merely the RH endpoint but the stronger, directly reusable right-half-plane statement in the local archived [rh-Main.lean](https://math.mit.edu/~drew/grh/#what-was-verified):

~~~lean
theorem LFunction_ne_zero_of_half_lt_re :
    DirichletLNonvanishingRightOfHalf := allChi
~~~

The proposition in [rh-Statements.lean](https://math.mit.edu/~drew/grh/#what-was-verified) is:

~~~lean
∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
  1 / 2 < s.re → (χ ≠ 1 ∨ s ≠ 1) →
    DirichletCharacter.LFunction χ s ≠ 0
~~~

Source B is the Masullo formalization, pinned for this comparison at commit
`6dfe34ef2ef48f1f2c2cfd2274b73663a0eac07c`. Its [RationalExteriorZeros.lean](https://github.com/mccorvie/riemann-masullo/blob/6dfe34ef2ef48f1f2c2cfd2274b73663a0eac07c/RiemannMasullo/Ch13_ZerosHecke/RationalExteriorZeros.lean#L648) contains the public theorem
`traceFormula_exteriorZeros_rat_of_dirichletGRH`.
The locally expanded GRH premise in that file matches Source A's proposition at the source level, including the positive modulus and exceptional point guard.

This is a specific logical interface match, not merely a resemblance between two papers using theta functions or Fourier analysis.

### 3.2 The upstream adapter already exists

The rational exterior-zero reduction includes the following relevant declarations [9,10]:

| Declaration | Mathematical responsibility |
| --- | --- |
| `exists_primitive_finiteHeckeL_eq_of_trivial_on_section` | Classify rational idelic characters trivial on a norm section by primitive Dirichlet characters, with equality of finite L-series for Re s > 1. |
| `meromorphicOrderAt_finiteHeckeL_continuation` | Transport meromorphic order through continuation and a nonvanishing archimedean factor in Re s > 0. |
| `order_nonpos_of_half_lt_re` | Exclude positive completed divisor orders on the right using Dirichlet GRH. |
| `isEmpty_exteriorZeros_of_dirichletGRH` | Use the right-half result and functional-equation reflection to exclude exterior zeros; the declaration is private. |
| `traceFormula_exteriorZeros_rat_of_dirichletGRH` | Provide the exterior-zero sum result over ℚ under the explicit GRH hypothesis. |
| `traceFormula_exteriorZeros_rat_iff_dirichletGRH` | Record the equivalence of the universally quantified rational obligation and Dirichlet GRH. |

Let A denote the exact Dirichlet nonvanishing proposition and B the rational exterior-zero cancellation statement, including the norm-section and test-function hypotheses in the upstream target. The planned composition is:

~~~text
Alpöge proof       a : A
Masullo reduction  f : A → B
--------------------------------
Candidate patch    f a : B
~~~

The target B is, for every admissible norm section τ, test φ vanishing on the norm-one classes, and half-width α > 0, the assertion that the exterior zero terms have sum zero. In particular, the exterior index is defined using positive completed divisor order and α ≤ |Re s − 1/2|; equality at the strip boundary is not discarded.

If the two proof terms can be joined under compatible definitions, instances, and accepted axioms, the composition supplies B for all admissible tests and positive widths. It requires no numerical enumeration of zeros or Fourier residuals.

### 3.3 What was checked locally, and what was not

The existing [RH_EXTERIOR_ZERO_BRIDGE.md](masullo/RH_EXTERIOR_ZERO_BRIDGE.md) records a local conditional test. The three declarations in [E2ADirichletExteriorBridge.lean](../tests/lean/E2ADirichletExteriorBridge.lean) passed on Colab with Lean 4.33.1 and pinned Mathlib. They prove emptiness and HasSum zero under explicit strip and zero-transfer hypotheses and include a synthetic boundary countermodel. The original source proposition body was recompiled with narrowed imports.

The earlier extraction receipt identifies the stored type of `LFunction_eq_zero_re` and its direct proof-value reference `claimAll`. The right-half-plane theorem above is the preferred interface for the next composition; its source is directly available. The separate original-object extraction of that preferred theorem was reported in the subsequent investigation, but this methodology record does not supply a new receipt for it.

| Evidence item | Status as of this document |
| --- | --- |
| Original archived statements and preferred right-half-plane theorem source | Observed |
| Upstream rational reduction and expanded input proposition at pinned revision | SOURCE MATCHED |
| Local conditional bridge (three declarations, Colab) | CONDITIONAL PASS |
| Original RH proof full local kernel replay | NOT_RUN |
| Upstream target transitive axiom/dependency audit in our environment | PENDING |
| Single-environment composition of both original proof assets | AMBER |
| S-local joint limits and geometric quotient comparison | OPEN |
| Hecke GRH over arbitrary number fields | Not established by this composition |

The environments differ: Alpöge uses Lean 4.33.1 and the pinned Masullo repository uses Lean 4.36.0. Direct reuse of incompatible compiled objects is not justified. A shared toolchain may require porting and rechecking a substantial dependency closure. A source-level statement match plus separate replay receipts is valuable evidence but is not a single-kernel composed proof.

## 4. Why the method matters for mathematical AI engineering

The central benefit is **obligation-level search before proof generation or numerical escalation**. A research agent should ask whether the required conclusion is already implied by a verified theorem before attempting to manufacture another approximation or derivation.

An external theorem can replace a difficult proof obligation only if the interface is mathematically correct. Missing assumptions become explicit adapter targets. A mismatched normalization becomes a transport lemma. A nonconstructive result remains a logical result rather than a fabricated algorithm. A circular dependency is rejected even if its surface syntax compiles. This gives the AI system a structured failure signal.

There are three distinct forms of progress:

1. **Reuse:** a known theorem resolves a compatible target without reproving the original result.
2. **Adaptation:** a new verified lemma transfers a result across definitions, domains, or assumptions.
3. **Discovery:** a genuinely new mathematical conclusion or technique is established, with novelty assessed against prior work.

The first two are valuable engineering even when the consequence is already known. The third requires a separate novelty claim and expert review. No one should confuse a successful library integration with a newly discovered theorem.

For this case, the exterior-zero obligation is a different node from the weighted trace comparison. The new path does not make the failed numerical certificate stronger. It identifies a logical route around a different obligation that had been motivating the investigation. That distinction is exactly what dependency-aware research planning should preserve.

## 5. Proposed E2A Proof Artifact Composer

The following is a design proposal, not an implemented or benchmarked product.

~~~text
Source theorem + proof object + provenance
                    |
                    v
          Proof Artifact Registry
                    |
Internal AMBER --> exact obligation and context
                    |
                    v
       premise retrieval / candidate ranking
                    |
                    v
   semantic interface check + dependency analysis
                    |
          missing assumptions? ----> adapter goals
                    |                     |
                    +<--------------------+
                    |
                    v
           candidate proof patch
                    |
                    v
     kernel replay + custody + goal identity gate
                    |
             ACCEPT / HOLD / REJECT
                    |
                    v
        reusable proof artifact, if accepted
~~~

The registry must distinguish module imports from direct theorem-type and proof-value references, and those from transitive closure. The existing [proof dependency pilot](PROOF_DEPENDENCY_PILOT.md) is a useful precursor.

A minimal artifact record should carry the source URI, author attribution, source revision, content digests, declaration name, elaborated proposition, assumptions, definitions and instances, proof dependencies, axiom policy, toolchain lock, replay command, evidence receipt, provenance track, nonclaims, and outstanding obligations. A graph edge should express a specific verified implication or transport, not an AI-generated similarity score.

Retrieval can combine lexical search, embedding-based search and type-directed matching; its output is a candidate, never an accepted proof. An adapter can be generated by an AI system or written by a mathematician, but must be checked against the unchanged target. The verification stage must be isolated from untrusted candidate code and must reject bypasses of kernel checking.

The core computation is not the claim of novelty. The contribution is the custody: isolating the exact claim, preserving the source and pinned verification environment, and making the boundary inspectable. The same principle applies when the artifact is a proof rather than a numerical computation.

## 6. Admission and promotion policy

| Gate | Required evidence | Failure or unresolved state |
| --- | --- | --- |
| P0 — DISCOVERED | Exact source and declaration locator | Candidate only |
| P1 — PINNED | Immutable revision, content hashes, attribution and toolchain | Block on drift |
| P2 — MATCHED | Reviewed propositions, quantified parameters, definitions and exceptions | AMBER for a semantic mismatch |
| P3 — BRIDGED | Checked adapters; every remaining assumption listed | CONDITIONAL PASS if any obligation remains |
| P4 — COMPOSED | Original target elaborates and the actual proof terms compose in a compatible environment | AMBER if only separate replays exist |
| P5 — AUDITED PASS | Clean replay, unchanged trusted statement, transitive axioms/dependencies, no prohibited assumptions or cycles | REJECT if trust policy fails |

These proposed proof-composition gates do not replace the project's existing artifact-to-application transfer gates or operational evidence levels. A proof result does not automatically pass a domain-transfer or deployment gate.

Required negative controls include altered target statements, changed exceptional-point guards, missing transfer hypotheses, incompatible toolchains, and reliance on the unresolved target itself. The existing synthetic boundary countermodel is an example of testing the necessity of an assumption. A checker must reject attempts to turn AMBER into PASS by weakening the target, adding a disguised axiom, using sorryAx, or substituting an unverified proof object.

Axiom inspection with #print axioms is required for the composed endpoint; source-text searches for sorry are insufficient. Axiom-free appearance alone does not establish that the formalized proposition faithfully represents a paper's intended claim.

## 7. Two tracks, no provenance laundering

**Track A — Independent manuscript investigation.** Continue to investigate the Masullo geometric trace route without using results derived from the November 2026 RH formalization. Preserve NR-01 and NR-02, the fixed trace construction, and open issues #7353 and #7354. The upstream repository explicitly excludes November 2026 RH-formalization-derived contributions [11].

**Track B — External-result-dependent proof composition.** Reuse the existing GRH theorem with explicit attribution to its authors and use the rational reduction from its own pinned upstream source. Maintain separate proof dependencies, receipts, and claims. Do not submit this composition as a repair of the independent manuscript proof.

The global exterior-zero problem #5571 remains open in its general upstream scope. The rational specialization can be addressed by a known external result; this cannot validate the missing geometric kernel, global-to-local comparison, joint cutoff limit, or arbitrary-number-field GRH.

This separation protects the intellectual value of both research programs. It is also a reproducibility requirement: the dependency graph must show which conclusion relies on which source.

## 8. Immediate research action and evaluation

The next bounded experiment should target the existing public rational reduction rather than rebuilding character classification from scratch.

- Pin the preferred original theorem and the exact upstream source; obtain a dedicated original-object reference receipt for the preferred endpoint if not already available.
- Check the upstream rational reduction and its equivalence theorem using the pinned toolchain. Audit the transitive dependency closure for the unresolved exterior-zero theorem, sorryAx and other disallowed dependencies.
- Compare the elaborated GRH propositions and definition closures, including the guard at s = 1. Assess the smallest viable common-environment port. Do not claim binary compatibility.
- If the composition replays, publish the unchanged target, actual composed declaration, axiom report, source hashes and repeatable command. If not, record the precise blocker and retain AMBER.

Compare this approach against a baseline that attempts the same *logical obligation* without external theorem retrieval. Measure successful closures, kernel-accepted patches, false promotions, adapter effort, compute and human time, and retained hypotheses. Do not compare the cost of proving exterior-zero cancellation against a different task such as geometric trace convergence as though they were identical.

A positive result would demonstrate a concrete cross-project proof-reuse workflow. A negative result would reveal a specific semantic, dependency, or toolchain obstacle. Both outcomes are useful if preserved in a replayable record.

## 9. Position relative to prior research

Mathlib is already a large reusable mathematical library. LeanDojo and ReProver established premise retrieval and retrieval-augmented theorem proving as research directions [12,13]. Lean's reference manual describes its dependent type theory, kernel and proof-validation mechanisms [14,15]. We do not claim to originate these methods.

The proposed E2A emphasis is narrower: **cross-project proof artifact custody, explicit obligation repair, and evidence-gated promotion**, connected to reproducible numerical research and negative-result registers. Its distinctive value is a hypothesis to test, not an established superiority claim.

## 10. Closing principle

The original work established which pieces of a difficult trace computation could be isolated, reproduced and bounded. Its failure to meet the final certificate budget is not a reason to discard that evidence. It is a reason to change the question and choose a better mathematical route.

A verified theorem should be treated neither as an untouchable final answer nor as an interchangeable snippet of code. It is a typed mathematical dependency with provenance, assumptions, and a trust boundary.

**From Equation to Artifact. From Artifact to Proof Composition. From a checked composition to the next checkable claim.**

The original mathematics belongs to its authors. Flamehaven's proposed contribution is the disciplined custody of the connection, including the exact point at which it succeeds or fails.

## References and reproducibility anchors

Local references are relative to this document. Public GitHub links used for the concrete interface comparison are commit-pinned. General project and documentation pages are contextual sources, not immutable build inputs.

1. Riemann Evidence Atlas, [Negative Results for the S-Local Trace Comparison](masullo/NEGATIVE_RESULT_REGISTER.md), NR-01 and NR-02.
2. Riemann Evidence Atlas, [Fixed-cutoff weighted quotient trace](masullo/S_LOCAL_WEIGHTED_QUOTIENT.md) and [trace decomposition](masullo/S_LOCAL_TRACE_SPLIT.md).
3. Riemann Evidence Atlas, [Galerkin diagnostics](masullo/S_LOCAL_LOW_GALERKIN.md), [constant term](masullo/S_LOCAL_CONSTANT_TERM.md), and [first Fourier pair](masullo/S_LOCAL_FIRST_HARMONIC.md).
4. Riemann Evidence Atlas, [160-bit first-pair certificate](masullo/s-local-first-harmonic-160.json), SHA-256 `17e012ea858da50f3d930e0b54a9724e87254f523d8e2dbac6e98d43a0b95c81`; [cross-platform Arb receipt](masullo/s-local-first-harmonic-colab-arb-replay.json); [nested diagnostic receipt](masullo/s-local-first-harmonic-colab-nested-replay.json).
5. Riemann Evidence Atlas, [A Dirichlet GRH Bridge for Exterior Zeros](masullo/RH_EXTERIOR_ZERO_BRIDGE.md), [conditional Colab receipt](masullo/dirichlet-exterior-bridge-replay.json), [original declaration references](masullo/dirichlet-exterior-original-references.json). Bridge source SHA-256 `62b2c5168ec2d8caad55815c26fc25b146e4f1fd49ed035aee8ece259175bafd`; archived statements SHA-256 `79ef7ca776e42abe1f46caee13ea09bd19f1e2d0b1620d8d5d200258f33b47bf`; pinned Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`.
6. Levent Alpöge, [announcement / research record, 20 November 2026](https://alpo.ge/remark.pdf); local archived [Main](https://math.mit.edu/~drew/grh/#what-was-verified), [Statements](https://math.mit.edu/~drew/grh/#what-was-verified) and [MIT audit log](https://math.mit.edu/~drew/grh/audit.log). Preserved Main.olean SHA-256 `9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad`.
7. Andrew V. Sutherland, [RH/GRH independent verification record](https://math.mit.edu/~drew/grh/). Cited through the preserved Atlas source and audit records; no fresh external kernel replay in this document.
8. Lean FRO and Mathlib Initiative, [joint statement on the Riemann hypothesis](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/).
9. RiemannMasullo contributors, [RationalExteriorZeros.lean](https://github.com/mccorvie/riemann-masullo/blob/6dfe34ef2ef48f1f2c2cfd2274b73663a0eac07c/RiemannMasullo/Ch13_ZerosHecke/RationalExteriorZeros.lean), especially lines 539, 569–653 and 768–775. Git blob `f41e51e00f6541855c1d87fdbb8f4506d82909f3`. [Pinned Lean toolchain](https://github.com/mccorvie/riemann-masullo/blob/6dfe34ef2ef48f1f2c2cfd2274b73663a0eac07c/lean-toolchain).
10. RiemannMasullo contributors, [Targets.lean, order comparison](https://github.com/mccorvie/riemann-masullo/blob/6dfe34ef2ef48f1f2c2cfd2274b73663a0eac07c/RiemannMasullo/Ch13_ZerosHecke/Targets.lean#L72); [exterior index and open-strip proof](https://github.com/mccorvie/riemann-masullo/blob/b343e185c4296c7691cd86bb58ea3fd6e0b7aa61/RiemannMasullo/Ch12_TraceGeometric/Sec5.lean#L67).
11. RiemannMasullo, [research and contribution policy](https://github.com/mccorvie/riemann-masullo), [#5571 exterior zeros](https://github.com/mccorvie/riemann-masullo/issues/5571), [#7353 global/local comparison](https://github.com/mccorvie/riemann-masullo/issues/7353), [#7354 quotient kernel](https://github.com/mccorvie/riemann-masullo/issues/7354).
12. The Mathlib Community, [Mathlib4](https://github.com/leanprover-community/mathlib4).
13. Kaiyu Yang et al., *LeanDojo: Theorem Proving with Retrieval-Augmented Language Models*, NeurIPS 2023, Datasets and Benchmarks Track. [arXiv:2306.15626](https://arxiv.org/abs/2306.15626), [proceedings](https://papers.neurips.cc/paper_files/paper/2023/hash/4441469427094f8873d0fecb0c4e1cee-Abstract-Datasets_and_Benchmarks.html).
14. Lean, [The Lean Language Reference](https://lean-lang.org/doc/reference/latest/).
15. Lean, [Validating a Lean Proof](https://lean-lang.org/doc/reference/latest/ValidatingProofs/).

**Document custody note:** This document synthesizes existing local evidence, the inspected pinned upstream declarations, and a proposed research workflow. It does not record a new Lean compilation, Arb integration, full proof replay, independent peer review, or measured performance improvement. No existing status has been promoted to unconditional PASS by writing this document.
