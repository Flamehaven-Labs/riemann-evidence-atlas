# Close Zeta Zeros and the Biorthogonal Norm Bound

## Where the manuscript uses the bound

In the pinned 2026-11-20 PDF, the argument following equation (10.3.1.18) on p. 451 uses normalization of the Markushevich basis to choose a constant $C$ independent of the zero and derivative order. The bound already fails at derivative order zero for the trivial character over $\mathbb Q$, center line $a=1/2$, and Sobolev order $s=2$. [Pinned manuscript and digest](README.md) · [Counterexample report #1169](https://github.com/mccorvie/riemann-masullo/issues/1169)

| Location | Dependency identified |
| --- | --- |
| p. 444, Terminology 10.2.1.2 and Corollary 10.2.1.4 | The manuscript infers uniform boundedness of the biorthogonal functionals from the basis vectors' norms being bounded away from zero. Corollary 10.2.2.3 on p. 447 uses the same terminology for the strip basis. |
| pp. 451–452, (10.3.1.18)–(10.3.1.23) | The same $C$ is used in (10.3.1.19), (10.3.1.20), and (10.3.1.22). It supports the Schatten-norm Cauchy conclusion in (10.3.1.23). |
| pp. 454–455, Theorem 10.3.2.1 | The proof applies the earlier method to positive-width strips and separately estimates a sum involving derivatives of the transform. |
| pp. 463–464, (10.4.2.24) and (10.4.2.34) | The manuscript again chooses a common bound for lifts of biorthogonal vectors, then uses an index-independent constant to control the rank-one sum and claim an $S_1$ limit. |

## Lower bound imposed by the gap

Let $\delta=|t-u|>0$. In the weighted dual norm, $\|\eta_t\|^2=\pi c$. The Fourier identity $\int_{\mathbb R}\cos(\delta x)/(1+x^2)\,dx=\pi e^{-\delta}$ gives $\|\eta_t-\eta_u\|^2=2\pi c(1-e^{-\delta})$. Biorthogonality gives $(\eta_t-\eta_u)(\psi_t)=1$. The operator-norm bound for evaluation yields the lower bound below. Evaluation in the quotient is independent of the representative, so one takes the infimum over representative norms.

$$
\|\eta_t\|\|\psi_t\|
\ge \frac{1}{\sqrt{2(1-e^{-\delta})}}
\ge \frac{1}{\sqrt{2\delta}}.
$$

A common bound $C>0$ would force $\delta\ge 1/(2C^2)$ for every pair of distinct simple zeros. Conrey's Theorem 1 and the zero count give $\gg T\log T$ simple critical-line zeros up to height $T$. A fixed positive gap would give only $O(T)$ zeros, so arbitrarily small positive gaps occur. [Conrey, equation (8) and Theorem 1](https://www.maths.dur.ac.uk/users/herbert.gangl/morethan2_5.PDF)

## Lean verification scope

| Declaration | Result |
| --- | --- |
| `inverse_sqrt_gap_le` | The inverse square-root inequality from $1-e^{-\delta}\le\delta$. |
| `biorthogonal_product_lower` | A lower bound for the norm product when two continuous linear functionals give 1 and 0 on the same vector and the normalized distance formula holds. |
| `gap_lower_of_uniform_cap` | The necessary gap $\delta\ge1/(2C^2)$ under a common bound $C>0$. |
| `no_uniform_cap_of_close_pairs` | Nonexistence of a common bound given arbitrarily small positive gaps and the lower bound for each pair. |

The Lean declarations assume the normalized distance formula and the existence of close zero pairs. The Fourier identity and zero count cited above justify the analytic application to the source space. [Lean source](../../tests/lean/E2ABiorthogonalGap.lean)

On 2026-11-24, Windows and a fresh Colab Linux runtime compiled the four theorems with Lean 4.33.1 and Mathlib pinned to `0df444a360eaa60ab8c11dca51a86af692955474`. The axiom records list `propext`, `Classical.choice`, and `Quot.sound`. At the time of this replay, a GitHub Actions run for this file had yet to be confirmed. [Windows receipt](biorthogonal-gap-windows-replay.json) · [Original Colab receipt](biorthogonal-gap-colab-replay.json)

Restore the pinned dependencies, then run this command from the repository root.

~~~sh
cd formal/landau
lake env lean --root=../.. -j 2 ../../tests/lean/E2ABiorthogonalGap.lean
~~~

## Candidate replacement estimates

A gap-dependent upper bound would require a new estimate on the sum of its products with the Mellin transform. The current result gives a lower bound for the norm product. A second approach is to estimate the restricted operator for a cluster of close zeros directly. The public proposals require checking whether their estimates hold in the manuscript's space and extend to the trace sum. [Public repair proposal](https://github.com/mccorvie/riemann-masullo/issues/1169#issuecomment-7053478224)

For two zeros, a bound on the difference between Mellin multiplier values can offset growth in the off-diagonal entry. [Two-zero model](TWO_ZERO_BLOCK.md)
