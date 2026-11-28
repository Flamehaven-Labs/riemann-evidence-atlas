# Galerkin Diagnostic for the Lower Frequency Trace

This calculation uses the rational trivial-angular spaces of the trace split, the fixed G1 test, and Sobolev order two. It compares the two place sets at finite cutoffs. The lower frequency gate and both spatial edges are sharp. The trace values use floating-point quadrature and a finite-dimensional orthogonal compression. [Trace split](S_LOCAL_TRACE_SPLIT.md) · [G1 test](GEOMETRIC_TRACE_COMPARISON.md)

## The projected operator

For each frequency level $Y=L$, use $x=Yr$ and the exact rescaled weight $w_D(x)=W(\log x-\log Y)/W(-\log Y)$. The real frequency band in this chart is $[-1,1]$. The retained lower gate has radius $b=L^{-2}$ in this chart. The spatial windows have endpoints $(1,L^2)$ and $(L^{-1},L^3)$ for the balanced and quadratic schedules respectively.

For the positive half of the real frequency band take the continuous piecewise linear hat functions $h_i$. The uniform subdivision is supplemented by the dyadic nodes $b/2,b,2b,\ldots<1$. The value at the upper endpoint is zero and the lower endpoint is free. Extend the spectra evenly and take $v_i=TC h_i$, using $T=I$ at the real place alone. In the two-place model the exact lower-masked spectrum before the final $TC$ is
$$
(T^{-1}M_qTh_i)(\xi)
 =\mathbf1_{\xi<b}h_i(\xi)
   +\mathbf1_{b/2<\xi<b}\sum_{j\ge1}h_i(2^j\xi)
 \qquad (\xi>0),
$$
up to endpoint values. The second term is a finite sum because $\xi>b/2$ there. The code constructs the affine pieces of this spectrum and integrates each cosine transform explicitly. The physical dyadic sum $T$ is then truncated at a specified scaled radius. The convolution uses $A_kv(x)=\int k(t)e^{-t/2}v(e^{-t}x)\,dt$.

The Gram matrix integrates over the positive line and the operator matrix over the indicated spatial window. With exact integrals, the trace on the chosen finite span is $\operatorname{Tr}(G^{-1}B)$. The implementation normalizes the Gram diagonal, uses a Cholesky factor and solves in the resulting basis, and records the condition number and the solve residual for each trace. The solve residual measures the linear algebra step only.

## Fixed-cutoff convergence of the exact compressions

At a fixed $L$, the meshes used here are nested when the uniform subdivision count doubles. Their maximum interval shrinks to zero. For an even smooth spectrum compactly supported strictly inside the band, piecewise linear interpolation converges uniformly. The total variations of the interpolants are bounded by that of the smooth spectrum. Fourier integration by parts therefore gives a common bound $C\min(1,1/x)$ for the inverse transforms. This is square integrable against $w_D$ at both ends for $0<\alpha<1/2$. Dominated convergence gives weighted convergence of the physical profiles before applying the bounded $T$. Smooth strict-band profiles are dense by the weighted band approximation in the trace split. Thus the union of the transformed hat spaces is dense in $TB_Y$ in the original chart.

For fixed cutoffs, their orthogonal projections converge strongly to the projection onto $TB_Y$. The cutoff operator $M_mA_kK_{\rm low}$ is trace class at this fixed spatial window. Finite-rank approximation then gives trace-norm convergence of the exact Galerkin compressions. This argument supplies no uniform rate as the spatial window grows. The reported computation also truncates the Gram integration and the physical dyadic series and uses finite quadrature. Those errors are compared by refinement in the recorded runs.

## Observations at strip half-width $1/8$

Each value below is the numerical lower trace at $S=\{\infty,2\}$ minus that at $S=\{\infty\}$. These rows use 32 uniform frequency cells, the added dyadic knots, and the refined integration settings of the driver.

| $L$ | Basis dimension | Balanced $(L,L)$ | Quadratic $(L^2,L)$ |
| --- | ---: | ---: | ---: |
| 2 | 32 | -1.842675 | -8.028721 |
| 4 | 32 | -3.297308 | -4.403771 |
| 8 | 34 | -1.038068 | -1.900527 |

The 12 main runs span three basis sizes at each level and one integration refinement at the largest size. The quadratic value is below the balanced one in each of these approximations. The values move substantially with basis size, so the current runs do not determine the trace at any of the three cutoffs to a certified tolerance. [Windows run](s-local-low-galerkin-windows.json)

Increasing only the Gram upper radius from $8L^2$ to $64L^2$ changes the 32-cell quadratic estimates by about $0.0414$ at $L=2$ and $0.0064$ at $L=4$. With the larger radius held fixed, increasing from 32 to 64 cells gives $-8.086265$ and $-7.193641$ respectively. The quadratic trace at $L=4$ thus still changes by about $2.80$ under basis refinement. At $L=2$ with 32 cells and the larger radius, doubling the test integration order changes the quadratic value by about $0.0012$. Halving the radius panel width changes it by about $0.0220$ and changes the balanced value by about $0.0337$. The tails and quadrature error are not enclosed by these comparisons. [Extended Gram runs](s-local-low-galerkin-extended-gram.json) · [One-setting refinements](s-local-low-galerkin-isolated-refinements.json)

The G1 control gives $k(\log 2)=-0.25$ and both computed Mellin moments have absolute value below $2.2\cdot10^{-10}$ at the refined test order. Separate floating-point checks compared 1,024 finite-gate samples with the direct theta expression, 48 cosine-kernel evaluations with independent quadrature, and 32 finite-matrix traces with QR orthogonalization. The repository's 51 Python regression tests also passed. These checks exercise the calculation and carry no bound for the infinite-dimensional trace error.

Colab Linux replayed six matching configurations at $L=2,4$ with NumPy 2.4.4. Across the 12 trace differences the maximum absolute discrepancy from Windows was $2.0\times10^{-13}$. The Colab summary was decoded from the runtime output and checked against its SHA-256. The replay checks arithmetic reproducibility at fixed finite sizes. [Colab receipt](s-local-low-galerkin-colab.json) · [Colab notebook](https://colab.research.google.com/drive/14DqVSaTvQEHSmL5OdNEIVBjeuyoqc5xk)

The lower unfolded term has a nonzero quadratic limit $C=-\log 2/(4\sqrt2)$. The observed projected values do not establish equality or inequality with that limit. A controlled comparison needs a basis error estimate as a function of $L$ and a sharper handle on the low-frequency spectral jumps. The upper trace and the Step III diagonal remain separate obligations. [Upper and lower trace terms](S_LOCAL_TRACE_SPLIT.md)

## Comparing nested compressions at $L=4$

The 128-cell run reverses the ordering of the two finite schedule values seen at 64 cells. To inspect this change, construct the 128-cell Gram and operator matrices once at each integration setting. The coarse 64-cell hats embed by their values at the fine knots. The corresponding columns in orthonormal coordinates are obtained using the fine Gram factor, then completed to an orthonormal basis by QR. In that basis the trace on the fine space is the trace on the coarse space plus the trace on its orthogonal complement. The same quadrature and the same fine matrices are used for both terms. This identity holds for a non-self-adjoint operator by summing its diagonal in the adapted basis.

For the two spatial masks, compute the common form on $[1,L^2]$ once. The quadratic form adds the contributions on $[L^{-1},1]$ and $[L^2,L^3]$. The audit repeats both trace splits after extending the Gram radius, then after refining the radius panels, the test quadrature, and the theta truncation. [Nested-compression audit driver](../../tools/s_local_low_nested.py)

| Integration setting | Balanced 64 cells | Balanced 128 cells | Quadratic 64 cells | Quadratic 128 cells |
| --- | ---: | ---: | ---: | ---: |
| Baseline | -3.781320 | -3.854819 | -7.193641 | -2.655977 |
| Doubled Gram upper radius | -3.781303 | -3.854813 | -7.193536 | -2.657046 |
| Refined radius panels, test order and theta extent | -3.786042 | -3.849159 | -7.186722 | -2.643714 |

The schedule ordering reverses between 64 and 128 cells in all three settings. Across the two schedules at 128 cells, the largest absolute change relative to the baseline is $0.01226359$, and the largest difference across all pairs of settings is $0.01333191$. The quadratic increment from adding the orthogonal complement is about $+4.54$ in all three runs. These figures describe sensitivity at the tested configurations. The finite-cutoff trace error and the behavior at larger basis sizes remain open. [Nested audit report](s-local-low-galerkin-nested-audit.json)

| Spatial portion in the aligned coordinate | Increment from the added modes in the two-place trace difference |
| --- | ---: |
| Common window $[1,16]$ | -0.073500 |
| Near-origin extension $[1/4,1]$ | -0.012208 |
| Outer extension $[16,64]$ | +4.623371 |
| Entire quadratic window $[1/4,64]$ | +4.537664 |

These are baseline quadrature values. The outer extension corresponds to the physical interval $r\in[4,16]$. The sum of the two extension forms reproduces the schedule difference at both basis sizes and for the increment. This is the spatial contribution of the additional finite modes at $L=4$. [Independent 128-cell run](s-local-low-galerkin-128-cell.json) · [Spatial strip report](s-local-low-galerkin-spatial-edges.json)

There is an a posteriori bound for the remaining fixed-cutoff basis error. Use the nuclear expansion of $M_mA_kK_{\rm low}$ in the weighted-trace construction and write its terms as $c_j a_j\otimes(\mathscr K^*b_j)^*$ in the ordinary $L^2(dt)$ chart. Let $P$ be the full unpolarized projection in this chart, and $P_N\le P$ the exact Galerkin projection. Set $E=P-P_N$. The trace difference equals the trace on $E$, by extending an orthonormal basis of $P_N$ to one of $P$. It follows that
$$
\big|\operatorname{Tr}(P M_mA_kK_{\rm low}P)
       -\operatorname{Tr}(P_N M_mA_kK_{\rm low}P_N)\big|
\le\sum_j |c_j|\,\|(I-P_N)a_j\|\,\|(I-P_N)\mathscr K^* b_j\|.
$$
Here the compressed operators in the trace are transported to the same chart. The inequality uses $E\le I-P_N$ and Cauchy–Schwarz in each rank-one term. This gives a bound in terms of finite-projection residuals and an absolutely summable Fourier tail. Its size depends on how well the chosen vectors are represented by the finite space. The estimate has not been evaluated in the reported runs. [Nuclear expansion](S_LOCAL_WEIGHTED_QUOTIENT.md#a-finite-level-weighted-trace-with-both-projection-legs)

The ambient residual contains two orthogonal terms:
$$
\|(I-P_N)u\|^2=\|(I-P)u\|^2+\|(P-P_N)u\|^2,\qquad
\|(P-P_N)u\|^2=\|Pu\|^2-\|P_Nu\|^2.
$$
In particular the ambient bound can retain an outside-space component as $P_N$ increases. To bound the true omitted-space residual, a certified upper bound on $\|Pu\|^2$ and a certified lower bound on $\|P_Nu\|^2$ suffice. Exterior frequency tests now improve the upper bounds for the constant outgoing rows in both extension strips and both place sets. The same test family gives a residual bound when combined with primal trial vectors. [Projection bounds from exterior frequencies](S_LOCAL_PROJECTION_BOUNDS.md)

## Evidence needed for a fixed-cutoff ordering

For the refined 128-cell run, the stored quadratic-minus-balanced gap in the two-place trace difference is $1.2054450173235587$. At $L=4$, a certified total absolute error strictly below that gap would preserve the observed ordering. If errors are bounded separately by schedule, sum the two schedule bounds, each including both place-set traces. A direct comparison can cancel the common spatial interval exactly, since the level, projection, and frequency gate are fixed within each place set. It then suffices to enclose the difference of the two-place traces on the union of the two extension strips and check that its lower endpoint is positive. This requires control of quadrature, the Gram solve, the theta truncation, and the omitted basis at the fixed cutoff. The joint limit remains a separate problem.

The audit finding is **ACCEPT** for the finite-matrix reversal, its spatial localization, and the distinction between baseline and pairwise changes. **AMBER** applies to any extension of the observed error ranking or ordering to the full fixed-cutoff operator. A claim that the current sensitivity checks certify an ordering for the full operator would receive **REJECT** because it would use the observed variation as an error enclosure. The nested split residual and source hashes were checked against the saved report. This check did not replay the Galerkin integrals.

## Upper-radius tail of the Gram matrix

Two integrations by parts give $|C h_i(x)|\le c_i/x^2$, where $2\pi^2 c_i$ is the sum of the absolute slopes at the endpoints and the absolute interior jumps of the slope. The dyadic sum gives $|TC h_i(x)|\le(4/3)c_i/x^2$. The omitted Gram matrix is positive semidefinite, and its trace, hence its operator norm, is bounded above by
$$
\frac{16}{9}\sum_i c_i^2\,
\frac{Y^{-4\alpha}R^{-p}}{1+\log^2 Y}
\left(\frac{1+\log^2(R/Y)}p+\frac{2\log(R/Y)}{p^2}+\frac2{p^3}\right),
\qquad p=3-2\alpha,\quad R\ge Y.
$$
For the 128 uniform cells at $Y=4$, the squared constants sum to $128^2(1+4\cdot127)/\pi^4$. The displayed bounds are approximately $1.80\cdot10^{-3}$ for $R=1024$ and $3.32\cdot10^{-4}$ for $R=2048$. If $G_0$ is the exact Gram matrix up to $R$, set $F=G_0^{-1/2}(G-G_0)G_0^{-1/2}$ and $A=G_0^{-1/2}BG_0^{-1/2}$. For $G_0$ positive definite, the trace change from the Gram tail is $-\operatorname{Tr}(F(I+F)^{-1}A)$. Its absolute value is at most $\|A\|\operatorname{Tr}(G-G_0)/\lambda_{\min}(G_0)$ because $0\le F(I+F)^{-1}\le F$. Using this estimate for an enclosure requires bounds for the Gram core, the operator matrix quadrature, and the omitted physical theta terms.

At fixed $Y$ and strip width, the absolute bound for $N$ uniform cells scales as $O(N^3R^{-p}(1+\log^2 R))$. A radius proportional to $N$ fails to make this bound decay at positive strip width. The relative Gram error also depends on the smallest eigenvalue.

## Replay

~~~powershell
$env:OPENBLAS_NUM_THREADS = '1'
uv run --no-project --python 3.14 --with numpy==2.4.4 python tools/s_local_low_galerkin.py --refine
~~~

[Numerical driver](../../tools/s_local_low_galerkin.py)

To replay any supplemental row, import the driver, construct its `Quadrature` from the row's `quadrature` object and call `calculate_scale(level, cells, 0.125, quad)`. The reports identify the driver by SHA-256.

Run the nested audit with the same environment:

~~~powershell
uv run --no-project --python 3.14 --with numpy==2.4.4 python tools/s_local_low_nested.py --output nested-audit.json
~~~

For the spatial strip report, use the baseline settings of the nested driver. Feed each strip's form into the same nested trace calculation while holding the Gram matrix and the inclusion fixed.
