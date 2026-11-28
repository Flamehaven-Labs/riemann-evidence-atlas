# The S-local Sharp Cutoff over the Rationals

## Scope

This calculation uses the multiplicative sharp cutoffs and the unfolded distributional Fourier integral in Masullo, equations (12.4.1.16)–(12.4.1.24), pp. 518–519. The kernel identification on the manuscript's weighted invariant quotient and the smoothing limit in its Step III remain separate obligations. The sharp cutoff considered here is one-sided in the product norm, as in (12.4.1.22). Definition 9.3.3.1 on p. 427 uses a symmetric band. The footnote on p. 514 proposes extending that definition for the local calculation. [Pinned manuscript](README.md) · [G1 test and evidence](GEOMETRIC_TRACE_COMPARISON.md)

## Quotient coordinates and the test lift

For $S=\{\infty,2\}$ let $G_S=\mathbb R^\times\times\mathbb Q_2^\times$, $\Gamma_S=\{\pm2^n:n\in\mathbb Z\}$ embedded diagonally, and $J_S=G_S/\Gamma_S$. Write $|x|_S=|x_\infty||x_2|_2$. A fundamental domain is $\Omega_S=\mathbb R_{>0}\times\mathbb Z_2^\times$. Multiply first by $2^{-v_2(x_2)}$ and then by the sign of the real component to obtain the unique representative. Its first coordinate is $|x|_S$. For $S=\{\infty\}$ take $\Gamma_S=\{\pm1\}$ and $\Omega_S=\mathbb R_{>0}$.

Use Lebesgue measure on $\mathbb R$ and self-dual additive Haar measure $du$ on $\mathbb Q_2$ with $\operatorname{vol}(\mathbb Z_2)=1$. On $G_S$ the product multiplicative measure is $c_S\,dx/|x|_S$, with $c_S=2$ when $2\in S$ and $c_S=1$ otherwise. The angular factor of the fundamental domain at 2 then has mass $2\operatorname{vol}(\mathbb Z_2^\times)=1$.

Lift the G1 radial test $k(\log|g|_S)$ to $\widetilde\varphi(g)=k(\log g_\infty)$ on $\Omega_S$ and zero elsewhere. It is smooth and compactly supported on $G_S$. Its periodization $\sum_{\xi\in\Gamma_S}\widetilde\varphi(\xi g)$ is the stated test on $J_S$, as required by (12.4.1.4). The position mask $P_\lambda$ is multiplication by $\mathbf1_{|x|_S\le\lambda}$, and the frequency mask is $\mathcal F^{-1}P_{\lambda'}\mathcal F$. They commute with the diagonal S-unit dilations on the additive $L^2$ space since $|\xi|_S=1$. The masks and this commutation are defined before passage to the weighted quotient used in the manuscript.

## The unfolded diagonal integral

For a term $\xi\in\Gamma_S$, origin (12.4.1.16) and the substitution $z=g\xi-1$ give the additive test
$$
\eta_\xi(z)=|1+z|_S^{-1/2}\widetilde\varphi\bigl(\xi/(1+z)\bigr).
$$
Extend it by zero outside the support of this expression. The change of variables uses $|\xi|_S=1$ and $d\mu_S(g)=c_S\,dg/|g|_S$. Write $\widehat{\eta_\xi}$ for the additive Fourier transform with the positive sign in the character.

For a given $\xi$, change frequency variables to $w=xu$ in (12.4.1.22) and integrate $x$ over $\Omega_S$ with $|w|_S/\lambda'\le |x|_S\le\lambda$. The angular mass is one. The interval in $\log|x|_S$ has length $\log_+(A/|w|_S)$ for $A=\lambda\lambda'$ and $\log_+(v)=\max(0,\log v)$. This gives the normalized sharp unfolded expression
$$
D_{S,\xi}(A)
 =\int_{A_S}\widehat{\eta_\xi}(w)\log_+(A/|w|_S)\,dw .
$$
For each $\xi$, the Fourier transform is rapidly decreasing in the real coordinate and compactly supported and locally constant in the finite coordinate. The logarithm is locally integrable in each coordinate, so this single-term integral and the change of variables after forming $\widehat{\eta_\xi}$ are absolutely integrable. This argument starts from the unfolded integral in (12.4.1.22).

## Evaluation by additive Fourier inversion

Let
$$
f(x)=
\begin{cases}
(1+x)^{-1/2} k(-\log(1+x)),&x>-1,\\
0,&x\le-1 .
\end{cases}
$$
Then $f\in C_c^\infty((-1,0))$. At $\xi=1$, $\eta_1=f$ for $S=\{\infty\}$ and $\eta_1=f\otimes\mathbf1_{2\mathbb Z_2}$ for $S=\{\infty,2\}$. The finite factor follows from $1+z_2\in\mathbb Z_2^\times$. Since $\eta_\xi(z)=\eta_1((z+1)/\xi-1)$, substituting $v=\xi w$ in the integral changes the Fourier factor to $\psi_S(av)\widehat{\eta_1}(v)$, where $a=1-\xi^{-1}$. The product norm and measure are unchanged. The finite Fourier factor is $\frac12\mathbf1_{|v_2|_2\le2}$.

For the additive character of conductor $\mathbb Z_2$ the integral over a ball is
$$
B_j(a)=\int_{|u|_2\le2^j}\psi_2(au)\,du
=2^j\mathbf1_{\,|a|_2\le2^{-j}} .
$$
This follows from translation invariance on the ball and the criterion for the character to be trivial there. Put $c_j(a)=B_j(a)-B_{j-1}(a)$, the shell integral. The Fourier mass of $\eta_\xi$ is zero for every $\xi$. For $n=0$ this uses $f(0)=f(-2)=0$, and for $n\ne0$ it uses either $B_1(a)=0$ or $f(\xi^{-1}-1)=0$. Equivalently, $\eta_\xi(0)=\widetilde\varphi(\xi)=0$.

After the limit in a fixed term, the factor $-\log|v|_S$ splits into real and finite logarithms. For $S=\{\infty,2\}$ this gives
$$
D_{S,\xi}(\infty)
=-\frac12 B_1(a)\int_{\mathbb R}\widehat f(s)e^{2\pi ias}\log|s|\,ds
-\frac{\log 2}{2}\,f(-a)\sum_{j\le1}j\,c_j(a).
$$
Here $\int\widehat f(s)e^{2\pi ias}\,ds=f(-a)$. The real term is retained only for $\xi=\pm1$, where $B_1(a)=2$. Those two terms coincide with the entire unfolded result for $S=\{\infty\}$. In the finite term, the support of $k$ forces $\xi=2$. Then $a=1/2$, $B_j(1/2)=2^j$ for $j\le-1$ and zero for $j\ge0$. Summation by parts gives
$$
\sum_{j\le1} j\,c_j(1/2)=-\sum_{j\le-1}2^j=-1 .
$$
Since $f(-1/2)=\sqrt2\,k(\log2)$, the difference of the limiting unfolded expressions is
$$
D_{\{\infty,2\}}(\infty)-D_{\{\infty\}}(\infty)
 = \frac{\log2}{2}\sqrt2\,k(\log2)
 = -\frac{\log2}{4\sqrt2}.
$$
The coefficient was computed from the Fourier integral over the additive shells.

The exact arithmetic check sums the characters on finite dyadic quotients using integer cancellation of opposite roots. It computes the log weight $-1$ for $a=1/2$ at truncation depths 8, 16, and 24 using an exact low-radius tail. For the unit character parameter $a=1$, the corresponding weight is $-2$. [Exact shell check](../../tools/s_local_dyadic_shell_check.py)

## Sum of cutoff errors

For a fixed $\xi$, subtract the integral with weight $\log A-\log|v|_S$. The constant integrates to zero as above. The error for $S=\{\infty,2\}$ is
$$
E_\xi(A)=\frac12\sum_{j\le1}c_j(a)
\int_\mathbb R\widehat f(s)e^{2\pi ias}\ell_{A,j}(s)\,ds,
\qquad
\ell_{A,j}(s)=\log_+(2^j|s|/A).
$$
Let $C_0=\int|s\widehat f(s)|\,ds$ and $C_1=\int|s\widehat f'(s)|\,ds+\int|\widehat f(s)|\,ds$. Both are finite. For $j\le1$, $\ell_{A,j}(s)\le 2|s|/A$ and its weak derivative is bounded by $2/A$. Thus the integral has absolute value at most $2C_0/A$. For $a\ne0$, integration by parts also bounds it by $C_1/(\pi A |a|)$, using the integrable weak derivative of $\widehat f\ell_{A,j}$.

- For $\xi=\pm2^n$ with $n\ge1$, $|a|_2=2^n$. The ball formula gives $\frac12\sum_{j\le1}|c_j(a)|=2^{-n}$. The first bound sums over these $\xi$.
- For $n\le-1$, $a$ is a 2-adic unit and $\frac12\sum_{j\le1}|c_j(a)|=1$. Its real absolute value is at least $2^{-n-1}$. The integration-by-parts bound sums over these $\xi$.
- For $\xi=\pm1$, the half-sum of the absolute shell weights is one. There are two terms and the first bound applies. Each real-only error is bounded by $C_0/A$.

In particular
$$
\left|\big(D_{\{\infty,2\}}(A)-D_{\{\infty\}}(A)\big)
       +\frac{\log 2}{4\sqrt2}\right|
\le \frac{10C_0+4C_1/\pi}{A}.
$$
Here $D_S(A)$ denotes the sum of the unfolded terms. This proves convergence for the one-sided sharp unfolded calculation and justifies summing the limits. For example, the choice $\lambda=\lambda'=L$ gives an $O_f(L^{-2})$ error. The constants are expressed by norms of the fixed Fourier transform.

The same bound applies to one-sided smooth monotone masks that equal $1$ for $r\le L-\varepsilon$ and $0$ for $r\ge L$. Each mask is a probability mixture of sharp upper bounds with thresholds in $[L-\varepsilon,L]$, using the negative derivative of the mask as the density. Average the two-cutoff calculation over the position and frequency thresholds. The uniform bound with $A\ge(L-\varepsilon)^2$ justifies averaging the sum of terms and gives an error bounded by $(10C_0+4C_1/\pi)/(L-\varepsilon)^2$. The schedule $\varepsilon=L^{-2}$ for $L\ge2$ satisfies $\varepsilon L\to0$ in (12.4.1.28). This is a smoothing result for the unfolded one-sided expression.

## Remaining operator comparison

On a two-sided sharp product-norm band $[1/\lambda,\lambda]$ in position and $[1/\lambda',\lambda']$ in frequency, inclusion–exclusion in the same unfolded expression gives
$$
D_S(\lambda\lambda')-D_S(\lambda'/\lambda)
-D_S(\lambda/\lambda')+D_S(1/(\lambda\lambda')) .
$$
The two middle terms depend on the relative cutoff schedule. The follow-up proves a small-cutoff estimate and gives the limit for each ratio regime. A comparison with the manuscript must identify the kernel of the weighted quotient operator and justify tracing it along its diagonal for the chosen cutoff. Those steps remain open. [Two-sided cutoff limits](S_LOCAL_BAND_LIMITS.md) · [S-local kernel and trace obligation](https://github.com/mccorvie/riemann-masullo/issues/7354)
