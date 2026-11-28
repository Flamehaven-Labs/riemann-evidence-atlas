# The Weighted S-Local Quotient at a Fixed Frequency Level

We use the pinned 20 November manuscript, $F=\mathbb Q$, $S=\{\infty\}$ or $S=\{\infty,2\}$, the trivial angular type, Sobolev order $s=2$, and $0<\alpha<1/2$. The calculation below identifies the dense core of the stated product-norm Paley–Wiener level. Smooth upper and symmetric frequency gates descend on this core and extend to bounded maps on the weighted ambient space. A compact spatial mask then gives a trace-class compression with an integrable trace density at any fixed level. The comparison with the two simultaneous limits in NR-01 is still open. [Pinned manuscript and SHA-256](README.md) · [NR-01](NEGATIVE_RESULT_REGISTER.md)

## Which cutoff does the manuscript use?

| Location | Operation |
| --- | --- |
| Definition 9.3.3.1, p. 427 | Multiplicatively symmetric scalar spatial mask, supported in $[1/\Lambda,\Lambda]$ and equal to one on the smaller plateau. Our smoothed band profiles satisfy these scalar conditions. |
| (7.3.2.12)–(7.3.2.17), p. 355, and Definition 11.2.1.3, pp. 488–489 | Take the theta image of the Bruhat core whose additive Fourier transform has compact support inside the product-norm region, impose the two origin conditions, and take the specified closure. The latter definition uses the weighted Hilbert closure. |
| Theorem 12.4.1.1, footnote 2, p. 514 | The proposed independent lower endpoint occurs in the spatial cutoff. The resulting logarithmic lower endpoint is $\max\{|w|_S/\lambda',1/\lambda''\}$. |
| Step II, pp. 516–517 | The displayed composite is $M_\rho A_{\widetilde\varphi}\mathcal F_S^{-1}M_{\rho'}\mathcal F_S$. Both displayed masks smooth upper product-norm inequalities. The frequency multiplier has no lower hole. |

Thus NR-01's symmetric frequency band changes Step II. Its two schedules can be tested on a compression with that extra frequency gate once the gate and its effect on the weighted level have been justified. The public discussion also analyzes the spatial floor and optional lower frequency hole separately. [Independent lower cutoffs in Issue #7354](https://github.com/mccorvie/riemann-masullo/issues/7354#issuecomment-7153102915)

## The trivial angular core

Use the quotient chart $J_{\{\infty,2\}}\simeq\mathbb R_{>0}\times\mathbb Z_2^\times$ with angular Haar mass one. The norm from (10.1.1.5), at $a=1/2$ and $I=[-\alpha,\alpha]$, is
$$
 \|\Phi f\|^2=\int_0^\infty |\Phi f(r)|^2 W(\log r)\,dr,
 \qquad W(t)=e^{2\alpha|t|}(1+t^2).
$$
In the half-twisted logarithmic chart the vector is $e^{t/2}\Phi f(e^t)$ and the measure is $W(t)\,dt$. In the formulas below put $\Pi f=\Phi f/2$ to absorb the two real signs. A common nonzero constant leaves the level and compression unchanged.

Angular averaging commutes with the theta map and preserves the product-norm support condition and the two origin conditions. We may use functions even in the real variable and invariant under the finite units. Write a finite tensor decomposition of $\widehat f$ as
$$
 \widehat f(x,u)=\sum_j h_j(x)\mathbf 1_{2^j\mathbb Z_2}(u).
$$
Such a decomposition is obtained by subtracting consecutive shell values. If $\widehat f$ is supported where $|x||u|_2\le Y$, its value on the shell $v_2(u)=j$ vanishes for $|x|>2^jY$. Thus each difference $h_j$ is supported in $[-2^jY,2^jY]$. Set
$$
 h(v)=\sum_j h_j(2^j v).
$$
Then $h$ is smooth, even and supported in $[-Y,Y]$. Moreover $h(0)=\widehat f(0,0)$ and $\int_{\mathbb R}h=\int_{\mathbb R\times\mathbb Q_2}\widehat f=f(0,0)$. The factors in the last identity are exactly $\operatorname{vol}(2^j\mathbb Z_2)=2^{-j}$.

For $r>0$ define $Tg(r)=\sum_{i\ge0}g(2^i r)$ on Schwartz input, and let $C$ be the real Fourier transform on even functions, restricted to $r>0$. The theta sum on a tensor $a(x)\mathbf1_{2^j\mathbb Z_2}(u)$ is $\sum_{i\ge j}a(2^i r)$. The finite-place inverse transform sends $\mathbf1_{2^j\mathbb Z_2}$ to $2^{-j}\mathbf1_{2^{-j}\mathbb Z_2}$. The real Fourier scaling identity is $C(h_j(2^j\,\cdot))(r)=2^{-j}(C h_j)(2^{-j}r)$. Applying the theta sum to the finite tensors gives
$$
 \Pi\widehat f=T h,\qquad \Pi f=T C h.
$$
Conversely every even smooth $h$ supported in $[-Y,Y]$ with $h(0)=\int h=0$ is obtained by taking $\widehat f=h\otimes\mathbf1_{\mathbb Z_2}$. For $S=\{\infty\}$ the same statement uses $T=I$. The unweighted operator $T=\sum_{i\ge0}2^{-i/2}E_i$ converges in operator norm, where $E_i g(r)=2^{i/2}g(2^i r)$ is unitary on $L^2(dr)$.

This identifies the weighted level as the closure of the displayed core in $L^2(W(\log r)\,dr)$. On the core, $Ch$ vanishes to order at least two at the origin and is rapidly decreasing at infinity. Splitting the sum at $2^i r=1$ gives $TCh=O(1)$ at zero and rapid decay at infinity, which puts it in the weighted space for the stated width. The follow-up identifies the surviving origin condition and its orthogonal projection. The dyadic fold agrees with the arithmetic theta model discussed upstream. [Weighted closure and projection](S_LOCAL_TRACE_SPLIT.md) · [One-prime projector calculation](https://github.com/mccorvie/riemann-masullo/issues/7354#issuecomment-7152208733)

## Descending a smooth frequency gate

Let $q$ be a smooth upper or symmetric frequency mask, constant near the origin and zero above its finite upper threshold. Extend it evenly to $\mathbb R$. On a core lift, multiplication of $\widehat f$ by $q(|x||u|_2)$ preserves compactly supported Schwartz–Bruhat functions. In fact the real coordinate has bounded support, so the mask is constant on a uniform sufficiently small dyadic ball in the finite coordinate. On the remaining finitely many valuation shells in the support it is a smooth real multiplier. The product still vanishes at the additive origin, while its integral can change. We use the weighted ambient space as codomain.

In the quotient chart let $M_q$ mean multiplication by $q(r)$. Since the product norm is invariant under the summation group, the folded Fourier profile of the gated input is $M_q T h$. The folded physical profile of its inverse transform is $TC^{-1}T^{-1}M_q T h$. In terms of the original physical profile $TC^{-1}h$ the resulting operator is
$$
 K_q=T C^{-1} T^{-1} M_q T C T^{-1}.
$$
Here $C^{-1}=C$ on even functions. The calculation identifies the same result for every core lift of a given profile, since $T$ and $C$ are invertible in flat $L^2(dr)$. For $S=\{\infty\}$ set $T=I$. [Upstream frequency-gate descent](https://github.com/mccorvie/riemann-masullo/issues/7354#issuecomment-7152334021)

The operator bound on $L^2(W(\log r)\,dr)$ can be chosen independently of the two frequency endpoints. Let $B g(r)=g(2r)$ and $\widetilde B g(r)=g(r/2)/2$. For both families of powers the dilation estimate is $O((1+j)2^{-(1/2-\alpha)j})$ in the weighted norm. This follows by changing variables and bounding $W(t\pm j\log2)/W(t)$ by $2(1+(j\log2)^2)2^{2\alpha j}$. Consequently $T=\sum_{j\ge0} B^j$ and $T^{-1}=I-B$ are bounded there. In the flat formula,
$$
 T^{-1}M_qT=M_q+M_{q-q(2\,\cdot)}\sum_{j\ge1}B^j,
 \qquad C^{-1}B^j C=\widetilde B^{\,j}.
$$
To bound the conjugated multipliers uniformly, put $w(r)=W(\log|r|)$ on the full line. It is an $A_2$ weight. On a centered interval of radius $R\le1$, substitute $r=Rv$ to compare the averages of $w$ and $1/w$ to $w(R)$ and $1/w(R)$. Both normalized integrands are bounded by $2 v^{-2\alpha}(1+\log^2 v)$ for $0<v\le1$. For $R\ge1$ the same comparison works on $1\le r\le R$. The part below one contributes finite integrals, and both $Rw(R)$ and $R/w(R)$ are bounded below there as functions of $R\ge1$. On an interval whose distance to zero exceeds its length, $w$ is comparable to a constant because the endpoint radii differ by a factor of at most two. Every other interval is contained in a centered one of at most four times its length. These bounds prove the $A_2$ condition.

The weighted Hilbert transform bound now gives a uniform bound for projections onto frequency half-lines. Modulation implements a change of endpoint and is unitary on $L^2(w\,dr)$. A sharp symmetric band is a sum of at most two interval projections, and the smoothed masks in NR-01 are probability averages of these sharp bands. Thus $C^{-1}M_q C$ and $C^{-1}M_{q(2\,\cdot)} C$ have a common bound $N_\alpha$ independent of the endpoints and smoothing widths. By the power estimate and the displayed operator identity,
$$
 \|K_q\|\le \|T\|\|T^{-1}\|N_\alpha
       \left(1+2\sum_{j\ge1}\|\widetilde B^{\,j}\|\right).
$$
The same bound defines sharp band gates by the weighted extension of the flat formula. The compact smooth core computation above identifies the smooth gates with the descended additive action. [Weighted Hilbert transform bound, Corollary 1.8](https://arxiv.org/pdf/0906.1941)

## A finite-level weighted trace with both projection legs

Let $P_{S,Y}$ be the orthogonal projection onto that weighted level in the half-twisted logarithmic chart. Use the smooth frequency action $K_q$ just constructed. A matching sharp upper gate $\mathbf1_{|u|_S\le Y}$ is also allowed on the input level, where it acts as the identity by the core support condition. Let $m$ be a bounded spatial mask supported in a compact interval of the logarithmic coordinate. In the angular-trivial chart the cutoff convolution is
$$
 (M_m A_k F)(t)=m(t)\int_{\mathbb R}k(t-u)F(u)\,du.
$$
Here $k$ is the fixed smooth compact G1 test and the sign follows from the source action $f(x)\mapsto f(g^{-1}x)$. Use the orthogonal compression $P_{S,Y}M_m A_k K_q P_{S,Y}$, transporting $K_q$ from the positive-radius chart. For the matching sharp upper gate use $K_q=I$ in this expression.

There is a trace-class proof at every fixed $Y$ and for every such $m$. Choose compact intervals $I,J$ with $\operatorname{supp}m\subset I$ and $I-\operatorname{supp}k\subset J$. Under the unitary multiplication by $\sqrt W$ to ordinary $L^2(dt)$ the kernel is
$$
 m(t)\sqrt{W(t)}\ \mathbf1_J(u)\, k(t-u)/\sqrt{W(u)}.
$$
Periodize $k$ with a period large enough that there is no overlap with its translates on $I-J$. Its Fourier coefficients $c_n$ satisfy $\sum_n|c_n|<\infty$ by two integrations by parts. With angular frequencies $\nu_n$ define
$$
 a_n(t)=m(t)\sqrt{W(t)}e^{i\nu_n t},
 \qquad b_n(u)=\mathbf1_J(u)e^{i\nu_n u}/\sqrt{W(u)}.
$$
Both norms are independent of $n$. Write $\mathscr P$ and $\mathscr K$ for the transported projection and frequency operator. The compressed kernel has the nuclear expansion
$$
 \sum_{n\in\mathbb Z} c_n\,(\mathscr P a_n)\otimes(\mathscr P\mathscr K^* b_n)^*.
$$
The sum converges in trace norm, with bound $\|K_q\|\|m\sqrt W\|_2\|\mathbf1_J/\sqrt W\|_2\sum_n|c_n|$, and its kernel converges in $L^2(dt\,du)$. The trace density is the $L^1(dt)$ sum
$$
 D_{S,Y,m}(t)=\sum_{n\in\mathbb Z}c_n(\mathscr P a_n)(t)
                       \overline{(\mathscr P\mathscr K^* b_n)(t)}.
$$
For every bounded test multiplier $v$, the integral $\int vD_{S,Y,m}$ is the trace of the compressed operator followed by $M_v$ (in the unitary Haar chart). This proves that the density is independent of the Fourier expansion and determines the integrated diagonal. Taking $v=1$ gives the trace of this fixed-level compression. The trace density uses both projection legs. Identifying it with a specified regularization of the manuscript's Step III diagonal requires a separate comparison. [Upstream projected-kernel construction](https://github.com/mccorvie/riemann-masullo/issues/7354#issuecomment-7153272235)

For a spatial mask $|m|\le1$ supported in an interval of length $\ell$, split it into at most $1+\lceil\ell\rceil$ pieces of length at most one. The trace norm bound for each piece is uniform in its center. Indeed $I-J$ stays in a fixed bounded interval, so the same Fourier series works for all pieces, and $W(t)/W(u)$ is bounded uniformly for $t\in I,u\in J$. Summing gives $\|P_{S,Y}M_m A_k K_qP_{S,Y}\|_{S_1}\le C_{\alpha,k}(1+\ell)$, uniformly in $Y$ and the frequency endpoints. For the symmetric spatial masks this is $O_{\alpha,k}(1+\log\lambda)$. An estimate on the cancellation of the corresponding densities is needed for convergence of the trace difference.

## Why the printed additive multiplier needs a domain argument

A Schwartz–Bruhat function on $\mathbb R\times\mathbb Q_2$ has a single finite depth $N$ of translation invariance by $2^N\mathbb Z_2$ in the finite variable, uniform in the real variable. This follows from the finite tensor description and the compact support and local constancy of each finite-place factor. Take $f=a\otimes\mathbf1_{\mathbb Z_2^\times}$, where $a$ is a nonzero real even smooth bump supported away from $0$. Then $f\in\mathcal S_{00}$ as described in Remark 7.2.1.3. On $\mathbb Z_2$ its finite-place Fourier transform is $1/2$.

Let $\rho'$ be either an upper mask equal to one near zero and zero above its cutoff, or a symmetric band mask with a nonempty plateau and $\rho'(0)=0$. In both cases there is an open positive interval on which $\rho'$ differs from $\rho'(0)$. For each proposed depth $N\ge0$, choose $r$ in that interval with $\widehat a(2^N r)\ne0$, which is possible by real analyticity and nonvanishing of the Fourier transform. At the common real frequency $x=2^N r$, the points $u=0$ and $u=2^N$ lie in the same additive coset and have product norms $0$ and $r$. Their values in $M_{\rho'}\widehat f$ differ. Hence $M_{\rho'}\widehat f$ is outside Schwartz–Bruhat space. Fourier inversion cannot give the stated endomorphism of that space for this input. The input here tests the stated domain on p. 516. On the fixed band core with the matching sharp gate the multiplier is the identity, as used above.

This obstruction precedes the issue of which polar functionals survive closure. The Lean file checks the dyadic product norm and the failure of uniform dyadic invariance given the nonvanishing and mask conditions. The analytic proof supplies those conditions and the tensor characterization. [Lean source](../../tests/lean/E2ASLocalQuotientCore.lean)

Both declarations replayed with Lean 4.33.1 and Mathlib at 0df444a360eaa60ab8c11dca51a86af692955474 on Windows and Colab Linux. The receipts match except for the host target. The Colab file was reconstructed byte-for-byte from the notebook's emitted receipt and checked against its SHA-256. These are replays of the two dyadic declarations. The weighted norm and trace arguments above are analytic. [Windows receipt](s-local-quotient-core-windows-replay.json) · [Colab receipt](s-local-quotient-core-colab-replay.json) · [Colab notebook](https://colab.research.google.com/drive/1J6V0BVISTLJCzvjX-4tjQLqxUGhSrxsC)

## What is still needed for NR-01

Each compact symmetric spatial mask and smooth symmetric frequency mask of NR-01 can now be inserted into the compression at its own finite $Y$. To use this family as a model for Step III, the choice of $Y$ and the diagonal regularization must be related to the manuscript. The trace norm bound grows with the spatial interval and gives no vanishing remainder. The next comparison is between the projected trace densities and the unfolded densities, with particular attention to the projection, any surviving origin constraints and the two cutoff edges. The sign and size of the limiting difference remain open. [Optional lower frequency hole](https://github.com/mccorvie/riemann-masullo/issues/7354#issuecomment-7153102915) · [Open source comparison](https://github.com/mccorvie/riemann-masullo/issues/7354)

At $Y=\lambda'$ the rescaling $r\mapsto Yr$ takes the level-one core to the level-$Y$ core, since $T$ commutes with scaling and the two zero conditions on $h$ are preserved. In the aligned coordinate $v=t+\log Y$ the level is therefore the closure of a single core with the shifted weight $W(v-\log Y)$. Set $D=\log Y$. On $|v|\le R\le D$,
$$
 \frac{W(v-D)}{W(-D)}
 = e^{-2\alpha v}\frac{1+(v-D)^2}{1+D^2},\qquad
 \left|\frac{W(v-D)}{W(-D)}-e^{-2\alpha v}\right|
 \le e^{2\alpha R}\frac{2RD+R^2}{1+D^2}.
$$
The local limiting weight at fixed positive width is $e^{-2\alpha v}$. Any comparison using a flat weight must account for this factor. Local convergence of the weights by itself provides no estimate for projections on the whole line.

The spatial floor in this aligned coordinate is $\log(\lambda'/\lambda)$. The product of the spatial top and the additive frequency floor is $\lambda/\lambda'$. These quantities stay at $0$ and $1$ on the balanced schedule, and tend to $-\infty$ and $+\infty$ on the quadratic schedule, respectively. This identifies the two different regimes a uniform projected-density calculation must cover.
