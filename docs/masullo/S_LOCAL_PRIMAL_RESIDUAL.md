# Primal Projection Bounds for the 128-Cell Space

The trial space is the unpolarized Galerkin space at $L=4$ and $\alpha=1/8$. The extra dyadic nodes in the mesh coincide with nodes of the uniform 128-cell mesh at this level. The test rows are the constant outgoing rows on $[1/4,1]$ and $[16,64]$ for the two place sets. [Galerkin space](S_LOCAL_LOW_GALERKIN.md) · [Dual bounds](S_LOCAL_DUAL_GRAM.md)

For any $g$ in the finite space, orthogonality gives
$$
 \|P_Nu\|_w^2
 =2\operatorname{Re}\langle u,g\rangle_w-\|g\|_w^2
  +\|P_Nu-g\|_w^2.
$$
A floating-point Galerkin solve supplies trial coefficients. Round them to multiples of $2^{-40}$ and certify the scalar pairing and norm for that exact trial. The variational identity makes the certificate valid for any such trial. An upper bound $U$ for $\|Pu\|_w^2$ and this lower bound $L_N$ give $\|(P-P_N)u\|_w^2\le U-L_N$.

## Certified bounds

| Row support | Places | Lower bound on $\|P_Nu\|_w^2$ | Upper bound on $\|(P-P_N)u\|_w^2$ |
| --- | --- | ---: | ---: |
| $[1/4,1]$ | $\{\infty\}$ | 2.5730 | 0.3850 |
| $[1/4,1]$ | $\{\infty,2\}$ | 1.4778 | 1.7005 |
| $[16,64]$ | $\{\infty\}$ | 2.6859 | 0.5186 |
| $[16,64]$ | $\{\infty,2\}$ | 1.4346 | 1.7694 |

For the last row, the direct trial in the report gives a lower bound of 0.8826 and a residual upper bound of 2.3214. The table uses the rescaled trial $(79/128)g$. Given the saved lower expression $p$ for the pairing and upper expression $n$ for the squared norm, the objective for $tg$ is bounded below by $2tp-t^2n$ for $t\ge0$. Here $p$ is the saved finite pairing minus the pairing error. Recombining the two expressions at $t=79/128$ with interval arithmetic verifies the last row without repeating the integrals.

**ACCEPT** for the four lower bounds and four residual upper bounds at the fixed cutoff. **AMBER** for the full trace error and schedule ordering. These bounds cover the four constant outgoing rows. The two-place outer row has a pairing error cap of about 0.298 and a core norm error cap of about 0.354. Tightening those dyadic tail caps would improve the scalar certificate for this trial span. The other outgoing rows, incoming rows, and Fourier tail are open.

The follow-up certifies the matching constant incoming rows and combines both legs in a trace error bound for the constant term. [Constant incoming rows](S_LOCAL_CONSTANT_TERM.md)

## Enclosing the scalar integrals

Let $h$ be the even extension of the affine interpolant through the 129 nodal values. The last nodal value is zero. On the positive line the flat transform is $f(x)=2\int_0^1h(\xi)\cos(2\pi x \xi)\,d\xi$. If $s_j$ are the slopes of the 128 affine pieces, two integrations by parts give
$$
 f(x)=\frac{d_0+\sum_{j=1}^{128}d_j\cos(2\pi jx/128)}{2\pi^2x^2},
 \qquad
 d_0=-s_0,\quad d_j=s_{j-1}-s_j\ (1\le j<128),\quad d_{128}=s_{127}.
$$
The real-place trial is $g=f$. The two-place trial is $g(x)=\sum_{j\ge0}f(2^jx)$. Evaluate its finite truncation separately on each dyadic radial panel. With $D=\sum_j|d_j|/(2\pi^2)$, a sum starting at dilation $2^m$ is bounded in absolute value by $4D/(3\cdot 4^m x^2)$. Integrate the square of this bound using the maximum of the weight on the panel. For the row pairing apply Cauchy–Schwarz on the row support, which is a union of the same panels. For the core norm apply the triangle inequality to the finite trial and the remainder.

When each omitted dilation traverses an integer number of periods on a panel $[\ell,2\ell]$, there is a second bound for the squared error. Using the root mean square $B$ defined below, it is $w_{\max}\ell^{-3}(4B/(3\cdot4^m))^2$. Arb can select this bound when it is smaller. The retained dilations with $2^jx\le1/8$ on a whole panel are grouped into a degree-16 Taylor polynomial. The uniform error in this group is at most $A(\pi/4)^{18}/(18!(1-2^{-18}))$, by the cosine remainder and the geometric sum over these dilations. Its weighted norm is included in the same error estimate.

For $x$ below the radial core, the transform also satisfies $|f(x)|\le A$, using the computable majorant for $2\int_0^1|h(\xi)|\,d\xi$ from the absolute nodal values. In the two-place case, use $|f(y)|\le |f(0)|+2\pi^2Ay^2$ for $y=2^jx<1/8$. There are at most seven dilations with $1/8\le y<16$, each bounded by $A$. Bound the remaining terms by the geometric series. On writing $x=a e^{-r}$ for the lower endpoint $a$, the number of small dilations is bounded by $1+\log((1/8)/a)/\log 2+r/\log 2$. The resulting affine bound in $r\ge0$ can be squared and integrated against the weight and Jacobian using exponential moments. At the real place use the constant bound $A$.

For $x\ge R$, write $x^2f(x)=F(x)$ and let
$$
 B^2=\frac{d_0^2+\tfrac12\sum_{j=1}^{128}d_j^2}{(2\pi^2)^2}.
$$
The mean square of $F$ on each interval of length 128 is $B^2$. For the two-place sum, $x^2g(x)=\sum_{j\ge0}4^{-j}F(2^jx)$ and its root mean square on each such interval is at most $4B/3$ by the triangle inequality. The weight factor satisfies
$$
 x^{-4}w_D(x)\le R^{-4}w_D(R)(x/R)^{-3+\beta},
 \qquad \beta=1/4,
$$
because the logarithmic derivative of $1+t^2$ in $t=\log(x/4)$ is at most one. Summing the interval maxima of the displayed majorant gives the far norm cap using the factor $128+R/(2-\beta)$. The pairing has support inside the radial core.

The calculation encloses the finite core integrals with Arb. The upper and lower expression fields in the report describe one-sided bounds on the stated norms.

## Replay

~~~powershell
uv run --no-project --python 3.14 --with python-flint==0.9.0 python tools/s_local_primal.py --trials-from docs/masullo/s-local-primal-106.json --report primal-replay.json
~~~

The trial numerators are in the report. To regenerate candidate coefficients with the Galerkin solver, add `--with numpy==2.5.5` to the `uv run` command and omit `--trials-from`. Replay the saved trial numerators when comparing the certificate for the same trial across environments.

The saved Windows run used 106-bit Arb and radial endpoints $2^{-28}$ and $256$. The scalar error assembly was recomputed from the saved component balls at 192-bit precision. Twenty-one point values of the cosine transform were compared with the original affine-piece implementation in floating-point arithmetic. The 160-bit integration run was stopped before completion.

[Certificate driver](../../tools/s_local_primal.py) · [106-bit report](s-local-primal-106.json)
