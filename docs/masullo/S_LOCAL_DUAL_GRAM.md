# Weighted Gram Bounds for Exterior Frequency Trials

At $L=4$ and $\alpha=1/8$, the same 16 exterior frequency packets give stronger upper bounds on all four constant outgoing row norms. The computation encloses their weighted Gram matrix and bounds the gain from optimizing over their span. [Exterior test vectors and row definitions](S_LOCAL_PROJECTION_BOUNDS.md)

| Row | Places | Previous upper bound for $\|Pu\|_{w_D}^2$ | New certified upper bound |
| --- | --- | ---: | ---: |
| $[1/4,1]$ | $\{\infty\}$ | 3.181115 | 2.957967782 |
| $[1/4,1]$ | $\{\infty,2\}$ | 3.199459 | 3.178366625 |
| $[16,64]$ | $\{\infty\}$ | 3.204505185 | 3.204504881755 |
| $[16,64]$ | $\{\infty,2\}$ | 3.204299 | 3.203995523 |

The 160-bit run also bounds the optimal reductions for the outer row from above by $3.369286\times10^{-7}$ and $0.000510471$, respectively. These are ceilings for the gain from the current 16-packet spans. Improving the matrix integration or solve can recover only the difference between the lower and upper gain estimates for these spans.

## Enclosing the weighted Gram matrix

Write $v_i=f_i/w_D$, where $f_i=(T^{-1})_{\rm flat}^*Cz_i$ and $z_i=\mathbf 1_{[a_i,b_i]}$, with $a_i=1+i/16$ and $b_i=a_i+1/16$. At the real place, the flat profile is
$$
 f_i(x)=\frac{\sin(2\pi b_i x)-\sin(2\pi a_i x)}{\pi x}.
$$
For two places subtract $(\sin(\pi b_i x)-\sin(\pi a_i x))/(\pi x)$. The weighted Gram entries are $G_{ij}=\int_0^\infty f_i f_j/w_D\,dx$. Use the product-to-sum identity for the sine products and integrate the resulting scalar cosine moments on $[a,R]$, with $a=2^{-12}$ and a split at $x=4$. The formula $1-\cos(2z)=2z^2\operatorname{sinc}^2(z)$ removes the division by $x^2$ in each moment. The resulting core matrix $G_c$ is positive definite. A linear combination of the sine numerators that vanishes on this interval vanishes identically by analyticity. The full-line flat profiles are independent by unitarity of the cosine transform and the disjoint packet interiors, including the half-scale copies in the two-place case.

The two omitted tails are positive semidefinite. Set $S=W(-\log4)$ and $\beta=1/4$. On $(0,a)$, $|f_i|\le c/16$ with $c=2$ or $3$ according to the place set. The Cauchy–Schwarz estimate and $1/w_D(x)\le S(x/4)^\beta/(1+\log^2(a/4))$ give the operator bound
$$
 \tau_0=\frac{c^2 S}{16\cdot 4^\beta(1+\log^2(a/4))}
           \frac{a^{1+\beta}}{1+\beta}.
$$
On $(R,\infty)$ use $F(x)=1/(\pi^2x^2 w_D(x))$. For a packet coefficient vector $\gamma$, the sine numerator of the sum has adjacent difference coefficients $d_j$, including the two endpoints, with $\sum_j |d_j|^2\le 4\|\gamma\|_2^2$. The sine harmonics within each scale are orthogonal on any period of length 32. The mean square of the numerator over one period is therefore at most $h\|\gamma\|_2^2$, with $h=2$ at the real place and $h=8$ for two places by the squared triangle bound. Since $F(x)\le F(R)(x/R)^{-2-\beta}$ for $x\ge R\ge 4$, summing upper bounds by periods gives
$$
 \tau_\infty=hF(R)\left(32+\frac{R}{1+\beta}\right),
 \qquad G_c\preceq G\preceq G_c+(\tau_0+\tau_\infty)I.
$$

For the pairing vector $b=(\langle v_i,u\rangle_{w_D})_i$, inversion reverses these positive-definite matrix bounds. Arb encloses both scalar expressions using interval linear solves:
$$
 b^*(G_c+(\tau_0+\tau_\infty)I)^{-1}b
 \ \le\ b^*G^{-1}b\ \le\ b^*G_c^{-1}b.
$$
Subtracting a certified lower endpoint of the left expression from an upper endpoint of $\|u\|_{w_D}^2$ gives the projection bound. The saved projection field encloses this upper-bound expression, and the tail fields enclose upper-bound expressions for the tail operator norms.

## Replay and scope

~~~powershell
uv run --no-project --python 3.14 --with python-flint==0.9.0 python tools/s_local_dual_gram.py --precision 106 --radius 128 --report dual-gram-106.json
uv run --no-project --python 3.14 --with python-flint==0.9.0 python tools/s_local_dual_gram.py --precision 160 --radius 256 --report dual-gram-160.json
~~~

The larger-radius run strictly tightened all four brackets for the full optimal reductions. Direct integration of the sine products reproduced eight sampled core entries in each run within the corresponding Arb balls. This checks the cosine-moment assembly through a different integrand using the same Arb integration library. The reports bind the generator, reused pairing code, and fixed G1 Lean source by SHA-256.

**ACCEPT** for both weighted Gram enclosures and the four constant outgoing projection bounds. **AMBER** for a sufficient outer-strip improvement, the joint primal and dual bound for the omitted-basis residual, the full trace error, and the two cutoff schedule limits. The next bound for the omitted-basis residual needs a certified lower estimate of $\|P_Nu\|^2$ or a direct integral of the joint trial residual.

The subsequent scalar certificates now give lower estimates of $\|P_Nu\|^2$ and combined residual bounds for these four rows. [Primal projection bounds](S_LOCAL_PRIMAL_RESIDUAL.md)

[Certificate driver](../../tools/s_local_dual_gram.py) · [106-bit report](s-local-dual-gram-106.json) · [160-bit report](s-local-dual-gram-160.json)
