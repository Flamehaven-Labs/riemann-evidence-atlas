# Lower Frequency Cutoffs and the Polar Projection

This note uses the rational, trivial-angular sector of the fixed-level weighted comparison, with $S=\{\infty\}$ or $S=\{\infty,2\}$, $0<\alpha<1/2$, and Sobolev order two. It separates the lower frequency term from the upper term, identifies the surviving origin condition, and gives a trace identity for its rank-one correction. [Fixed-level weighted construction](S_LOCAL_WEIGHTED_QUOTIENT.md)

## Use the same spatial mask and level

Write $H_S(q)=\operatorname{Tr}(P_{S,Y}M_m A_kK_qP_{S,Y})$ and $H=H_{\{\infty,2\}}-H_{\{\infty\}}$. Keep $Y$, $m$, and the two projectors fixed when comparing the gates. For sharp cutoffs let $q_{\rm upper}$ retain frequencies up to $\lambda'$ and $q_{\rm low}$ retain frequencies below $1/\lambda'$. For the smoothed cutoffs average both terms over the same upper thresholds $u$, using lower thresholds $1/u$. The gate formula and trace linearity give
$$H(q_{\rm band})=H(q_{\rm upper})-H(q_{\rm low}).$$
The same splitting holds for the unfolded trace difference $Q$. With the spatial band $[1/\lambda,\lambda]$ and the prior function $d$,
$$
Q_{\rm upper}=d(\lambda\lambda')-d(\lambda'/\lambda),
\qquad
Q_{\rm low}=d(\lambda/\lambda')-d(1/(\lambda\lambda')).
$$

| Schedule | $\lim Q_{\rm upper}$ | $\lim Q_{\rm low}$ |
| --- | --- | --- |
| $(L,L)$ | $C-d(1)$ | $d(1)$ |
| $(L^2,L)$ | $C$ | $C$ |

Here $C=-\log 2/(4\sqrt2)$. The table also holds with the symmetric smoothing of NR-01. The threshold ratios converge uniformly on the shrinking intervals, so the limits use the same continuity and endpoint estimates as the four-term formula. In particular the unfolded lower frequency term survives the quadratic schedule even though its cutoff tends to zero. The projected terms $H(q_{\rm upper})$ and $H(q_{\rm low})$ require separate estimates. [Unfolded cutoff bounds](S_LOCAL_BAND_LIMITS.md) · [Balanced enclosure](S_LOCAL_EQUAL_RATIO.md)

## Which origin condition survives the weighted closure?

Work in the positive-radius chart $L^2(w\,dr)$ with $w(r)=e^{2\alpha|\log r|}(1+\log^2 r)$, extending profiles evenly when taking Fourier transforms. Let $B_Y$ be the even weighted band space with real Fourier support in $[-Y,Y]$. It is closed since $w\ge1$ and Fourier support is closed in ordinary $L^2$. Write $g=Ch$ in the core formulas. The condition $\int h=0$ says $g(0)=0$, whereas $h(0)=0$ says $\int g=0$. For fixed $Y$ the first is continuous in the weighted norm, by Fourier inversion and Cauchy–Schwarz over $[-Y,Y]$.

Even Schwartz functions with compact Fourier support inside the band and $g(0)=0$ are dense in $B_Y\cap\ker\operatorname{ev}_0$. First shrink Fourier support by $g(r)\mapsto g(ar)$ with $a<1$ tending to $1$. This converges strongly in the weighted norm, by density of continuous functions of compact support and boundedness of dilations uniformly near $a=1$. Then multiply by $\phi(\epsilon r)$, where $\phi$ is even Schwartz, band limited, and $\phi(0)=1$. For sufficiently small $\epsilon$ the enlarged spectrum stays strictly inside the band. The products are Schwartz since every derivative of a band-limited $L^2$ function is bounded. Dominated convergence gives weighted convergence and both operations preserve the value zero at the origin.

Choose an even Schwartz function $\psi$ with compact Fourier support, $\psi(0)=0$ and $\int_{\mathbb R}\psi=1$. One may choose its Fourier transform as an even smooth bump with value one at zero, then subtract an even bump away from zero to make the integral zero. Set $\psi_R(r)=R^{-1}\psi(r/R)$. Its integral stays one and its spectrum shrinks. Changing variables gives
$$
\|\psi_R\|_{L^2(w\,dr)}^2
=O_{\psi,\alpha}\big(R^{2\alpha-1}(1+\log^2 R)\big).
$$
Indeed $w(Rx)\le 2R^{2\alpha}(1+\log^2 R)w(x)$ for $R\ge1$, and $\psi$ has finite weighted norm. Subtracting $(\int g)\psi_R$ from any fixed smooth band approximation imposes zero integral at arbitrarily small cost. This proves that the two-condition core closes to $B_Y\cap\ker\operatorname{ev}_0$. The sequence $\psi_R$ also exhibits discontinuity of the integral on the band. Bounded invertibility of the dyadic $T$ transports the result to the one-prime space. Take $T=I$ for the real place alone.

In particular the actual level has codimension one in $V_{S,Y}=TB_Y$. It is the kernel in $V_{S,Y}$ of $\ell(v)=(T^{-1}v)(0)$. The account in the public issue gives the same loss of the integral condition for the real-place model. [Real-place weighted closure argument](https://github.com/mccorvie/riemann-masullo/issues/7354#issuecomment-7167631726)

## Weighted projection and the surviving rank-one term

Let $J:B_Y\to L^2(w\,dr)$ be the restriction of $T$ and use weighted adjoints. The operator $J^*J$ on $B_Y$ has lower bound $\|T^{-1}\|^{-2}I$. It has closed range by the lower bound and dense range by self-adjointness and injectivity. Consequently
$$
P_{V_{S,Y}}=J(J^*J)^{-1}J^*.
$$
The normal equation $J^*(x-Jb)=0$ proves the formula. Let $e_{S,Y}$ be the normalized Riesz vector of $\ell$ in $V_{S,Y}$. Then $P_{S,Y}=P_{V_{S,Y}}-e_{S,Y}\otimes e_{S,Y}^*$. For each fixed smooth upper, low, or band gate, write $D=M_m A_kK_q$. The trace of $D$ compressed to the actual level is exactly
$$
\operatorname{Tr}(P_{S,Y}DP_{S,Y})
=\operatorname{Tr}(P_{V_{S,Y}}DP_{V_{S,Y}})
 -\langle e_{S,Y},D e_{S,Y}\rangle_w .
$$
This follows by writing the trace in an orthonormal basis of the level and appending its single orthogonal unit vector in $V_{S,Y}$. Both compressions are trace class by the fixed-window argument. [Related finite-codimension trace argument](https://github.com/mccorvie/riemann-masullo/pull/7738)

For the G1 test the scalar term has a useful spatial form. The gate $K_q$ preserves $V_{S,Y}$, since $T^{-1}M_q T$ preserves the real band support of $h$. The operator $A_k$ commutes with $T$ and preserves $V_{S,Y}$, since the support of $k$ is in positive log radius and $g(r)\mapsto g(e^{-t}r)$ shrinks frequency support for $t>0$. In the positive-radius chart,
$$
\ell(A_k v)=\left(\int k(t)e^{-t/2}\,dt\right)\ell(v)=0.
$$
The last equality uses the fixed G1 Mellin moment. Therefore, for the real spatial mask $m$ and $e=e_{S,Y}$, the scalar is
$$
\langle e,M_mA_k K_q e\rangle_w
=\langle (M_m-I)e,A_kK_q e\rangle_w,\qquad
|\langle e,M_m A_kK_q e\rangle_w|
\le \|(1-m)e\|_w\,\|A_k\|\,\|K_q\|.
$$
The unmasked pairing vanishes for every gate in the split. Controlling the weighted mass of the Riesz vector in the discarded region is a separate estimate for a moving spatial window. [G1 Mellin moments](GEOMETRIC_TRACE_COMPARISON.md)

## A fixed spatial window has zero limiting difference

Let the low frequency radius $\delta$ tend to zero, the upper radius tend to infinity, and $Y$ tend to infinity. The frequency endpoints in each smoothing mixture obey the same limits. On the positive-radius weighted ambient space $K_{\rm low}$ tends strongly to zero and $K_{\rm upper}$ tends strongly to the identity. For a sharp real Fourier projection onto $[-\delta,\delta]$ and an even smooth compactly supported input, Fourier inversion and one integration by parts bound its output by $C\min(\delta,1/r)$. Integrating against $w$ gives squared norm $O(\delta^{1-2\alpha}(1+|\log\delta|^2))$. Density and the uniform weighted multiplier bound extend the convergence to all inputs, and the estimate on the dense core applies uniformly to shrinking cutoff mixtures. Expanding real Fourier projections converge strongly to the identity by testing first on weighted band-limited functions. Those are dense because smoothly truncating the Fourier transform of an even compactly supported smooth function converges in Schwartz topology. The dyadic series formula transfers both strong limits to $K_q$, including the term with $q(2\,\cdot)$.

The projectors $P_{S,Y}$ tend strongly to the identity. The levels increase with $Y$. Their union is dense: start with even compactly supported smooth functions vanishing near the origin, approximate by smooth Fourier truncation, then remove the small residual value at the origin with a fixed band-limited Schwartz function of value one. Weighted convergence follows from Schwartz convergence. Use the closure characterization above and apply the bounded invertible $T$.

For a **fixed compact spatial mask**, $D_0=M_m A_k$ is trace class. Cyclicity writes each trace as $\operatorname{Tr}(K_q P_{S,Y}D_0)$. Strong convergence of the uniformly bounded factors on the left implies trace-norm convergence after multiplication by $D_0$, by finite-rank approximation. Thus
$$
\operatorname{Tr}(P_{S,Y}M_mA_kK_{\rm low}P_{S,Y})\longrightarrow 0,
\qquad
\operatorname{Tr}(P_{S,Y}M_mA_kK_{\rm upper}P_{S,Y})
\longrightarrow k(0)\int m(t)\,dt=0.
$$
The ambient trace is obtained by integrating the absolutely summable Fourier rank-one expansion on the diagonal, and $k(0)=0$ for G1. These claims hold for each $S$ separately. The same limit follows for the band by subtraction. Any nonzero limit of the simultaneous expanding-window trace difference must be detected outside fixed spatial windows.

For the balanced and quadratic schedules the spatial window grows with $Y$, and the trace-class operator $D_0$ then depends on the limit parameter. The fixed-window argument gives no uniform tail estimate for the unpolarized trace.

## The polar term on moving windows

Set $Y=\lambda'=L$, align the radius by $x=Yr$, and write $D=\log Y$. Up to a constant unitary normalization the physical weight becomes
$$
w_D(x)=\frac{W(\log x-D)}{W(-D)},\qquad w_\infty(x)=x^{-2\alpha}.
$$
The band is now $[-1,1]$, and $T$ and $A_k$ commute with this physical rescaling. The common bounds
$$
w_*(x):=\frac{x^{-2\alpha}}{2(1+\log^2 x)}
 \le w_D(x)\le 2 W(\log x)
$$
follow from the triangle inequality in the exponential factor and
$1+a^2\le 2(1+(a-b)^2)(1+b^2)$. For the lower bound the exponential ratio is at least $x^{-2\alpha}$. The weights converge locally uniformly on $(0,\infty)$.

For each weight let the unpolarized space be $T$ applied to the even band. For $w_*$ and $w_\infty$ interpret Fourier support in the sense of tempered distributions. Both weighted spaces embed continuously into tempered distributions by Cauchy–Schwarz against Schwartz tests, using the polynomial growth of the reciprocal weights at infinity and its local integrability at zero. The dyadic series for $T$ and its inverse are bounded for these weights by the same geometric dilation estimate as above. The unpolarized spaces are closed. Evaluation of $T^{-1}v$ at zero is continuous even in the $w_*$ norm on the band. In fact, choose a Schwartz convolution kernel with Fourier transform one on $[-1,1]$, and evaluate that convolution at zero as a weighted pairing.

Let $u_D$ minimize the $w_D$ norm among unpolarized vectors with $\ell(u_D)=1$, and let $u_\infty$ be the corresponding minimizer for $w_\infty$. The minimizers exist by orthogonal projection onto an affine hyperplane. We claim $\|u_D\|_{w_D}\to\|u_\infty\|_{w_\infty}$. For the upper bound, trial vectors $v=Tg$ with $g$ Schwartz, Fourier support strictly inside $[-1,1]$, and $g(0)=1$ are dense in that hyperplane for $w_\infty$. The dilation and multiplication argument for the band applies in that weight. For distributionally band-limited input, convolution with the Schwartz reproducer shows that the function and its derivatives have at most polynomial growth, so multiplication by $\phi(\epsilon x)$ again yields a Schwartz function. Renormalize the value at zero if needed. These trial vectors lie in $L^2(W(\log x)\,dx)$, since $Tg$ grows at most logarithmically at zero and decays rapidly at infinity. Dominated convergence therefore gives $\|v\|_{w_D}\to\|v\|_{w_\infty}$ for each trial vector.

For the lower bound, take a subsequence attaining the lower limit of the norms. The common lower weight bound gives a weakly convergent subsequence in $L^2(w_*\,dx)$. The weak limit has the band condition after applying $T^{-1}$, and $\ell=1$ by its continuity on the band. On each compact subinterval, weak lower semicontinuity and local uniform convergence of weights bound the squared $w_\infty$ norm of the limit there by the lower limit of the squared $w_D$ norms. Exhaust the positive line to obtain an admissible $w_\infty$ vector and the desired lower bound.

For every such trial vector the minimizer satisfies
$$
\|u_D-v\|_{w_D}^2=\|v\|_{w_D}^2-\|u_D\|_{w_D}^2.
$$
Thus $u_D$, and also the normalized vector $e_D=u_D/\|u_D\|_{w_D}$, can be approximated to arbitrarily small limiting error by a single fixed trial profile in the varying norms. This proves tightness of their weighted masses at zero and infinity.

On the **quadratic schedule** the aligned spatial mask tends to one uniformly on every compact interval in $(0,\infty)$, since its edges have scales $L^{-1}$ and $L^3$. The discarded mass $\|(1-m)e_D\|_{w_D}$ tends to zero by tightness. The polar scalar therefore tends to zero for the upper, low, and band gates.

On **both schedules** the aligned lower frequency endpoint is $O(L^{-2})$. The low gate sends $e_D$ to zero in the varying $w_D$ norms. To see this, use the uniform bounds on $K_{\rm low}$, the approximation by fixed trial profiles and $w_D\le 2 W(\log x)$. The strong low-gate limit already proved in the fixed $W$ weight applies to each trial profile. Hence the lower frequency term has no limiting polar scalar on either schedule.

On the **balanced schedule** the aligned spatial mask tends almost everywhere to $\mathbf 1_{[1,\infty)}$. The aligned upper gate is eventually the identity on each strict-band trial profile, because its plateau exhausts $[0,1)$ and the folded trial spectrum stays inside a smaller band. Its action on $e_D$ therefore differs from the identity by a term tending to zero in the varying norms. Approximation by fixed trial profiles and dominated convergence in the pairing give the limiting upper polar scalar
$$
\big\langle e_\infty,\mathbf 1_{[1,\infty)}A_k e_\infty\big\rangle_{w_\infty},
\qquad e_\infty=u_\infty/\|u_\infty\|_{w_\infty}.
$$
The band has the same limiting polar scalar. The expression uses the minimizing vector of each place set separately. Its value and the limits of the unpolarized moving-window traces remain to be computed. The weighted compression also still needs comparison with the manuscript's Step III regularization.

Write $\widehat H$ for the difference of the unpolarized traces and $\Delta_{\rm polar}$ for the difference of the rank-one scalars, in the order $\{\infty,2\}$ minus $\{\infty\}$. The exact difference to be estimated is
$$
H(q_{\rm band})-Q
 = (\widehat H(q_{\rm upper})-Q_{\rm upper})
 - (\widehat H(q_{\rm low})-Q_{\rm low})
 - \Delta_{\rm polar}(q_{\rm band}).
$$
The last term tends to zero on the quadratic schedule. On that schedule any nonzero discrepancy must therefore come from the unpolarized compression comparison. On the balanced schedule the last term is the difference of the two limiting scalar pairings.

A finite Galerkin calculation now evaluates the lower trace for both place sets with the sharp finite windows. The results are sensitive to the basis size, particularly on the quadratic schedule. [Lower trace diagnostic](S_LOCAL_LOW_GALERKIN.md)

## Lean declarations

The Lean file verifies the normal-equation characterization of the image projection, the bound for the polar pairing in terms of the spatial cutoff defect, and the upper-minus-low form of the unfolded four-term identity. The weighted closure, analytic trace identities, and strong limits above are analytic arguments. [Lean source](../../tests/lean/E2ASLocalTraceSplit.lean)

All three declarations replayed on Windows and Colab Linux with Lean 4.33.1 and Mathlib at 0df444a360eaa60ab8c11dca51a86af692955474. The Colab receipt was decoded from the emitted Base64 and checked against its SHA-256. The receipts agree apart from the host target. Python regression tests passed 51/51 under both Python 3.10 and Python 3.14. [Windows receipt](s-local-trace-split-windows-replay.json) · [Colab receipt](s-local-trace-split-colab-replay.json) · [Colab notebook](https://colab.research.google.com/drive/1DRC7-5rixEXsu3tCWMLHmG1Cxfe6a1A8)
