# Mellin Multipliers and Derivative Modes in Logarithmic Coordinates

Fix $\alpha>0$ and use the earlier weight $w_\alpha(x)=e^{-2\alpha|x|}/(1+x^2)$. Let $v_t(x)=e^{itx}$ and $j_t(x)=ixv_t(x)$. Use the following translation sign for a complex kernel $k$.

$$
(T_k f)(x)=\int_{\mathbb R}k(y)f(x+y)\,dy,\qquad
m(t)=\int_{\mathbb R} k(y)e^{ity}\,dy.
$$

## Integral action on derivative modes

If $k\in L^1$ and $\int |k(y)||y|\,dy<\infty$, dominated convergence gives $m'(t)=\int k(y)iy e^{ity}\,dy$. The majorant is $|k(y)||y|$ by $|e^{ihy}-1|\leq |hy|$. Expanding the original integral at each $x$ gives

$$
T_kv_t=m(t)v_t,\qquad T_kj_t=m(t)j_t+m'(t)v_t.
$$

For $q_\delta=(v_{t+\delta}-v_t)/\delta$ we also have

$$
T_kq_\delta=m(t+\delta)q_\delta+
  \frac{m(t+\delta)-m(t)}{\delta}v_t.
$$

Lean proves the three identities and differentiability of $m$. The last identity uses Lean's totalized inverse for every $\delta$. The divided-difference basis interpretation applies when $\delta\ne0$.

### Weighted $L^2$ limit of the mode sequence

$$
\lim_{\delta\downarrow0}
\frac{1}{Z_\alpha}\int_{\mathbb R}
  |T_kq_\delta(x)-T_kj_t(x)|^2w_\alpha(x)\,dx=0.
$$

The $L^1$ and first absolute moment conditions on the kernel suffice. The two coefficients in the exact action converge to $m(t)$ and $m'(t)$. The bounds $|q_\delta(x)|,|j_t(x)|\leq|x|$ and $|v_t(x)|=1$ dominate the squared error by a constant times $(1+x^2)w_\alpha(x)$. Lean proves this integral limit.

## Boundedness on the weighted $L^2$ space

The derivative of $\log(1+x^2)$ has absolute value $2|x|/(1+x^2)\leq1$. Together with the triangle inequality for absolute values, this gives

$$
w_\alpha(x)\le e^{(2\alpha+1)|y|}\,w_\alpha(x+y).
$$

Changing the integration variable for $U_yf(x)=f(x+y)$ yields $\|U_y f\|_{L^2(w_\alpha)} \le e^{(\alpha+1/2)|y|}\|f\|_{L^2(w_\alpha)}$. Lean checks both the pointwise weight inequality and the integrated squared-norm bound.

For boundedness of the full kernel operator, let $E(y)=e^{(\alpha+1/2)|y|}$ and assume $C=\int |k(y)|E(y)\,dy<\infty$. For measurable $f\in L^2(w_\alpha\,dx)$, Cauchy–Schwarz gives

$$
\left(\int |k(y)|\,|f(x+y)|\,dy\right)^2
\le C\int |k(y)|E(y)^{-1}|f(x+y)|^2\,dy
$$

By Tonelli and the translation bound, the weighted integral of the right side is at most $C^2\|f\|_{L^2(w_\alpha)}^2$. Thus the kernel integral converges absolutely almost everywhere and $\|T_k\|\le C$. Applying the bound to the difference of representatives shows that representatives equal almost everywhere give the same result. Every $k\in C_c^\infty(\mathbb R)$ satisfies the hypothesis. This general operator bound is analytic. Lean verifies the individual translation bounds and the limit on the specified mode sequence.

## Correspondence with the pinned manuscript

The 2026-11-20 Masullo PDF has SHA-256 `e039d3f6cf0a4b14f03c7edb85097752dd65c0a2fe543c76fe992be234f97bf5`. Equations (10.2.2.4) and (10.2.2.6) on PDF p. 446 use modes containing $(\log |g|_F)^m$ up to the interior multiplicity. On the center line $b=0$ with trivial character and multiplicity $N\ge2$, the logarithmic representatives for $m=0,1$ are $v_t$ and $xv_t$. Thus $j_t=i\,xv_t$ represents the same derivative direction.

Equation (10.3.1.13) on p. 449 gives the logarithmic Mellin moments for the dual action. Equation (10.3.1.17) on p. 450 expresses the action as a triangular matrix on a finite-dimensional subspace. For the trivial character, include the normalization of the test function and Haar measure pushed forward under $\log|g|_F$. Then $M(z)=\int k(y)e^{zy}\,dy$, $m(t)=M(it)$, and $m'(t)=iM'(it)$. In the manuscript's $xv_t=j_t/i$ basis, the off-diagonal coefficient is $M'(it)$. The Atlas columns describe action on dual modes. To compare with the manuscript's original-space matrix, keep track of the rows and columns of the evaluation and dual bases.

This correspondence rederives the manuscript's logarithmic moment structure for one component without assuming the existence of a repeated zero. The action on the full idelic quotient, projections, uniform repeated-mode estimates, and the infinite Schatten sum remained open at this stage. [Public manuscript analysis and repair discussion](https://github.com/mccorvie/riemann-masullo/issues/1169)

## Replay

The [Lean source](../../tests/lean/E2AMellinTranslation.lean) imports the positive-width and mode-confluence proofs. The [verifier](../../tools/verify_mellin_translation.py) records all three proof digests, the Mathlib lock, the Lean version, and axiom output.

~~~sh
python -E -S tools/verify_mellin_translation.py \
  --lean "$(elan which lean)" --mathlib-project formal/landau
~~~

## Replay results

On 2026-11-25, Windows and Google Colab Linux replayed seven declarations with Lean 4.33.1 and Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`. The receipt fields matched apart from the host banner. The axiom output lists `propext`, `Classical.choice`, and `Quot.sound`. The Colab input combined public commit `0cb5cd9` with the selected proof and verifier files. The input ZIP SHA-256 is `019970cf19b247b0f84ac937edf00b494528fe323122fe545e7b8ef25037d16f`.

The original Colab JSON bytes were recovered and checked against remote SHA-256 `b344d63d56ae8cf31a691e0529cc1ea5a669f9e32c98c82921233e026343b7dc`. [Windows receipt](mellin-translation-windows-replay.json) · [Original Colab receipt](mellin-translation-colab-replay.json)
