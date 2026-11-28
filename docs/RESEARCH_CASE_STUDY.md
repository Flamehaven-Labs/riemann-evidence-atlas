# Reading an AI-assisted proof through its Lean declarations

Riemann Evidence Atlas follows two related lines of research. Levent Alpöge's AI-assisted
Lean formalization proves RH and the Dirichlet L-function statements recorded in its
independent audit. Alessandro Maria Masullo's draft pursues Hecke GRH through a trace
formula, and a separate formalization project records results and unresolved steps.
Atlas compares individual arguments and preserves the evidence needed to check them.
[Alpöge verification](https://math.mit.edu/~drew/grh/) ·
[Masullo formalization and errata](https://github.com/mccorvie/riemann-masullo)

## What carried over from QSOT and NSRW

| Prior work | Use in Atlas |
| --- | --- |
| QSOT-Harness assigns evidence classes to model outputs and records which checks actually ran. | Atlas applies the same reporting discipline to mathematical statements, numerical bounds, proof replay, and missing evidence. Its standalone runs require no QSOT dependency. |
| Navier–Stokes Research Workbench pairs source-bound Lean statements with exact numerical enclosures and replay receipts. | Atlas adapts the NSRW rational interval and verification modules. It uses them on the Landau tail and keeps the exact theorem, numerical interval, and runtime result together. |
| Atlas's Lean declaration inspection | Atlas adds a comparison between the type of a theorem, the constants used in its proof, and the modules imported by its source. This lets a researcher trace the part of the proof that can answer a specific question. |

[QSOT-Harness](https://github.com/Flamehaven-Labs/QSOT-Harness) ·
[NSRW research verification](https://github.com/flamehaven01/NavierStokes-Research-Workbench/blob/main/docs/NSRW_RESEARCH_VERIFICATION.md) ·
[Exact code attribution](../NOTICE.md) · [Proof-reference pilot](PROOF_DEPENDENCY_PILOT.md)

The audit starts with a fixed mathematical claim. For a numerical claim, preserve the
input, enclosure, threshold, and rejection control. For a Lean claim, read the declaration
type and its assumptions, then record the proof references and compile in a pinned
environment. When a theorem from another project matches an open obligation, attempt the
application with the original target intact and inspect the compiled declaration's axiom
dependencies. Use ACCEPT for evidence that supports the stated claim, AMBER for an open
check, and REJECT for an inference that the evidence rules out. [Verification specification](CROSS_REPO_WORKFLOW_AND_VERIFICATION_SPEC.md)

## Where the investigation changed direction

The Masullo draft is 940 pages. The original Alpöge development has 175,187 Lean modules.
The independent audit also describes a shorter formalization. Even with kernel verification,
a reader still needs to know which assumption a proof uses and which theorem gives the
crucial step. Atlas approaches that reading task by working backwards from one named
obligation. [Masullo source inventory](masullo/README.md) ·
[Original proof audit](https://math.mit.edu/~drew/grh/) · [Shorter proof audit](https://math.mit.edu/~drew/shortgrh/)

In the geometric trace investigation, the certified first Fourier pair error bound was
65.23790 against a remaining budget of 0.755145. This rejects the sufficiency of that
certificate. The actual signed error and the weighted quotient's joint limit remain open.
We then revisited the list of proof obligations and found a direct theorem application
for the separate exterior-zero question. [First Fourier pair](masullo/S_LOCAL_FIRST_HARMONIC.md)

Alpöge's `LFunction_ne_zero_of_half_lt_re` supplies right-half-plane nonvanishing.
The pinned Masullo formalization takes the same proposition, with the same guard at
`s = 1`, to show exterior zero terms sum to zero over the rationals for the stated
norm section, test function, and positive strip width. Lean checked the expanded premise
in 4.33.1 and 4.36.0. Colab rebuilt the Masullo target and compiled a conditional application
to that premise. Its axiom audit lists `propext`, `Classical.choice`, and `Quot.sound`.
The run that would supply the actual Alpöge proof in the common environment remains blocked
at the original import closure. [Upstream Lean theorem](https://github.com/mccorvie/riemann-masullo/blob/6dfe34ef2ef48f1f2c2cfd2274b73663a0eac07c/RiemannMasullo/Ch13_ZerosHecke/RationalExteriorZeros.lean#L648) ·
[Atlas Lean application](evidence/rational-exterior/ConditionalApplication.lean) ·
[Proof and import logs](masullo/RH_PROOF_COMPOSITION_REPLAY.md)

## What a reader can verify today

- Lean certifies two fixed Landau tail integrals and their numerical enclosures.
  A close threshold in the second case is unresolved at 128 bits and certified at
  256 bits. [Second Landau case](LANDAU_SECOND_CASE.md)
- The unfolded two-sided Fourier calculation has different limits for the balanced
  and quadratic cutoff schedules. A separate example shows that the product-norm
  frequency mask can leave the stated Schwartz–Bruhat domain.
  [Two negative results](masullo/NEGATIVE_RESULT_REGISTER.md)
- The fixed-cutoff weighted quotient has an integrable trace density in the studied
  trivial-angular sector. Its identification with Step III and its simultaneous
  cutoff limits remain open. [Weighted quotient](masullo/S_LOCAL_WEIGHTED_QUOTIENT.md)

For AI and software researchers, this case exposes concrete tasks that can be measured
without solving the full problem. Can a system retrieve a theorem with the right
hypotheses, reject a changed normalization, distinguish a missing import from a failed
proof, and preserve the evidence for its decision? For mathematicians, the same records
point to a precise next question. The roadmap starts with the Step III operator at
fixed cutoffs, then targets the signed low-frequency contribution on a moving window
if the source comparison permits that schedule. [Next research steps](ROADMAP.md#next-research-question) ·
[Detailed proof-composition case study](WHEN_VERIFICATION_HITS_A_WALL_PROOF_ARTIFACT_COMPOSITION.md)

## Related reading

- NSRW Part 1 follows the mass cancellation and the positive angular history at the same radius. [When One Moment Cancels and Another Stays Positive](https://flamehaven.space/writing/navier-stokes-research-workbench-when-one-moment-cancels-and-another-stays-positive/)
- NSRW Part 2 follows a rejected hypothesis, missing evidence, and a Lean repair. [A Rejected Zero Hypothesis, a Missing Archive, and a Repaired Lean Proof](https://flamehaven.space/writing/navierstokes-research-workbench2-a-rejected-zero-hypothesis-a-missing-archive-and-a-repaired-lean-proof/)
- NSRW Part 3 connects a source-derived bound to a bounded computation and a diagnostic benchmark. [From Proof to a Bounded Numerical Diagnostic](https://flamehaven.space/writing/navierstokes-research-workbench3-from-proof-to-a-bounded-numerical-diagnostic/)
- The earlier NSRW account explains how a candidate quantity led to a precise obstruction. [From a Scale-Invariant Candidate to an Obstruction](https://flamehaven.space/writing/from-a-scale-invariant-candidate-to-an-obstruction-what-changed-while-reproducing-a-navierstokes-construction/)
- The QSOT essay explains the evidence classes used to report a model check. [Verified Comes in Grades](https://flamehaven.space/writing/qsot-harness-verified-comes-in-grades-and-pretending-it-doesnt-is-where-slop-begins/)
