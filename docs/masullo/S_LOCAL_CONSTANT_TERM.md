# Constant Incoming Rows of the Fixed Lower-Gate Trace

This calculation uses the sharp lower gate at $L=4$, $\alpha=1/8$, and the unpolarized 128-cell Galerkin space. It bounds the constant Fourier term of the trace approximation on each of the two extension strips and each place set. [Trace expansion](S_LOCAL_WEIGHTED_QUOTIENT.md#a-finite-level-weighted-trace-with-both-projection-legs) · [Outgoing residuals](S_LOCAL_PRIMAL_RESIDUAL.md)

## The incoming vector and its flat energy

Write $w(x)=W(\log(x/4))/S$ with $S=W(-\log4)$. For an outgoing strip $[a,b]$ in the aligned radial coordinate, the incoming support is
$$
 J_x=[a e^{-1/4}/2,\ b e^{1/4}/2].
$$
This is the radial image of the interval $I-[\log 2-1/4,\log 2+1/4]$ in logarithmic coordinates. Its logarithmic length is $\log4+1/2$. A Fourier period of $2$ suffices on the difference interval $I-J$. The outgoing vector is $\mathbf1_{[a,b]}x^{-1/2}$ and the incoming vector after the weighted gate adjoint is $v=K_q^{*w}(H/w)$, where $H=\mathbf1_{J_x}x^{-1/2}$. In passing from the logarithmic kernel to $L^2(w\,dx)$ the factors $\sqrt S$ and $1/\sqrt S$ on the two legs cancel in the rank-one operator.

Use $F=TCT^{-1}$, where $C$ is the flat unitary cosine transform and $T=(I-B)^{-1}$ with $Bf(x)=f(2x)$ for two places. At the real place $T=I$. On flat $L^2(dx)$, $B^*f(x)=f(x/2)/2$ and $B^*B=BB^*=I/2$. As $TC=CT^*$, the expression $F=CT^*T^{-1}$ is unitary. Indeed, $T^*$ and $T^{-1}$ commute and $T^*T^{-1}$ has inverse equal to its adjoint. Also $F^2=I$, so $F=F^*$. Thus the sharp gate $K_q=FM_qF$ is an orthogonal projection in the flat norm. Its weighted adjoint applied to $H/w$ equals $(K_q H)/w$, as follows by pairing on the common flat and weighted core. Using $1/w\le S$ gives
$$
 \|v\|_w^2 \le S\|K_q H\|_2^2
   =S\int_0^{1/16}|FH(\xi)|^2\,d\xi.
$$

Write $J_x=[u_0,u_1]$ and $Z=CH$. For $\xi>0$,
$$
 Z(\xi)=\frac{2}{\sqrt{\xi}}
   \bigl(C_{\rm Fr}(2\sqrt{\xi u_1})-C_{\rm Fr}(2\sqrt{\xi u_0})\bigr),
$$
where $C_{\rm Fr}(s)=\int_0^s \cos(\pi t^2/2)\,dt$. At the real place $FH=Z$. For two places the identity $CB=B^*C$ gives
$$
 FH(\xi)=(I-B^*)TZ(\xi)
 =\frac12\left(\sum_{j\ge0} Z(2^j\xi)-Z(\xi/2)\right).
$$
The direct integral and integration by parts give $|Z(\xi)|\le A=4(\sqrt{u_1}-\sqrt{u_0})$ and $|Z(\xi)|\le D/\xi$ with $D=2/(\pi\sqrt{u_0})$. On each panel $[\ell,2\ell]$, truncate the sum after $j=m$. The omitted part of $FH$ is bounded by $D/(2^{m+1}\xi)$ and has squared flat norm at most $D^2/(2^{2m+2}\,2\ell)$. Arb encloses the finite-panel energy and the code adds the triangle bound for that panel. Below $\epsilon=2^{-24}$, split the dilations at $2^j\xi=1$. A bound on $|FH(\xi)|$ is $A(2-\log_2\xi)/2+D$. Its square integrates explicitly. At the real place the low-end cap is $\epsilon A^2$.

## A lower bound for the finite incoming projection

Let $\gamma=1/16$ and choose $h(\xi)=(1-\xi/\gamma)_+$ on the positive frequency line. Its even extension has flat cosine profile $f(x)=\gamma\operatorname{sinc}^2(\pi\gamma x)$, where $\operatorname{sinc} z=\sin z/z$. The trial $g=TC h$ is in the 128-cell space because $\gamma$ is a mesh node. Its gated value is $K_qg=g$ because $Th$ is supported in $[0,\gamma]$. This gives a pairing lower bound $p$ by integrating a finite nonnegative portion of $g(x)x^{-1/2}$ over an exact inner subinterval of $J_x$. The real-place trial is $g=f$ and the two-place trial is $\sum_{j\ge0}f(2^jx)$.

For the norm upper bound $n$, use $|f(x)|\le\min(\gamma,1/(\pi^2\gamma x^2))$. On the dyadic radial panels, integrate the squared finite trial against $w$ and add its local tail norm using the largest panel weight and the integral of $x^{-4}$. Below the radial core, split the sum at $2^jx=1$ and integrate the square of the resulting affine log bound. Above the core, the inverse-square decay bound gives an exponential-moment integral after changing to $\log x$. These scalar estimates give
$$
 \|P_N v\|_w^2 \ge \frac{p^2}{n},
 \qquad
 \|(P-P_N)v\|_w^2 \le S\int_0^{1/16}|FH|^2-\frac{p^2}{n}.
$$

## Constant coefficient and trace error

For the period $2$ expansion, $|c_0|=\int h_{\rm G1}(t)\,dt/8$, using the vanishing integral of the second derivative. Apply upper and lower monotone rectangles to the half bump on $[0,1/4]$ after translating its center. The error bound for each rank-one trace contribution is $|c_0|\sqrt{\eta_{\rm out}\eta_{\rm in}}$. Summing over the two strips and two place sets bounds the constant Fourier contribution to the error in the difference between cutoff schedules. The sign of each contribution may differ. This sum uses absolute bounds.

## Certified results

| Outgoing strip associated with the incoming row | Places | Incoming omitted-basis squared norm upper bound | Constant rank-one trace error upper bound |
| --- | --- | ---: | ---: |
| $[1/4,1]$ | $\{\infty\}$ | 0.83175 | 0.03062 |
| $[1/4,1]$ | $\{\infty,2\}$ | 3.21337 | 0.12657 |
| $[16,64]$ | $\{\infty\}$ | 7.14846 | 0.10425 |
| $[16,64]$ | $\{\infty,2\}$ | 6.89281 | 0.18896 |

The 160-bit run with one more dyadic dilation gives the table and bounds the sum of the four absolute errors by **0.4503**, about 37% of the observed finite-matrix gap of 1.2054450173. The 106-bit run gives the upper bound 0.4538. This comparison uses the gap as a scale for the error budget. The finite-matrix gap has its own numerical uncertainty. The constant term uses the period and input windows fixed here, and the remaining Fourier terms must use the same expansion to complete the bound.

The displayed row bounds are rounded upward separately and add to 0.4504. The aggregate 0.4503 is obtained by summing the underlying interval expressions before rounding. [First nonconstant pair](S_LOCAL_FIRST_HARMONIC.md)

**ACCEPT** for the four incoming residual estimates and the constant-term error sum in the fixed unpolarized model. **AMBER** for the complete trace error and fixed-cutoff ordering. The results leave the nonconstant terms and Fourier tail open.

## Replay

~~~powershell
uv run --no-project --python 3.14 --with python-flint==0.9.0 python tools/s_local_incoming.py --report incoming-106.json
uv run --no-project --python 3.14 --with python-flint==0.9.0 python tools/s_local_incoming.py --precision 160 --depth 3 --report incoming-160.json
~~~

The report fields ending in upper or lower expression describe one-sided bounds. The driver binds the exact outgoing reports, source utilities, and fixed G1 Lean source by SHA-256.

Both saved results were recombined from the component balls at 192 bits. Six Fresnel values were also compared against direct radial cosine integrals with Arb, using two support intervals and three frequencies per interval. The two runs share the integration method. Both precision and dilation depth changed.

[Certificate driver](../../tools/s_local_incoming.py) · [106-bit report](s-local-incoming-106.json) · [160-bit report](s-local-incoming-160.json)
