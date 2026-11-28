# Riemann Evidence Atlas Research Roadmap

Status as of 2026-11-28

## Research Aim

**Read and compare the formal proof of the Riemann hypothesis and an alternative proof approach step by step. Identify the assumptions that enable each conclusion and test the lemmas or models suggested by the comparison.**

Progress means explaining a step's mathematical role and giving another researcher the information needed to check its assumptions and conclusion. Turn connections from the comparison into lemmas or test them with counterexamples. Record unread proof terms, gaps in the manuscript, and refuted statements according to the evidence for each.

Read the primary sources, understand why the assumptions are used, and compare the approaches. Test the resulting questions with proofs, counterexamples, or calculations and record their scope and replay instructions. Return to the sources with the next question.

## Sources Under Comparison

- **Alpöge's Lean proof.** Lean FRO and Mathlib Initiative verified the standard RH statement and proof. Andrew Sutherland's November 24 report records a rebuild, statement comparison, and kernel check for standard RH and the Dirichlet $L$-function result. Atlas follows the available proof terms to learn what each auxiliary theorem does. [Lean and Mathlib joint statement](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) · [Independent verification record](https://math.mit.edu/~drew/grh/)
- **Masullo's approach to Hecke GRH.** The draft treats Hecke $L$-functions over all number fields and was under revision at public release. The follow-up formalization tracks open proof obligations and counterexamples to printed claims. The first comparison concerns a local term over `F = ℚ` that can be expressed with Dirichlet characters. [Draft announcement](https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/) · [Formalization and errata](https://github.com/mccorvie/riemann-masullo)

## Current Baseline

| Topic | Evidence | Open question or follow-up |
| --- | --- | --- |
| Fixed Landau tail in public `v0.2.0` | Lean proves the real integral identity and rational enclosure. Windows, Colab, and GitHub Actions replayed the proof. [Proof and replay record](P3_LANDAU_TAIL.md) | The second Landau case establishes the corresponding link for a different window and decay rate. |
| Second Landau case, v0.3.0 | The 128-bit enclosure was inconclusive at the close threshold. The 256-bit enclosure passed. Windows and Colab Linux replayed the Lean proof linking the real integral to the enclosure and threshold. [Execution and exact endpoints](LANDAU_SECOND_CASE.md) | The second case also replayed in [GitHub Actions on the pinned commit](https://github.com/Flamehaven-Labs/riemann-evidence-atlas/actions/runs/45417852314). |
| Original Lean proof terms | Checked type and proof-term references for seven declarations in five preserved modules. [Original reference record](rh-next-layer-module-set.json) | `VwinOfRow.olean`, full transitive dependencies, and an original RH kernel recheck remain open. |
| Prime-2 local term | Compared four characters in exact rational arithmetic and checked how the level and conductor affect the result. [Calculation and source locations](masullo/P2_CHARACTER_COMPARISON.md) | The analytic link from the manuscript's principal value to the Euler factor remains open. |

## Next Research Question

The mathematical aim remains to understand what each proof uses and what the comparison
reveals about the original problem. Reusing a checked Lean theorem can resolve a specific
obligation when its assumptions and conclusion match. Track the mathematical consequence
and the replay required to use an external proof.

| Research line | Current assessment |
| --- | --- |
| Rational exterior zeros | The pinned Masullo formalization and Atlas's application to the archived Dirichlet nonvanishing premise passed in Colab on Lean 4.36.0. The premise matched definitionally under Lean 4.33.1 and 4.36.0. The actual Alpöge proof remains to be imported in a shared environment. The 4.36.0 source probe stopped at `Supplements.Kernels.MainTheoremsCritical`. [Source, signatures, and replay](masullo/RH_PROOF_COMPOSITION_REPLAY.md) |
| Spectral trace | The radial fixed-character and all-character formulas retain the generator, basis, summability, and quotient density inputs documented in their derivations. [Fixed character](masullo/FIXED_CHARACTER_TRACE.md) · [All characters](masullo/GLOBAL_CHARACTER_TRACE.md) |
| Geometric trace | The fixed-cutoff weighted quotient has a trace density in the trivial-angular sector. NR-01 concerns schedule dependence of the unfolded integral, and NR-02 concerns preservation of the original Schwartz–Bruhat domain. The comparison with the manuscript's Step III diagonal and the joint weighted trace limit remain open. [Weighted quotient](masullo/S_LOCAL_WEIGHTED_QUOTIENT.md) · [Negative results](masullo/NEGATIVE_RESULT_REGISTER.md) |
| Numerical estimates | Reject the current first-pair norm-product certificate as sufficient for the remaining error budget. The bound is 65.23790 against 0.7551450173. The signed infinite-dimensional error remains open. Use numerical diagnostics when they test a specific analytic estimate. [First Fourier pair](masullo/S_LOCAL_FIRST_HARMONIC.md) |

1. **Identify the Step III operator at fixed cutoffs.** Start from the locally preserved
   manuscript, pp. 514–519, and the pinned formalization. For the G1 test over
   $\mathbb Q$ in the trivial-angular sector, match the operator order, projection,
   Haar normalization, diagonal regularization, and upper and lower cutoff parameters.
   Record an exact identity or the first unmapped term. The manuscript's editorial
   note leaves the lower spatial endpoint independent. Check which Atlas schedules
   a proposed comparison actually covers. [Projected density](masullo/S_LOCAL_WEIGHTED_QUOTIENT.md) · [Manuscript PDF](https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf)
2. **Target one moving-window estimate.** Use the identified operator on the quadratic
   schedule $(L^2,L)$ when the source permits it. The polar correction tends to zero on
   that schedule. If the comparison uses the two-sided band, start with its projected
   lower-frequency trace difference. The unfolded lower-frequency difference tends to
   $-\log 2/(4\sqrt{2})$ even as the lower cutoff shrinks. Seek a signed limit or an
   error estimate uniform along this schedule, or exhibit a counterexample to a
   proposed estimate. The fixed-window limit leaves this step open. [Upper and lower terms](masullo/S_LOCAL_TRACE_SPLIT.md)
3. **Keep the Alpöge import investigation bounded.** Start at the proof body of the
   archived `allChi` and identify the first directly reusable declaration and its
   definition dependencies. The original `Main` source transitively imports all
   175,187 project modules, so a smaller declaration-level dependency set needs its
   own evidence. Promote the full rational exterior-zero composition only after the
   actual proof enters a shared kernel-checked declaration with its axiom audit.
   [Composition replay](masullo/RH_PROOF_COMPOSITION_REPLAY.md)

Use Lean and Colab when an exact new claim or negative control is ready to replay.
Transfer to Navier–Stokes or TOE remains a later research decision tied to a specific
mathematical obligation.

## Research Sequence

1. **Connect the Landau calculation to a proof.** Local Lean connects the integral at $k=1$, $s=2$, and excluded window $[1/2,2]$ to the saved 256-bit interval. It uses the same close threshold. [Declarations and replay](LANDAU_SECOND_CASE.md#lean-proof-of-the-real-integral)
2. **Read the mathematics of a Lean declaration.** Locate the cosine zero theorem in `Formalism.VW.rh_of_right`. Distinguish the real-part condition on the cosine factor from the condition for applying the right-half-plane nonvanishing hypothesis. Local Lean checks the boundary example $s=2$. [Cosine factor analysis](RH_REFLECTION_COS.md)
3. **Compare a prime-2 local term in both sources.** Use the manuscript's principal-value definition and unit Haar measure to compute $-a\log 2$ for a local character of conductor exponent $a$. The manuscript's vanishing condition on norm-one classes makes the unit contribution zero. A full comparison with the Euler factor must match the test function, non-unit shells, and Mellin normalization. [Unit-shell analysis](masullo/P2_UNIT_SHELL.md)
4. **Check Masullo's biorthogonal norm bound.** Identify the common constant introduced after (10.3.1.18) and its role in Schatten convergence and lifts. Lean formalizes the gap-dependent lower bound and the positive separation a uniform bound would force. The results replayed on Windows and Colab. [Manuscript comparison and Lean results](masullo/BIORTHOGONAL_GAP.md)
5. **Verify the matrix for two nearby zeros.** Compute the matrix for two unit eigenvectors with inner product $e^{-\delta}$. Lean shows that its off-diagonal entry tends to zero under a multiplier difference bounded by $K\delta$ and diverges when the difference stays at 1. Proof and axiom records match on Windows and Colab. [Two-zero model and replay](masullo/TWO_ZERO_BLOCK.md)
6. **Check the change in decay order at fixed positive width.** Lean proves that the second moment is finite and positive and that the cosine integral's decrement is quadratic in the gap. The off-diagonal limit for a differentiable multiplier and the two counterexamples replayed on Windows and Colab. [Positive strip width](masullo/POSITIVE_STRIP_GRAM.md)
7. **Identify the second basis vector as two modes coalesce.** At fixed positive width, the divided difference converges to $ixv_t$ and the second Gram vector converges to $ixv_t/\sqrt{M_2}$ in weighted $L^2$. The multiplier derivative determines the Jordan term of the local matrix. Seven Lean declarations replayed on Windows and Colab. [Mode confluence and Jordan structure](masullo/MODE_CONFLUENCE.md)
8. **Compare the local model with the manuscript's Mellin action.** Lean verifies translation integral formulas for the base and derivative modes, differentiation of the multiplier, the weighted $L^2$ limit of the mode sequence, and bounds on individual translations. The formulas match the cited interior multiplicity condition and logarithmic moment coefficient. [Mellin multiplier and derivative modes](masullo/MELLIN_TRANSLATION.md)
9. **Apply the model to the idelic quotient's radial component.** Compare the manuscript's reciprocal weight and sign. Lean verifies the quotient norm, dual action, binomial translation of zero modes, and orthogonal compression. The density statement is an input to the analytic invariance argument for the fixed trivial character. [Idelic quotient and zero modes](masullo/ADELIC_QUOTIENT.md)
10. **Estimate the resolvent column sum.** Lean verifies summability of squared column norms using generator energy, the Laplace diagonal coefficient, and dyadic counts. The radial application uses the generator and basis construction. The idelic quotient application also requires the manuscript's density input. [Resolvent and Hilbert–Schmidt estimate](masullo/RESOLVENT_HILBERT_SCHMIDT.md)
11. **Derive the trace of a fixed-character radial model.** Pinned Lean on Windows and Colab verifies kernel differentiation, two-resolvent factorization, the rank-one expansion, and the absolutely summable Mellin diagonal. Standard operator theory gives the trace identity and trace norm convergence of orthogonal compressions. [Fixed-character trace](masullo/FIXED_CHARACTER_TRACE.md)
12. **Sum trace norms over all characters in the radial model.** Fourier decay on the compact Lie quotient and the Hecke zero count give trace norm summability. Three Lean theorems on coefficient cancellation and summability passed on Windows and Colab. The idelic quotient application retains the density input. [All-character trace](masullo/GLOBAL_CHARACTER_TRACE.md)
13. **Compare with the geometric trace.** Seven declarations for the fixed rational-field test replayed on Windows and Colab. The unfolded S-local Fourier integral gives the prime-2 contribution with a one-sided cutoff error bound. In the symmetric two-sided calculation, the quadratic schedule has limit zero and validated quadrature gives a positive limit for the balanced schedule. The difference persists for the specified smoothing of the bands. The weighted quotient kernel and diagonal trace formula remain open. [Geometric trace comparison](masullo/GEOMETRIC_TRACE_COMPARISON.md) · [Two-sided cutoff limits](masullo/S_LOCAL_BAND_LIMITS.md) · [Negative result register](masullo/NEGATIVE_RESULT_REGISTER.md)

14. **Construct the weighted S-local compression.** At fixed cutoffs in the trivial angular type the descended smooth frequency gate is bounded and the weighted compression has an integrable trace density. The next comparison concerns the two simultaneous-cutoff limits and the manuscript's Step III diagonal. [Weighted S-local quotient](masullo/S_LOCAL_WEIGHTED_QUOTIENT.md)
15. **Separate the lower frequency and polar terms.** One origin condition survives weighted closure. Its rank-one contribution tends to zero on the quadratic schedule, and the low frequency gate has zero limiting polar contribution on both schedules. The balanced upper polar scalar, the unpolarized moving-window limits, and the Step III comparison remain open. [Trace split and moving-window estimates](masullo/S_LOCAL_TRACE_SPLIT.md)
16. **Measure basis and quadrature sensitivity of the lower trace.** At $L=4$ the order of the two finite schedule values reverses between 64 and 128 cells across three integration settings. The added modes contribute mainly in the outer spatial strip of the quadratic window. The exact Galerkin compressions converge at fixed cutoffs. An error enclosure at the tested basis sizes and a uniform estimate as the window grows remain open. [Lower trace diagnostic](masullo/S_LOCAL_LOW_GALERKIN.md)
17. **Bound the full projection using exterior frequencies.** Explicit orthogonal test vectors give certified upper bounds on four constant outgoing row norms at $L=4$. A joint trial residual separates the missing basis from the outside-space error. The remaining nuclear rows and the trace error bound are open. [Projection bounds](masullo/S_LOCAL_PROJECTION_BOUNDS.md)
18. **Enclose the weighted Gram matrices for the exterior trials.** Arb integration, positive semidefinite tail bounds, and interval solves improve all four outgoing projection estimates. The gain brackets show that tighter integration alone has little room to improve the two outer-row bounds for these packet spans. The joint primal and dual residual and full trace error remain open. [Weighted Gram bounds](masullo/S_LOCAL_DUAL_GRAM.md)
19. **Bound the missing 128-cell components of four outgoing rows.** Fixed dyadic trial coefficients and scalar Arb integrals give four lower bounds on the finite projection. Combined with the weighted Gram results, they bound the four omitted-basis squared norms. The two-place outer row still has a substantial dyadic tail allowance. The other rows, Fourier tail, and trace ordering remain open. [Primal projection bounds](masullo/S_LOCAL_PRIMAL_RESIDUAL.md)
20. **Bound the first Fourier term of the trace approximation error.** The flat low-gate projection bounds the four constant incoming vectors. An in-band trial gives a positive finite-projection lower bound for each. The sum of the four constant rank-one error bounds is below 0.4503 for the period-two expansion. The nonconstant terms, Fourier tail, and trace ordering remain open. [Constant incoming rows](masullo/S_LOCAL_CONSTANT_TERM.md)
21. **Check the first conjugate Fourier pair against the error budget.** The coefficient magnitude is between 2.02129 and 2.02253. Certified incoming and outgoing residual bounds give a norm-product sum of at most 65.23790, above the remaining budget of 0.7551450173. The Arb report is byte-identical on Windows and Colab. On both hosts, Lean checks the signed polarization, nested projection lower bound, and exact budget arithmetic. The signed mixed-projection values and full trace ordering remain open. [First Fourier pair](masullo/S_LOCAL_FIRST_HARMONIC.md)
22. **Test the exterior-zero implication using the archived Dirichlet theorem.** Colab Lean checks that open-strip membership and zero transfer into Alpöge's Dirichlet statement imply an empty exterior index and a zero sum. The upstream source gives a strict-strip argument for the completed divisor. This first bridge takes the completed-Hecke-to-Dirichlet zero transfer as an assumption. The next entry uses the upstream implementation of that transfer. The weighted quotient and joint trace limit have their own analytic obligations. [Dirichlet exterior-zero bridge](masullo/RH_EXTERIOR_ZERO_BRIDGE.md)
23. **Apply the verified rational exterior-zero theorem to the archived premise.** The fixed Masullo source compiled under Lean 4.36.0 and its axiom audit passed. The archived GRH premise matched definitionally in both toolchains, and the 4.36.0 conditional application replayed with the original test-function and strip-width assumptions. Direct use of Alpöge's proof remains AMBER at the shared-environment import closure. [Composition and reproducibility record](masullo/RH_PROOF_COMPOSITION_REPLAY.md)

## Replay at Phase Transitions

- **Check the environment early.** When a new Mathlib module, original `.olean`, or runtime dependency is needed, try reading or compiling it first. Record missing inputs and timeouts separately from a failed proof check.
- **Compile new statements in pinned Lean.** Record exact declarations, axiom output, and commands. Before using new calculations or formal results in the next stage, replay the same inputs and toolchain on Colab Linux and compare them with the local baseline. Replay numerical calculations and negative controls at numerical stages and the relevant Lean declarations at formal stages. Record evidence from source reading and documentation when obtained.
- **Tie a public release to GitHub Actions evidence for its commit.** Record Colab as cross-environment replay. Record a separate researcher's independent verification as its own run.

On 2026-11-24, Colab Linux replayed four second Landau theorems and four RH reflection cosine theorems with Lean 4.33.1 and Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`. Axiom records matched Windows. Python 3.13.18 passed 51 regression tests, and five prime-2 unit-shell inputs at eight truncation depths matched the Windows results.

The run bundled files selected from the working tree based on `5cea957` with comparison logs. The input ZIP SHA-256 is `686a2f54843f2b9f9fd33e9d72dd1f9ac387f3a928ca7adc5ef7ebe8cda54537`. [Original Landau receipt](landau-second-case-colab-replay.json) · [Colab replay procedure](LEAN_MATCH_AND_COLAB.md)

## Longer-Term Connections

Connect to Navier–Stokes when there is a specific proof obligation. For example, an explicit tail bound beyond a finite window first requires boundary and decay assumptions supported by the source solution. TOE is a longer-term research direction. Design a comparison only when the candidate model's equations, assumptions, observables, and falsifying outcomes can be specified.

## Research Record

- Before a run, specify the source location, assumptions, pinned inputs, comparison method, expected result, and rejection condition. Record the reason if a criterion changes after observing the result.
- Record replay commands and actual observations. Distinguish successful proof compilation, independent arithmetic comparison, missing data, and insufficient precision.
- Treat each audit finding as a claim to check against the source, locked inputs, and available evidence. Report **ACCEPT** for findings supported at their stated scope, **AMBER** when evidence is incomplete or the scope needs qualification, and **REJECT** when verified evidence contradicts the finding or the stated inference fails. Record the reason and any correction. An audit judgment may change when better evidence becomes available.
- Add terminology or diagrams only when they clarify assumptions or observations. Use runnable code for capabilities and link the corresponding result artifact or proof for claims.
