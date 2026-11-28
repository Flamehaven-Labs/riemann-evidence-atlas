# Limits for Two Nearby Zeros at Positive Strip Width

In the public positive-width model, take Sobolev order $s=2$ and compare two modes on the same center line. For fixed $\alpha>0$, use the following weight, normalizing constant, and second moment. [Public weighted-space model](https://github.com/mccorvie/riemann-masullo/issues/1169#issuecomment-7057208991)

$$
w_\alpha(x)=\frac{e^{-2\alpha|x|}}{1+x^2},\qquad
Z_\alpha=\int_{\mathbb R}w_\alpha(x)\,dx,\qquad
M_2(\alpha)=\frac{\int_{\mathbb R}x^2 w_\alpha(x)\,dx}{Z_\alpha}.
$$

Both $w_\alpha$ and $x^2w_\alpha$ are bounded by $e^{-2\alpha|x|}$, which is integrable on both half-lines. Their integrals are positive because the continuous nonnegative integrands are positive at $x=0$ and $x=1$, respectively.

In the inner product of the normalized center-line modes $e^{itx}/\sqrt{Z_\alpha}$, evenness of the weight cancels the sine term. The real correlation $\rho_\alpha(\delta)$ is therefore the integral of $\cos(\delta x)w_\alpha(x)$ divided by $Z_\alpha$. The argument treats the cosine integral and the complex inner product space separately.

## From the integral to the Gram denominator

$$
\frac{1-\cos(\delta x)}{\delta^2}
=\frac{x^2}{2}\operatorname{sinc}^2\left(\frac{\delta x}{2}\right).
$$

The continuous $\operatorname{sinc}$ function equals 1 at zero and has absolute value at most 1. Dominated convergence gives $(1-\rho_\alpha(\delta))/\delta^2\to M_2(\alpha)/2$. Lean also proves the following two-sided bounds for sufficiently small positive $\delta$.

$$
\frac{M_2(\alpha)}4\,\delta^2
\ \le\ 1-\rho_\alpha(\delta)\
\le\ \frac{3M_2(\alpha)}4\,\delta^2.
$$

For unit eigenvectors $u,v$ with a real inner product $\rho$ satisfying $|\rho|<1$, the second orthonormal vector is $(v-\rho u)/\sqrt{1-\rho^2}$. The off-diagonal entry in this basis is $\rho(b-a)/\sqrt{1-\rho^2}$. The specified weight gives $\sqrt{1-\rho_\alpha(\delta)^2}/\delta\to\sqrt{M_2(\alpha)}$.

## Three off-diagonal regimes

| Multiplier difference | Result at fixed positive width |
| --- | --- |
| $\lvert b-a\rvert\le K\delta$ | The off-diagonal magnitude is at most $2K/\sqrt{M_2(\alpha)}$ for sufficiently small positive gaps. |
| $b=m(t+\delta)$ and $a=m(t)$ with $m$ differentiable at $t$ | The off-diagonal entry converges to $m'(t)/\sqrt{M_2(\alpha)}$. |
| $a=0$, $b=1$ | The off-diagonal magnitude diverges to $+\infty$. |

For $m(t)=t$ the limit is $1/\sqrt{M_2(\alpha)}\ne0$. The $O(\sqrt{\delta})$ decay at zero width and the boundedness at fixed positive width use different weights. Joint limits of width and gap fall outside this proof. [Zero-width two-zero model](TWO_ZERO_BLOCK.md)

For the supplementary numerical run with $\alpha=1/4$, $M_2\approx1.324157806194$ and the linear multiplier gives an off-diagonal limit of about $0.869020712016$. Simpson quadrature on $[0,80]$ used symmetry and partitions of 16,000 and 32,000 subintervals. At $\delta=10^{-6}$ the observed off-diagonal entry was about $0.869020712016$.

## Verification scope

Lean proves the integral limit and exact matrix identities for a general real Gram inner product and applies the weight limit to the off-diagonal entry. The manuscript's idelic quotient, zeros with distinct real parts or with multiplicity, the full window projection, and the infinite Schatten norm sum are outside these declarations. [Lean source](../../tests/lean/E2APositiveStripGram.lean)

On 2026-11-24, Windows and a fresh Colab Linux runtime checked 12 declarations with Lean 4.33.1 and Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`. All receipt fields except the host banner matched. The axiom records list `propext`, `Classical.choice`, and `Quot.sound`. The declarations also replayed in [GitHub Actions on the public commit](https://github.com/Flamehaven-Labs/riemann-evidence-atlas/actions/runs/45417852314). [Windows receipt](positive-strip-gram-windows-replay.json) · [Original Colab receipt](positive-strip-gram-colab-replay.json)

Replay from the repository after restoring the pinned Mathlib dependencies.

~~~sh
cd formal/landau
lake env lean --root=../.. -j 2 ../../tests/lean/E2APositiveStripGram.lean
~~~
