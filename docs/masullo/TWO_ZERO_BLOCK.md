# The Mellin Multiplier on Two Nearby Zero Modes

## Matrix for two vectors

Let $\delta=|t-u|>0$ and assume the unit vectors $v_t,v_u$ have real inner product $\rho=e^{-\delta}$. Let the linear map $A$ satisfy $Av_t=av_t$ and $Av_u=bv_u$, with $a=m(t)$ and $b=m(u)$. Then $w=e^\delta v_u-v_t$ is orthogonal to $v_t$ and $\|w\|^2=e^{2\delta}-1$. Set $D=\sqrt{e^{2\delta}-1}$. The vector $e_2=w/D$ is a unit vector and $v_u=e^{-\delta}(v_t+D e_2)$, so $(v_t,e_2)$ is an orthonormal basis of their span.

$$
A e_2=\frac{b-a}{D}\,v_t+b e_2,\qquad
[A]_{(v_t,e_2)}=
\begin{pmatrix}a & (b-a)/D \\ 0 & b\end{pmatrix}.
$$

## Small multiplier differences

If $|b-a|\le K\delta$ and $K\ge0$, then $D\ge\sqrt{2\delta}$ bounds the off-diagonal magnitude by $K\sqrt{\delta/2}$. With a common $K$ this entry tends to zero as $\delta\to0^+$.

Holding $a=0$ and $b=1$ gives off-diagonal magnitude $1/D$, which diverges to $+\infty$ as $D$ tends to zero through positive values. The two regimes differ in the size of the multiplier jump. This counterexample uses freely specified multipliers in the two-vector model.

On a fixed vertical line, write $m(t)=\int_{\mathbb R}k(x)e^{itx}\,dx$. If $k$ is integrable and $\int_{\mathbb R}|xk(x)|\,dx<\infty$, the first absolute moment serves as $K$. Integrate $\lvert e^{iux}-e^{itx}\rvert\le \lvert u-t\rvert\lvert x\rvert$ to obtain the Lipschitz condition.

## Lean declarations

| Declaration | Result |
| --- | --- |
| `orthonormal_block` | Gram–Schmidt in a complex inner product space and the exact two matrix columns. |
| `off_diagonal_norm_le` | The bound $K\sqrt{\delta/2}$ under the Lipschitz condition. |
| `off_diagonal_tendsto_zero` | Convergence of the complex off-diagonal entry as the positive gap tends to zero. |
| `fixed_jump_diverges` | Divergence of the off-diagonal magnitude to $+\infty$ when the multiplier jump is fixed at 1. |

The Lean inputs are the exact Gram inner product and two eigenvector identities. The result computes the matrix restricted to the span of the two vectors. Isolating a window in the whole space, summing $S_1$ norms over infinitely many windows, and comparing with the geometric trace require further arguments. The public finite-window proposal treats the whole window as an operator on the original quotient. [Lean source](../../tests/lean/E2ATwoZeroBlock.lean) · [Public finite-window proposal](https://github.com/mccorvie/riemann-masullo/issues/1169#issuecomment-7055349843)

On 2026-11-24, Windows and a fresh Colab Linux runtime replayed four declarations with Lean 4.33.1 and Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`. The proof and axiom output digests matched. At the time of this replay, the GitHub Actions run for the file had yet to occur. [Windows receipt](two-zero-block-windows-replay.json) · [Original Colab receipt](two-zero-block-colab-replay.json)

Use the following command in a checkout with the pinned dependencies restored.

~~~sh
cd formal/landau
lake env lean --root=../.. -j 2 ../../tests/lean/E2ATwoZeroBlock.lean
~~~

At fixed positive width, $1-\rho(\delta)$ decays quadratically in the gap. The off-diagonal entry can then converge to a nonzero multiple of the derivative of the multiplier. [Positive-width formal verification](POSITIVE_STRIP_GRAM.md)
