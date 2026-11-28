# Resolvent and Hilbert–Schmidt Estimate for a Fixed Character

For positive width and $s=2$, the dual radial weight is $w_\alpha(x)=e^{-2\alpha|x|}/(1+x^2)$. Let $E$ be the closed span of polynomial modes of the retained zeros in the strip. Identifying $E$ with the dual of the idelic quotient uses the density conclusion of Masullo's Theorem 10.2.2.1. This stage checks the resolvent approach proposed by leecrossley in Issue #1169. [Idelic quotient analysis](ADELIC_QUOTIENT.md) · [Public resolvent proposal](https://github.com/mccorvie/riemann-masullo/issues/1169#issuecomment-7057208991)

## From a translation bound to generator energy

The translation $U_t f(x)=f(x+t)$ satisfies $\|U_t\|\le e^{\omega|t|}$ for $\omega=\alpha+1/2$. Dominated convergence gives strong continuity on $C_c(\mathbb R)$, and density and the uniform bound near zero extend it to weighted $L^2$. The space $E$ is invariant under translation in both directions, so the restricted group is strongly continuous. Let $A$ be its generator.

If $y\in D(A)$, the orbit $U_t y$ is differentiable at zero with derivative $Ay$. For positive $t$,

$$
\|U_t y\|^2\le e^{2\omega t}\|y\|^2
$$

and equality holds at $t=0$. Comparison of the right derivatives gives $\Re\langle y,Ay\rangle\le\omega\|y\|^2$. Lean's `orbit_energy_le` derives this from differentiability and the local upper bound. For $R_b e=y$ and $e=b y-Ay$, it follows that

$$
(b-\omega)\|R_b e\|^2\le \Re\langle R_b e,e\rangle.
$$

## Diagonal coefficient in an orthonormal basis

Order the modes at each zero by increasing degree. Each finite span $V_n$ is invariant by the [binomial translation formula](ADELIC_QUOTIENT.md). Polynomial exponential modes with distinct $z$ are linearly independent. Apply powers of $(\partial_x-z)$ that annihilate all other exponents in a finite relation. The leading coefficient of the remaining polynomial is multiplied by a nonzero constant. Positivity of the weight identifies a zero relation in $L^2$ with an identity of continuous representatives. Gram–Schmidt therefore yields a complete orthonormal basis $(e_n)$ of $E$.

On $V_n/V_{n-1}$, the action of $U_t$ is multiplication by $e^{z_n t}$. Thus $U_t e_n-e^{z_n t}e_n\in V_{n-1}$. For $b>\omega$, the Bochner integral $R_b=\int_0^\infty e^{-bt}U_t\,dt$ is bounded. Difference quotients and integration by parts give its inverse relation to the generator. Passing the continuous coordinate functional through the integral gives

$$
\Re\langle R_b e_n,e_n\rangle
=\Re\frac{1}{b-z_n}
=\frac{b-\Re z_n}{(b-\Re z_n)^2+(\Im z_n)^2}.
$$

The Lean theorem `laplace_diagonal_of_orthogonal_error` obtains this complex diagonal from the Laplace integral under orthogonality of the preceding-space component to $e_n$. If $b\ge\alpha+1$, then

$$
\|R_b e_n\|^2\le\frac{b+\alpha}{b-\omega}\frac{1}{1+(\Im z_n)^2}.
$$

## From zero counts to column summability

The $k$th shell contains modes with $2^k\le 1+|\Im z|<2^{k+1}$. A multiplicity-weighted count $N(T)=O(T\log T)$ gives $O((k+1)2^k)$ modes per shell. Since $(k+1)2^k=O(3^k)$, one can bound every shell count by $C3^k$ for some $C$. The published zeta count supplies the positive ordinates, and symmetry gives the negative ordinates. For a general fixed character, assume the corresponding count. [Hasanalizade–Shen–Wong's zeta zero count](https://arxiv.org/abs/2107.06506)

By $(1+|\Im z|)^2\le 2(1+(\Im z)^2)$, each summand on the shell is at most $2/4^k$. The shell sum is bounded by the summable geometric sequence $2C(3/4)^k$. Lean links the finite shell count bound to the inverse-square series and the resolvent column sum.

$$
\sum_n \|R_b e_n\|^2<\infty.
$$

The same geometric comparison gives the following analytic tail bound starting at shell $K$.

$$
\sum_{k\ge K}\sum_{i\in J_k}\|R_b e_i\|^2
\le 8C\frac{b+\alpha}{b-\omega}\left(\frac34\right)^K.
$$

A concrete counting constant $C$ makes this inequality quantitative. The tail bound is an analytic consequence of the geometric comparison.

Under these assumptions the specified fixed-character radial model satisfies $R_b\in S_2$. The construction of the orthonormal basis and generator domain and the zero-count theorem come from the analytic argument and cited literature. The idelic quotient application also uses the manuscript's density input.

The follow-up uses this column sum to treat kernel differentiation, factorization through two resolvents, and the fixed-character diagonal sum. [Fixed-character trace](FIXED_CHARACTER_TRACE.md) · [Public trace-class factorization](https://github.com/mccorvie/riemann-masullo/issues/1169#issuecomment-7057208991)

## Replay

[Lean source](../../tests/lean/E2AResolventHilbertSchmidt.lean) · [Verifier](../../tools/verify_resolvent_hilbert_schmidt.py)

~~~sh
python -E -S tools/verify_resolvent_hilbert_schmidt.py \
  --lean "$(elan which lean)" --mathlib-project formal/landau
~~~

## Replay results

On 2026-11-25, Windows and a fresh Google Colab Linux runtime compiled eight declarations with Lean 4.33.1 and Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`. The axiom output lists `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`. All fields except the host banner matched. Python 3.10 and 3.14 each passed 51 regression tests.

Colab combined public commit `0cb5cd9` with the new Lean source and verifier. The input ZIP SHA-256 is `1a0de0c2aa00657df6f9e3e6a5bbe901e76cf4e757fa531a177431d3e8d65c93`. The 1,291-byte Colab receipt was recovered and checked against remote SHA-256 `8ef1fbec0bfed832d08dd66228fb42525799f389ee76cd6f1617914130fc9e6d`. [Windows receipt](resolvent-hilbert-schmidt-windows-replay.json) · [Original Colab receipt](resolvent-hilbert-schmidt-colab-replay.json)
