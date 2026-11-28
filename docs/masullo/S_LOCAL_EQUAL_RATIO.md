# The Balanced Two-Sided Limit of the Unfolded S-Local Integral

## Result

For the fixed G1 test, the balanced unfolded two-sided limit is positive. The one-sided difference tends to $C=-\log 2/(4\sqrt2)$. At the finite cutoff product $A=1$, validated real integration gives
$$
-\frac{663}{100}<d(1)<-\frac{14}{10},\qquad
\frac{268}{100}<C-2d(1)<\frac{1314}{100}.
$$
The second interval encloses the limit for $\lambda=\lambda'\to\infty$. The unfolded two-sided schedule $(\lambda,\lambda')=(L^2,L)$ tends to zero. These are two distinct limits of the same unfolded two-sided expression. The balanced value also holds for the symmetric smooth band construction with both thresholds drawn from $[L-L^{-2},L]$. The products tend uniformly to infinity and the ratios tend uniformly to $1$, so continuity of $d$ at $1$ gives the same limit after averaging. [Limit formulas](S_LOCAL_BAND_LIMITS.md) · [Fixed G1 test](GEOMETRIC_TRACE_COMPARISON.md)

## Real integral used in the enclosure

Let $b=\xi^{-1}$ for an S-unit $\xi=\pm 2^n$. With the notation of the one-sided proof, put $J_b(r)=I_{1-b}(r)$. In the Fourier integral, integration of the $\log_+$ kernel against the exponential gives
$$
K_r(y)=\frac{\operatorname{Si}(2\pi r y)}{\pi y},\qquad K_r(0)=2r.
$$
This follows by integrating $\int_0^r\cos(2\pi s y)\log(r/s)\,ds$ by parts and doubling. The Fourier transform has the positive sign, so Fubini and the substitution $1+x=e^{-t}$ give
$$
J_b(r)=\int k(t)e^{-t/2} K_r(e^{-t}-b)\,dt.
$$
Both transformations are justified by compact support of $f$ and the integrability of the Fourier weight over $[-r,r]$.

For each S-unit, summation by parts in the shell index replaces $c_j=B_j-B_{j-1}$ by a difference of consecutive real integrals. The endpoint at $j\to-\infty$ vanishes by $I_a(r)=O_f(\sqrt r)$. At $A=1$ the result is
$$
d(1)=\sum_{b=\pm1}\bigl(J_b(1/2)-J_b(1)\bigr)
+\frac12\sum_{n\in\mathbb Z,\ \sigma=\pm1}
 \sum_{k\ge\max(0,n)} 2^{-k}
 \bigl(J_{\sigma2^{-n}}(2^k)-J_{\sigma2^{-n}}(2^{k-1})\bigr).
$$
The first sum combines the $B_1$ contributions and the $S=\{\infty\}$ subtraction. This calculation uses the exact 2-adic ball integrals. [Shell calculation](S_LOCAL_SHARP_CUTOFF.md#evaluation-by-additive-fourier-inversion)

## Absolute bounds for the omitted terms

On the support of $k$, $3/8\le e^{-t}\le 2/3$. Use $e^{-1/4}\ge 3/4$ and the reciprocal bound for $e^{1/4}$. For $n\ge0$, $|e^{-t}-b|\ge 1/8$ except for the stationary term $b=1/2$. For $n=-m<0$, $|e^{-t}-b|\ge 2^{m-1}$. The tail bound $|\operatorname{Si}(x)-\pi/2|\le 2/x$ for $x>0$ follows by integration by parts. Consequently, away from $y=0$,
$$
|K_r(y)-K_{r/2}(y)|\le \frac{3}{\pi^2 r y^2}\le \frac{1}{3r y^2}.
$$

For $b=1/2$ and $|y|\le1/24$, the corresponding $t$ differs from $\log 2$ by less than $1/8$. This uses $1+2y\in[11/12,13/12]$ and $|\log(1+2y)|\le1/11$. The bump is flat there and $|f|\le1/2$. In this region bound the integral of the absolute kernel difference by its whole-line integral. For $|y|\le1/r$, the bound $|K_r(y)|\le2r$ gives size at most $3r$ and integral at most $6$. Outside that interval the inverse-square estimate gives integral at most $6/\pi^2$. The whole integral is at most $7$. On the complementary stationary region use $|y|\ge1/24$ in the inverse-square estimate.

For a simple test norm bound, write $u=2-32(t-\log2)^2$ and $p(u)=\operatorname{smoothTransition}(u)$. For $0<u\le1/2$, put $v=1/u$ and $r_0=\exp(-1/u+1/(1-u))$. Then $p=r_0/(1+r_0)$ and $r_0\le e^{2-v}$. The first and second derivatives of the log odds have absolute bounds $v^2+4$ and $2v^3+16$. Maximizing $e^{2-v}v^j$ for $j=2,3,4$ on $v\ge2$, and using $e>2$, gives $|p'|\le8$ and $|p''|\le155$. The other half follows by $p(u)=1-p(1-u)$. Thus $|h''|\le155\cdot16^2+8\cdot64=40192$. The two transition intervals have combined length $1/2-1/(2\sqrt2)<3/20$. Since $t>0$, it follows that $\|f\|_1=\int |k(t)|e^{-t/2}dt<6100$ and $|k|\le41000$.

The computation retains $n\ge -N$ and $k<K$, with $N=8$ and $K=10$. At $k\ge K$ the inverse-distance-squared majorants sum to $64(2k+1)+8/3$ for nonstationary terms and add $24^2$ for the far stationary region. There are $2k+1$ nonstationary terms with $n\ge0$, and the negative-unit factor is $2\sum_{m\ge1}4^{1-m}=8/3$. The near stationary contribution is at most $7/2$ before its shell weight. For the omitted negative units with $k<K$, extend the $k$ sum to all $k\ge0$ to get an upper bound. With $B=64(2K+1)+8/3+24^2$, the total omission is bounded by
$$
\frac{6100}{6}\,4^{-K}\left(\frac{4B}{3}+\frac{512}{9}\right)
+\frac72\,2^{-K}
+\frac{6100}{6}\frac{32}{9}\,4^{-N}
=\frac{383279}{147456}.
$$
This is an exact rational error bound.

## Validated quadrature and replay

The computation collects like terms in the finite sum, leaving 306 kernels. It splits the real test into its two transitions and its plateau. On the transitions it uses the analytic formula for $p(u)$ and differentiates twice by the chain rule. The value on the plateau is $k=-1/4$. The transition formulas are split again at $u=1/2$ so that the exponential is evaluated with the smaller real sign. Each quadrature callback uses entire exponential and sine-integral functions and meromorphic quotients on its segment. When a complex input rectangle includes a possible zero of a denominator, ball division returns a non-finite enclosure and the quadrature must subdivide.

The four breakpoints and the possible zero of $e^{-t}-b$ at $t=\log2$ are trimmed by $\varepsilon=2^{-32}$ on the relevant sides. The integration endpoints are rounded inward to exact dyadics. The code verifies that their total additional excluded length is below $2^{-96}$, giving a bound of $8\varepsilon+2^{-96}$ per kernel. Use $|k|\le41000$, $e^{-t/2}\le1$, and $|K_r|\le2r$ and sum with the absolute finite weights. The endpoint allowance is below $0.0133$. The finite integrals are enclosed using FLINT ball quadrature at 106 bits. The two analytic omissions are then added to the ball before comparing with the threshold.

~~~sh
uv run --no-project --python 3.14 --with python-flint==0.9.0 python tools/s_local_equal_ratio.py
~~~

[Validated quadrature code](../../tools/s_local_equal_ratio.py) · [Enclosure record](s-local-equal-ratio-enclosure.json)

The saved enclosure was generated on Windows on 2026-11-26. Its SHA-256 is `731c9a53e3892cb559c5032c54e26751114617a9196773b4112725a9be455f6d`. The run checked the G1 Lean source digest before and after integration and recorded the quadrature source digest. The finite-ratio limit uses the earlier Lean-replayed implication and this new numerical enclosure.

## Consequence for the quotient comparison

If a proposed normalized quotient trace difference $H$ tends to $C$ on both schedules, then its correction $\mathcal E=H-Q$ must tend to $C$ on the quadratic schedule and to $2d(1)<-2.8$ on the balanced schedule. Any proof that gives an $o(1)$ identification of $H$ with $Q$ on both schedules would therefore force distinct limits for $H$. The actual weighted quotient kernel and its trace formula remain open. The enclosure certifies the unfolded integrals only. [Negative result register](NEGATIVE_RESULT_REGISTER.md)
