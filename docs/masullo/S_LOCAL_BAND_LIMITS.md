# Small Cutoffs and Two-Sided Limits of the Unfolded S-Local Integral

This note continues the sharp cutoff calculation for the fixed G1 test over $\mathbb Q$. The quantities $D_S(A)$ below are the unfolded Fourier integrals of (12.4.1.22)–(12.4.1.24). [One-sided cutoff calculation](S_LOCAL_SHARP_CUTOFF.md)

## Small-cutoff bound

Write $g=\widehat f$ for the real Fourier factor, with $f$ as in the one-sided calculation. Since $g$ is Schwartz, it is bounded, $g'$ is integrable, and $\int_{\mathbb R}|g(s)||s|^{-1/2}\,ds$ is finite. Define
$$
I_a(r)=\int_{\mathbb R}g(s)e^{2\pi ias}\log_+(r/|s|)\,ds .
$$
The estimate $\log_+ v\le 2\sqrt v$ gives
$$
|I_a(r)|\le L_0\sqrt r,\qquad
L_0=2\int_{\mathbb R}|g(s)||s|^{-1/2}\,ds .
$$
In particular this bound includes the zero phase. Bounding the integrand by $\sup |g|$ alone gives an $O(r)$ bound for a single real integral. That bound cannot be summed over the small 2-adic shells of the zero-phase term, since $r=A2^{-j}$ there.

For $a\ne0$, use
$$
I_a(r)=\int_0^r\left(\int_{-u}^{u}g(s)e^{2\pi ias}\,ds\right)\frac{du}{u}.
$$
Fubini is justified by the absolute logarithmic integral. The inner integral is bounded by $2u\|g\|_\infty$. Integration by parts, retaining both endpoint terms, also bounds it by $(2\|g\|_\infty+\|g'\|_1)/(2\pi |a|)$. Taking the geometric mean and integrating gives
$$
|I_a(r)|\le L_1\sqrt{r/|a|},\qquad
L_1=2\sqrt{\|g\|_\infty(2\|g\|_\infty+\|g'\|_1)/\pi}.
$$

For $S=\{\infty,2\}$, the $\xi=\pm2^n$ term is $\tfrac12\sum_{j\le1}c_j(a)I_a(A2^{-j})$ with $a=1-\xi^{-1}$. The ball formula fixes the support and absolute size of its shell coefficients.

- If $n\ge1$, the nonzero coefficients are $c_j=2^{j-1}$ for $j\le -n$ and $c_{1-n}=-2^{-n}$. Thus $\tfrac12\sum_{j\le1}|c_j|2^{-j/2}=B\,2^{-n/2}$, where $B=1/(4(1-2^{-1/2}))+1/(2\sqrt2)$. Apply the bound with $L_0$.
- If $n\le-1$, $a$ is a 2-adic unit. The same weighted shell sum is $B$, obtained from the preceding coefficient pattern with $n=0$. Its real absolute value satisfies $|a|\ge 2^{-n-1}$. The bound with $L_1$ then gives a summable factor $2^{(n+1)/2}$.
- For $n=0$, both $\xi=1$ and $\xi=-1$ have $c_j=2^{j-1}$ for $j\le1$. Their weighted shell sums are finite, and the bound with $L_0$ applies to both.

For $S=\{\infty\}$ only the two real terms with $\xi=\pm1$ occur. It follows that $D_S(A)=O_f(\sqrt A)$ as $A\downarrow0$ for both sets of places. This argument proves absolute convergence of the series after integrating the additive character over each shell.

Each $I_a(r)$ is continuous for $r>0$. Indeed, the difference of the weights at $r$ and $r'$ has absolute value at most $|\log r-\log r'|$. Extend to $r=0$ by zero. The majorants above are uniform for $0\le A\le A_0$ with any finite $A_0$. The shell and S-unit sums therefore converge locally uniformly and $D_S$ extends continuously to zero.

## Two-sided cutoffs

Let $d(A)=D_{\{\infty,2\}}(A)-D_{\{\infty\}}(A)$ for $A>0$ and $d(0)=0$. The one-sided result gives $d(A)\to C=-\log 2/(4\sqrt2)$ as $A\to\infty$. For $P=\lambda\lambda'$ and $R=\lambda/\lambda'$, the difference of the two-sided unfolded integrals is
$$
Q(\lambda,\lambda')=d(P)-d(R)-d(R^{-1})+d(P^{-1}).
$$
For a single value $w$ of the product frequency, this is inclusion–exclusion for the length of $[-\log\lambda,\log\lambda]\cap[\log|w|_S-\log\lambda',\log|w|_S+\log\lambda']$ in the real variable $\log|x|_S$.

| Schedule, with $\lambda,\lambda'\to\infty$ | Limit of $Q$ |
| --- | --- |
| $\lambda=\lambda'$ | $C-2d(1)$ |
| $\lambda/\lambda'\to q\in(0,\infty)$ | $C-d(q)-d(q^{-1})$ |
| $\lambda/\lambda'\to\infty$ or $\lambda/\lambda'\to0$ | $0$ |

In the last case the two large-cutoff limits cancel and the two small-cutoff terms vanish. In particular $\lambda=L^2,\lambda'=L$ gives zero in the unfolded two-sided expression, while the one-sided target is $C\ne0$. The endpoint estimates alone allow $d(A)=CA/(1+A)$, for which the finite-ratio value is zero for every $q$. A separate enclosure for the actual fixed test establishes a positive limit at $q=1$. [Balanced limit enclosure](S_LOCAL_EQUAL_RATIO.md)

The two analytic estimates give constants $M,K\ge0$ such that $|d(A)-C|\le M/A$ and $|d(A)|\le K\sqrt A$ for $A>0$. When $P,R$ both grow,
$$
|Q|\le M(P^{-1}+R^{-1})+K(P^{-1/2}+R^{-1/2}).
$$
Thus the quadratic schedule gives $O_f(L^{-1/2})$.

### A symmetric smoothed schedule

Choose smooth probability densities of upper thresholds supported in $[L^2-L^{-4},L^2]$ for position and $[L-L^{-2},L]$ for frequency. Average the symmetric band masks $\mathbf1_{[1/u,u]}$ against these densities. For $L\ge2$, each average is symmetric under $r\mapsto r^{-1}$ and vanishes outside $[1/\Lambda,\Lambda]$. It equals one on $[1/\Lambda+\varepsilon,\Lambda-\varepsilon]$ because $1/(\Lambda-\varepsilon)\le1/\Lambda+\varepsilon$ for both choices. The boundary widths satisfy $\Lambda\varepsilon\to0$.

The two masks produce an average of $Q(u,v)$. Each termwise integral is absolutely integrable. The one-sided bounds give uniform absolute summability over the two threshold intervals for each fixed $L$, so the summation over S-units may pass through the averaging. Uniformly on the thresholds, $uv\asymp L^3$ and $u/v\asymp L$. The same estimate gives $O_f(L^{-1/2})$ and hence zero limit for this smoothed unfolded schedule.

## Scope of the result

The proof applies to the unfolded Fourier integrals and their cutoff schedules. The follow-up constructs the finite-cutoff weighted compression and separates the upper and lower frequency terms. The expanding-window comparison and identification with the manuscript's diagonal remain open. [Weighted trace construction](S_LOCAL_WEIGHTED_QUOTIENT.md) · [Trace split](S_LOCAL_TRACE_SPLIT.md) · [S-local kernel and trace obligations](https://github.com/mccorvie/riemann-masullo/issues/7354)

## Lean replay

The Lean module verifies five implications used in the cutoff comparison. It derives the right-hand limit from a square-root bound, handles a positive finite cutoff ratio, handles a diverging ratio, proves symmetry in the reciprocal ratio, and specializes the zero limit to the quadratic schedule. The Fourier estimates and symmetric smoothing calculation are analytic inputs.

On 2026-11-26, the five declarations passed on Windows and Colab Linux in Lean 4.33.1 with Mathlib pinned to `0df444a360eaa60ab8c11dca51a86af692955474`. Both successful runs exited 0 with empty stderr and recorded only `propext`, `Classical.choice`, and `Quot.sound` for each declaration. The Colab retry uses the corrected normed-group import and preserves the earlier elaboration error in the preceding cell. The saved receipt was decoded from the runtime output and its SHA-256 matched the printed digest. The receipts agree apart from the host in the Lean banner. [Colab replay and retry](https://colab.research.google.com/drive/1lk8xiotmjQhvpchOMBGYcvswnkSQRlZL#scrollTo=aUH3blHCqdd2)

| Artifact | SHA-256 |
| --- | --- |
| Lean source | `6082f2764d047b8601a1c6813b81c67ec4d4439ea01e66ee30c28292dd9dfe81` |
| Windows receipt | `66b3cfb4a325761729a3454676a2699f0183f1ff61ebebba2bc30c4ec04b21f4` |
| Colab receipt | `4743ffe12e32d2a86f97da092bb17edbcd87d8fd3584ac815fbb649f7dcf441a` |

From `formal/landau` with the pinned Mathlib imports restored, run

~~~sh
lake env lean --root=../.. -j 1 ../../tests/lean/E2ASLocalCutoffSchedule.lean
~~~

[Lean source](../../tests/lean/E2ASLocalCutoffSchedule.lean) · [Windows replay receipt](s-local-cutoff-schedule-windows-replay.json) · [Colab replay receipt](s-local-cutoff-schedule-colab-replay.json)
