# Projection Bounds from Exterior Frequencies

For the fixed $L=4$ lower-frequency calculation, the Gram solve gives the finite projection $P_N$. The full unpolarized projection $P$ also has a description by test vectors in its orthogonal complement. This gives an upper bound that can remove the part of a row lying outside the target space. Work in the aligned positive-radius chart with band $[0,1]$, weight $w_D(x)=W(\log x-D)/W(-D)$, $D=\log L$, and strip half-width $\alpha=1/8$. The cosine transform $C$ is the unitary real Fourier transform on even profiles, written on the positive half-line. [Weighted quotient](S_LOCAL_WEIGHTED_QUOTIENT.md) · [Galerkin residual](S_LOCAL_LOW_GALERKIN.md)

## Constructing the orthogonal test vectors

Let $T$ be the dyadic sum for the two-place case and $T=I$ for the real place alone. Let $\Pi_{\rm ext}$ be multiplication by $\mathbf1_{(1,\infty)}$ in frequency and define
$$
 A=\Pi_{\rm ext} C T^{-1}:L^2(w_D\,dx)\longrightarrow L^2(dx).
$$
The inclusion into unweighted $L^2$ is bounded because $w_D\ge1/W(-D)$. The kernel of $A$ is exactly the unpolarized folded band. For an exterior frequency function $z$, its adjoint image is
$$
 v_z=w_D^{-1} (T^{-1})_{\rm flat}^* C z.
$$
Indeed $\langle v_z,u\rangle_{w_D}=\langle z,Au\rangle_{dx}$. Hence $v_z$ is orthogonal to the target band. In the dyadic case $T^{-1}f(x)=f(x)-f(2x)$ and
$$
 (T^{-1})_{\rm flat}^* C z=C(z-z(2\,\cdot)).
$$
The factor in the physical dilation adjoint is $1/2$. Omitting it would change the exterior-space test. In the real-place case the corresponding expression is simply $Cz$.

The closure of these adjoint images is the full orthogonal complement. A vector orthogonal to every adjoint image has $Au=0$ by testing against every exterior $z$. Thus any nested dense family of exterior trials gives upper bounds converging to $\|Pu\|_{w_D}^2$ if one takes the exact best fit in their adjoint images. No assumption about convergence of the finite Galerkin trace is needed for this identity.

## Computable residual bound

For any exterior trial $v_z$ and primal trial $g_N\in\operatorname{ran}P_N$, the three orthogonal components of the residual give
$$
 \|u-v_z-g_N\|_{w_D}^2
 =\|(P-P_N)u\|_{w_D}^2
  +\|P_Nu-g_N\|_{w_D}^2
  +\|(I-P)u-v_z\|_{w_D}^2 .
$$
A certified upper enclosure of a single residual integral therefore bounds the missing-basis term. One may approximate the two trial vectors independently. This formula also identifies which two trial errors prevent the computable bound from being sharp.

## Certified upper bounds for four rows

Use the constant Fourier row $u(x)=m(x)/\sqrt{x}$ on each extension strip $[1/4,1]$ and $[16,64]$. This is the constant outgoing row of the nuclear decomposition transported to the physical chart, with the normalized weight. Set $g_N=0$ for this test. Split the exterior frequency interval $[1,2]$ into equal disjoint packets $I_i$ and use $z_i=\mathbf1_{I_i}$. The intervals and their half-scale copies meet only on null sets. In flat $L^2$, the transforms $(T^{-1})_{\rm flat}^*Cz_i$ are orthogonal and have squared norm $\kappa|I_i|$, with $\kappa=1$ at the real place and $\kappa=3/2$ for two places. Consequently, for any coefficients $\gamma_i$,
$$
 \left\|\sum_i\gamma_i v_{z_i}\right\|_{w_D}^2
 \le W(-D)\kappa\sum_i|\gamma_i|^2 |I_i|.
$$
Optimizing the resulting quadratic bound on $\|u-\sum_i\gamma_i v_{z_i}\|_{w_D}^2$ gives
$$
 \|Pu\|_{w_D}^2\le \|u\|_{w_D}^2
 -\frac{1}{W(-D)\kappa}\sum_i
        \frac{|\langle v_{z_i},u\rangle_{w_D}|^2}{|I_i|}.
$$
This upper estimate uses the global lower bound on the weight in the dual norm. Splitting a packet can improve it by Cauchy–Schwarz. It need not become sharp on this fixed exterior interval. An in-band packet would fail the orthogonality requirement. For example, testing it against $TCz_i$ in the target space gives the nonzero flat pairing $\|z_i\|_{dx}^2$.

The packet transform uses a difference of sines divided by $\pi x$. For two places subtract its half-scale adjoint term. Arb encloses the pairings on each spatial strip, and the row norm integrates a polynomial times an exponential after substituting $s=\log(x/4)$. The 16-packet calculation yields the following outward-rounded bounds. “Reduction” is a strict lower bound for the amount subtracted from the ambient norm squared.

| Row | Places | Reduction in upper bound | Certified upper bound for $\|Pu\|_{w_D}^2$ |
| --- | --- | ---: | ---: |
| $[1/4,1]$ | $\{\infty\}$ | 0.02339 | 3.181115 |
| $[1/4,1]$ | $\{\infty,2\}$ | 0.005046 | 3.199459 |
| $[16,64]$ | $\{\infty\}$ | $3.37\times10^{-8}$ | 3.204505185 |
| $[16,64]$ | $\{\infty,2\}$ | 0.00020644 | 3.204299 |

The ambient squared norm is about $3.204505218$ for both strips. The 4-, 8-, and 16-packet comparisons give strict improvements over the ambient estimate in all four cases. The 106- and 160-bit runs both verify the table, and all 24 corresponding reported bounds and reductions overlap. The two runs use the same Arb integration method.

The four scalar upper bounds are **ACCEPT**. A trace enclosure still requires the incoming rows, finite primal trials, and the sum over the remaining row indices. The fixed-$L$ ordering stays **AMBER**.

The weighted Gram calculation improves these bounds on the same packet spans and bounds how much improvement is possible for the two outer rows with those spans. [Weighted Gram bounds](S_LOCAL_DUAL_GRAM.md)

## Replay

~~~powershell
uv run --no-project --python 3.14 --with python-flint==0.9.0 python tools/s_local_projection_upper.py
~~~

[Certificate driver](../../tools/s_local_projection_upper.py) · [106-bit result](s-local-projection-upper-106.json) · [160-bit replay](s-local-projection-upper-160.json)
