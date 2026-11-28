# Mode Confluence and Jordan Structure at Positive Strip Width

Use the weight and normalization of the [positive-width model](POSITIVE_STRIP_GRAM.md). For fixed $\alpha>0$, let $d\mu_\alpha=w_\alpha(x)\,dx/Z_\alpha$ and $M_2=\int x^2\,d\mu_\alpha>0$. For real frequency $t$, let $v_t(x)=e^{itx}$. [Public weighted-space model](https://github.com/mccorvie/riemann-masullo/issues/1169#issuecomment-7057208991)

## Limit of the second basis vector

$$
q_δ=\frac{v_{t+\delta}-v_t}{\delta},\qquad
j_t=ixv_t,\qquad
q_\delta\longrightarrow j_t\quad\text{in }L^2(\mu_\alpha),\quad \delta\to0^+.
$$

Pointwise convergence follows by differentiating the complex exponential. The inequality $|e^{iy}-1|\le |y|$ gives $|q_\delta(x)|\le |x|$. The squared difference is bounded by $4x^2$. The second moment proved earlier gives convergence of the weighted squared error to zero. This integral is the squared weighted $L^2$ distance. We have $\|j_t\|^2=M_2$. The weight is even, so the integral of $ix$ vanishes and $v_t$ and $j_t$ are orthogonal.

With the earlier Gram denominator $D_\delta=\sqrt{1-\rho_\alpha(\delta)^2}$, the second Gram vector is

$$
e_\delta=\frac{v_{t+\delta}-\rho_\alpha(\delta)v_t}{D_\delta}
=\frac{\delta}{D_\delta}q_\delta+
  \frac{1-\rho_\alpha(\delta)}{D_\delta}v_t.
$$

Since $D_\delta/\delta\to\sqrt{M_2}$ and $1-\rho_\alpha(\delta)=O(\delta^2)$, we have $e_\delta\to j_t/\sqrt{M_2}$ in weighted $L^2$. Lean verifies the integral of the squared error against the specified weight. Even symmetry eliminates the sine term in the inner product.

## When a Jordan block appears

For each positive gap, assume that a linear operator acts on the two modes with multipliers $m(t)$ and $m(t+\delta)$. In the basis $(v_t,q_\delta)$, its second column is $((m(t+\delta)-m(t))/\delta,\ m(t+\delta))$. When $m$ is differentiable at $t$, the matrix converges to

$$
\begin{pmatrix}m(t)&m'(t)\\0&m(t)\end{pmatrix}
$$

In the orthonormal basis the off-diagonal limit is the previously derived $m'(t)/\sqrt{M_2}$. Subtracting $m(t)I$ from the limiting matrix leaves a square-zero part. It is nonzero exactly when $m'(t)\ne0$, yielding a two-dimensional Jordan block in that case. For $m'(t)=0$ the limit is scalar.

The result concerns a local model of two modes on the same center line. The [follow-up](MELLIN_TRANSLATION.md) checks compatibility with the logarithmic Mellin integral and the correspondence to repeated modes in the manuscript. The full idelic quotient operator, window projections, and trace sums require separate arguments.

## Replay

The precise declarations are in the [Lean source](../../tests/lean/E2AModeConfluence.lean). The verifier compiles the earlier Gram module in the same pinned Mathlib environment and records the new axiom lists and both source digests.

~~~sh
python -E -S tools/verify_mode_confluence.py --lean "$(elan which lean)" \
  --mathlib-project formal/landau
~~~

## Replay results

On 2026-11-25, Windows and Google Colab Linux compiled seven new declarations with Lean 4.33.1 and Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`. The axiom records, both proof digests, and the dependency lock digest matched. The axiom list contains `propext`, `Classical.choice`, and `Quot.sound`. Colab overlaid the new Lean source and verifier on public commit `0cb5cd9`. The input ZIP SHA-256 is `0f8fae5f8ee4305a2485f3ef932859ed4a0a82acfa612edce4dab2c8f7400376`.

The remote terminal reported Colab output SHA-256 `2bef732e9b211d707a5a56488a82534f778e0bd77f8f4b0bb72c54316ab635c7`. A local copy made from the Windows receipt by changing only the host banner matches that digest. [Windows receipt](mode-confluence-windows-replay.json) · [Hash-matched Colab copy](mode-confluence-colab-replay.json)
