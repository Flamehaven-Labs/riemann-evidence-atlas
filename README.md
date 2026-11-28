# Riemann Evidence Atlas

Riemann Evidence Atlas is an independent research repository for tracing Lean declarations related to the Riemann hypothesis and reproducing computable terms from the source papers. It separates declaration types from proof terms, computes exact rational enclosures, and certifies a fixed Landau tail integral in Lean.

[Versions and release notes](https://github.com/Flamehaven-Labs/riemann-evidence-atlas/releases) · [GitHub Actions](https://github.com/Flamehaven-Labs/riemann-evidence-atlas/actions/workflows/checks.yml) · [Changelog](CHANGELOG.md)

The project compares Alpöge's Lean proof with Masullo's approach to Hecke GRH, one
proof obligation at a time. The latest checkpoint documents where the numerical
trace certificate ran out of room and how an existing Lean theorem supplied a
conditional result for exterior zeros over the rationals.

[Read the case study](docs/RESEARCH_CASE_STUDY.md) · [Current roadmap](docs/ROADMAP.md) ·
[Colab Lean evidence and import blockers](docs/masullo/RH_PROOF_COMPOSITION_REPLAY.md) ·
[Release notes](docs/RELEASE_V0.3.0.md) · [Related writing](docs/RESEARCH_CASE_STUDY.md#related-reading)

## Quick start

Use Python 3.10 or later. Numerical runs and regression tests require only the Python standard library.

~~~sh
python -E -S tools/verify_baseline.py
python window_kernel.py
~~~

Pass inputs as JSON. The following case tests whether the integral over the positive half-line outside $[1,3]$ is at most $1/200$.

~~~json
{"component":"outside_window","k":3,"rate":"3","a":"1","b":"3","cap":"1/200","precision_bits":128}
~~~

~~~sh
python window_kernel.py --window case.json
~~~

| Exit code | Meaning |
| --- | --- |
| 0 | The computed upper bound is at or below the threshold. |
| 1 | The computed lower bound exceeds the threshold, or the input was rejected. |
| 2 | The enclosure straddles the threshold and the precision budget is exhausted. |
| 3 | Another execution outcome occurred. |

The optional `--ratio` input reproduces a historical MB-06 regression case at $\lambda=10^{-12}$ with the same arithmetic. Supply `lambda`, `cap`, and `precision_bits`. The arithmetic and runner code adapted from the Navier–Stokes repository are included here. These runs work offline without additional packages or a checkout of that repository. [Attribution and license](NOTICE.md)

## Computation and verification scope

We extract the positive kernel $u^k e^{-su}/k!$ with $s=\sigma-2>0$ from the author's `landau_window_ineq`. With $P_k(x)=\sum_{j=0}^k x^j/j!$, an antiderivative is $-e^{-su}P_k(su)/s^{k+1}$. Subtract the finite-window integral from the positive half-line integral $s^{-(k+1)}$ to compute the full tail.

- Inputs are dimensionless. The supported domain is $0\le k\le64$, $0\le a<b$, $s>0$, and $sb\le16$.
- The report records SHA-256 of the input bytes, the exact rational enclosure, and the precision used for the decision. Supported budgets are 128, 256, and 512 fractional bits.
- The example tail is approximately $0.00461721725334$. The calculation accepts $1/200$ as an upper bound and rejects $1/300$.
- The source trace records 13 references, including top-level Lean declarations, and the import path to the Landau inequality. The Lean 4.33.1 replay recovered seven declarations and six VALUE edges from five original modules. A separate pass classified 378 unresolved direct references. Lean 4.33.1 with pinned Mathlib verified the fixed tail's 128-bit enclosure and $1/300<J\le1/200$. Full transitive closure, a kernel recheck of the original RH proof, and the analytic link to Masullo's integral remain open.

[Lean trace](rh-proof-trace.json) · [Standalone results](window-results-v2.json) · [Earlier Colab baseline](window-results.json) · [Replay receipt](docs/standalone-replay.json)

| Check | Replay scope | Evidence |
| --- | --- | --- |
| Python | Fixed numerical cases and 51 regression tests on Linux and Windows with Python 3.10 and 3.14. | [Numerical results](window-results-v2.json) · [CI](.github/workflows/checks.yml) |
| Research models | The same notebook source replays the second Landau rational calculation, the exact prime-2 unit-shell sums, and the positive-width numerical check. | [Model replay notebook](colab/Research_Model_Replay.ipynb) |
| Lean and Mathlib | Lean 4.33.1 with pinned Mathlib replays the baseline and 28 declarations for the second Landau case, RH reflection, the biorthogonal bound, the two-zero matrix, and positive strip width. CI preserves input and receipt hashes and execution logs. | [Mathlib lock](formal/landau/lake-manifest.json) · [Research roadmap](docs/ROADMAP.md) |
| Original Lean references | Extracts direct type and proof-term references from preserved `.olean` files. | [Dependency analysis](docs/PROOF_DEPENDENCY_PILOT.md) |

## Second RH Landau Case

The same interval calculator tests a tail integral at different inputs. A local Lean run verified that the real integral lies inside the saved 256-bit enclosure and satisfies the stated thresholds. [Second case and replay](docs/LANDAU_SECOND_CASE.md) · [Numerical receipt](docs/landau-second-case.json) · [Lean receipt](docs/landau-second-case-lean-replay.json)

## Zero-Mode Models from the Masullo Manuscript

We formalized conditions under which arbitrarily small gaps preclude a uniform biorthogonal bound. In the span of two zero modes, the multiplier difference controls the off-diagonal entry. At zero width a Lipschitz multiplier makes the entry tend to zero. At fixed positive width a limit proportional to the multiplier derivative can remain. [Failure of the bound](docs/masullo/BIORTHOGONAL_GAP.md) · [Two-zero matrix](docs/masullo/TWO_ZERO_BLOCK.md) · [Positive strip width](docs/masullo/POSITIVE_STRIP_GRAM.md)

As two modes coalesce, the divided difference and the second Gram vector approach the derivative direction in weighted $L^2$. The limiting matrix is scalar when the multiplier derivative vanishes and otherwise has a Jordan term. Seven Lean declarations replayed on Windows and Colab. [Mode confluence and Jordan structure](docs/masullo/MODE_CONFLUENCE.md)

We verified the action of the logarithmic integral operator on derivative modes and the weighted $L^2$ limit, then compared the formulas with the manuscript's logarithmic moments and multiplicity conditions. Seven Lean declarations matched on Windows and Colab. [Mellin multipliers in logarithmic coordinates](docs/masullo/MELLIN_TRANSLATION.md)

Lean verified the reciprocal weight in the idelic quotient, quotient norm and dual action, and triangular translation of zero modes. The radial application assumes the manuscript's density theorem and includes the resolvent integral on an exponential mode. [Idelic quotient and zero modes](docs/masullo/ADELIC_QUOTIENT.md)

The weighted translation bound yields the generator energy estimate. Lean verifies summability of the squared resolvent column norms from the zero count. [Resolvent and Hilbert–Schmidt estimate](docs/masullo/RESOLVENT_HILBERT_SCHMIDT.md)

The fixed-character trace follows from kernel differentiation, factorization through two resolvents, and an absolutely summable Mellin diagonal. Eight Lean declarations replayed on Windows and Colab. Standard operator theory gives the trace-class conclusion and trace norm convergence of orthogonal compressions. [Fixed-character trace](docs/masullo/FIXED_CHARACTER_TRACE.md)

Fourier decay of the test function and Hecke zero counts give trace norm summability across all character blocks in the radial model. Coefficient cancellation and series comparison replayed in pinned Lean on Windows and Colab. [Trace over all character components](docs/masullo/GLOBAL_CHARACTER_TRACE.md)

For the geometric comparison over the rationals, seven declarations for the fixed radial test replayed in Lean on Windows and Colab. The unfolded S-local Fourier integral yields the exact prime-2 term and a one-sided cutoff error bound. The weighted quotient comparison and the global-to-local equality remain open. The separate rational exterior-zero cancellation theorem is checked under the archived Dirichlet nonvanishing hypothesis. [Geometric trace comparison](docs/masullo/GEOMETRIC_TRACE_COMPARISON.md) · [S-local cutoff calculation](docs/masullo/S_LOCAL_SHARP_CUTOFF.md)

For the trivial angular type over the rationals, the product-norm Paley–Wiener core now has a dyadic formula. At fixed cutoffs the weighted compression is trace class with an integrable trace density, including for smooth symmetric frequency masks. This gives an operator to compare with the two unfolded schedules. [Weighted S-local quotient](docs/masullo/S_LOCAL_WEIGHTED_QUOTIENT.md) · [Unfolded schedule dependence](docs/masullo/NEGATIVE_RESULT_REGISTER.md)

The trace split isolates the lower frequency gate and the single origin condition that survives the weighted closure. The corresponding polar correction vanishes on the quadratic schedule. The unpolarized moving-window comparison remains open. [Upper and lower trace terms](docs/masullo/S_LOCAL_TRACE_SPLIT.md)

## Colab

[Open the research model notebook in Colab](https://colab.research.google.com/github/Flamehaven-Labs/riemann-evidence-atlas/blob/main/colab/Research_Model_Replay.ipynb). Supply a full Git commit SHA and enable `RUN_LEAN` for Lean replay. GitHub Actions runs the numerical cells on a GitHub runner and compares the saved Colab receipts in a separate Lean job. The individual receipts identify runs that took place in an actual Colab session. [Replay instructions](docs/LEAN_MATCH_AND_COLAB.md) · [Original 10-case notebook](RH_Window.ipynb)

## Sources and Design Documents

| Document | Contents |
| --- | --- |
| [Cross-project verification specification](docs/CROSS_REPO_WORKFLOW_AND_VERIFICATION_SPEC.md) | Source, formal proof, numerical certificate, execution, and transfer evidence. |
| [Engineering research report](docs/ENGINEERING_RESEARCH_REPORT.md) | Source analysis of Landau and candidate NSRW and TOE experiments. |
| [Repository baseline](docs/REPOSITORY_BASELINE.md) | Preserved historical records, verification scope, and pending runs. |
| [Proof-term reference pilot](docs/PROOF_DEPENDENCY_PILOT.md) | Direct type and proof-term references in the original Lean artifacts. |
| [Lean matching and Colab replay](docs/LEAN_MATCH_AND_COLAB.md) | Inputs and results for synthetic declarations, original helper proofs, and Linux replay. |
| [P0–P3 patch sequence](docs/PATCH_SEQUENCE_P0_P3.md) | Review baselines, original Lean paths, local terms across both sources, and formal connections. |
| [2026-11-23 local validation](docs/LOCAL_VALIDATION_2026-11-23.md) | Scope of 17 regression tests, Lean 4.33.1 direct references, synthetic Choice paths, Python compatibility, and notebook execution. |
| [Inspector review and dispositions](docs/INSPECTOR_REVIEW_2026-11-23.md) | Evidence for each review and the ACCEPT, AMBER, and REJECT decisions. |
| [P0 baseline replay](docs/P0_BASELINE_REPLAY.md) | Running from a fresh checkout and replaying original evidence. |
| [P3 Landau tail verification](docs/P3_LANDAU_TAIL.md) | Pinned rational enclosure, real integral, and Lean replay. |
| [Independent P0–P3 audit](docs/P0_P3_INDEPENDENT_AUDIT_2026-11-23.md) | Scope of the November 23 audit and the then-missing Mathlib environment. |
| [Masullo manuscript and prime-2 baseline](docs/masullo/README.md) | PDF provenance, key pages, and rational identities. |
| [Prime-2 character comparison](docs/masullo/P2_CHARACTER_COMPARISON.md) | Four characters, modulus versus conductor, and conditions for relating the primary sources. |
| [Source inventory](sources.json) · [PDF page index](pdf-pages.jsonl) | Provenance, hashes, and original pages for four PDFs and public inputs. |
| [Lean archive](lean-archive-manifest.json) · [Extraction manifest](lean-extract-manifest.json) | Paths and SHA-256 digests for 14 archive fragments and 15 extracted files. |
| [Changelog](CHANGELOG.md) | Public versions and the earlier local baseline. |

To replay source tracing, download the original fragments from the archive inventory to the specified `sources/lean-parts/` paths. Use the extraction manifest to locate the required archive members. Run `python verify_lean_archive.py` to check the fragments and specified originals, then `python trace_lean.py` to rebuild the import graph. Rebuilding the PDF index requires the original files in the source inventory and the optional `pypdfium2` package. Downloaded originals, the large import graph, and local working notes are kept locally.
