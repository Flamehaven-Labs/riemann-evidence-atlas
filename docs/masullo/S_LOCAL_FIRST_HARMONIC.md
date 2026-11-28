# First Fourier Pair of the Lower-Gate Trace

Use the same sharp lower gate, period two, outgoing strips, and input intervals as in the constant-term calculation. Here $L=4$, $\alpha=1/8$, and $P_N$ is the exact 128-cell projection in the unpolarized space. Set $E=P-P_N$. [Constant term and normalization](S_LOCAL_CONSTANT_TERM.md)

## Coefficient enclosure

For the G1 bump centered at $\ell=\log2$ and $k=h''-h/4$, integration by parts gives
$$
 c_1=-e^{-i\pi\ell}\left(\pi^2+\tfrac14\right)
         \int_0^{1/4}h(\ell+s)\cos(\pi s)\,ds .
$$
The period-two coefficient of $h$ uses the factor $1/2$, which cancels the factor of two from the even translated bump. The product in the integral is nonnegative and nonincreasing on $[0,1/4]$, so left and right rectangle sums give certified endpoints. The support also gives $|c_1|/|c_0|\ge(4\pi^2+1)/\sqrt2$. The 160-bit run gives
$$
 2.02129<|c_1|<2.02253,\qquad
 37.38962 < |c_1|/|c_0| < 37.43362.
$$

## Residual bounds for the modulated rows

The constant outgoing and incoming data now carry the phase $e^{i\pi\log(x/4)}$. The phase has unit modulus. The outgoing full norm is therefore unchanged. Its weighted exterior-projection reduction can be computed from the same 16-packet Gram enclosure by solving separately for the real and imaginary components of the complex pairing.

For the incoming row the flat gate $K_q=FM_qF$ is an orthogonal projection. Let $H=\mathbf1_{J_x}x^{-1/2}e^{i\pi\log(x/4)}$ and $v=K_q^{*w}(H/w)$. To improve the bound $\|v\|_w^2\le S\|H\|_2^2$, remove flat energy detected by five disjoint box-frequency packets outside the gate. Their flat squared norms are their interval lengths. For a packet $Z$ supported in $[\xi_0,\xi_1]$, write $f=CZ$. At the two places,
$$
 FZ(x)=\tfrac12\left(\sum_{j\ge0}f(2^jx)-f(x/2)\right),\qquad
 f(x)=\frac{\sin(2\pi \xi_1x)-\sin(2\pi \xi_0x)}{\pi x}.
$$
At the real place $FZ=f$. For the two-place pairing over $J_x=[a,b]$, the omitted sum after index $m$ is bounded using $|f(y)|\le 2/(\pi y)$. Integration by parts against $x^{-3/2+i\pi}$ gives a second bound. With
$$
 A=a^{-3/2}+b^{-3/2}+\tfrac23|-\tfrac32+i\pi|(a^{-3/2}-b^{-3/2}),
$$
the second tail bound is $A(\xi_0^{-1}+\xi_1^{-1})4^{-m}/(12\pi^2)$. The driver keeps indices $0$ through $4$ and uses the smaller certified cap. A lower bound on each pairing modulus gives a lower bound on the energy removed from the flat complement. The squared norm of $H$ is $\log4+1/2$.

Both residual estimates also subtract a finite-projection lower bound. Use the constant-term triangular trial with bandwidth $1/16$ and its saved weighted norm cap. The incoming pairing uses $K_qg=g$. The outgoing pairing uses the weight $w$. Arb encloses the complex finite pairings, and the inverse-square triangle profiles bound the omitted dyadic terms. Each finite-projection gain is bounded below by the square of a certified lower modulus divided by the trial norm cap.

## Budget result

The two Fourier terms are complex conjugates because the cutoff and projections preserve real functions. With inner products linear in the first argument, the signed error on each strip is $2\operatorname{Re}(c_1\langle Ea_1,Ev_1\rangle_w)$. The tested bound for its absolute value is $2|c_1|\sqrt{\eta_{\rm out}\eta_{\rm in}}$.

| Strip | Places | Outgoing residual squared norm upper bound | Incoming residual squared norm upper bound | Pair error upper bound |
| --- | --- | ---: | ---: | ---: |
| $[1/4,1]$ | $\{\infty\}$ | 1.87879 | 4.92481 | 12.30432 |
| $[1/4,1]$ | $\{\infty,2\}$ | 1.94502 | 6.44760 | 14.32466 |
| $[16,64]$ | $\{\infty\}$ | 3.20287 | 7.57870 | 19.92926 |
| $[16,64]$ | $\{\infty,2\}$ | 3.20394 | 6.65590 | 18.67969 |

The upper bound obtained by summing the stored expressions is **65.23790**, compared with the remaining scale of **0.7551450173** after the constant term. The certified enclosure of the computed upper-bound expression lies wholly above the budget. With the current coefficient cap, a norm-product argument would require the sum of the four residual norm products to be below about 0.18668 even if this pair used the entire remaining allowance. The current residual estimates with norm products therefore fail to certify this pair within the budget. The bound leaves the actual signed error undetermined. An admissible estimate for this pair still leaves the later harmonics, Fourier tail, and finite-matrix error to control.

**ACCEPT** for the coefficient enclosure and the residual bounds. **REJECT** the use of their current norm-product sum as an in-budget certificate. **AMBER** for the signed infinite-dimensional error and the full trace ordering.

## Signed changes in nested finite spaces

A separate floating-point calculation evaluates $2\operatorname{Re}(c_1 B^*G^{-1}A)$ for the complex row pairings $A,B$ with the real Galerkin basis. The 128-cell rows and Gram matrix are obtained by restricting the same 256-cell arrays with the prolongation map. Both settings use the same periods and strips as the certificate.

| Quadrature setting | Signed change in schedule difference, 128 to 256 cells | Sum of absolute changes across the four rows |
| --- | ---: | ---: |
| Base | +0.038461 | 0.156829 |
| Refined | +0.041547 | 0.154981 |

The change in the two-place origin row was about $-0.002566$ in the base setting and $+0.000519$ in the refined setting. The combined change stayed positive in both settings, and the outer rows contributed most of the absolute change. These are finite-space diagnostics. The quadrature error and the contribution beyond 256 cells are open.

For a signed certification route let $\omega=\overline{c_1}/|c_1|$. Then on each strip
$$
 2\operatorname{Re}(c_1\langle Ea_1,Ev_1\rangle_w)
 =\frac{|c_1|}{2}
  \bigl(\|E(a_1+\omega v_1)\|_w^2-\|E(a_1-\omega v_1)\|_w^2\bigr).
$$
This formulation identifies the two mixed residuals whose squared norms need two-sided bounds. The finite diagnostic provides the corresponding signed comparison inside the two computed spaces.

## Windows and Colab verification

The pinned 160-bit Arb run was repeated on Windows and on Colab Linux using python-flint 0.9.0. The report was byte-identical in the two replays and the reference, with SHA-256 `17e012ea858da50f3d930e0b54a9724e87254f523d8e2dbac6e98d43a0b95c81`. The four row bounds and the budget result `BOUND_EXCEEDS_BUDGET` were identical. The Colab receipt was reconstructed from its printed JSON and matched the receipt hash printed by the runtime. [Arb replay receipt](s-local-first-harmonic-colab-arb-replay.json)

The signed 128-to-256-cell diagnostic also replayed on Colab with NumPy 2.5.5. Compared with the saved Windows runs, the maximum absolute differences in the individual row changes were $1.56\times10^{-15}$ for the base setting and $8.22\times10^{-15}$ for the refined setting. All four row signs agreed across platforms at each setting. The sign difference between the two settings for the two-place origin row also reproduced. The receipt was reconstructed and checked against the hash printed by Colab. [Nested replay receipt](s-local-first-harmonic-colab-nested-replay.json)

Lean 4.33.1 and the pinned Mathlib revision checked the following five declarations on Windows and Colab Linux. The proof source and normalized axiom output were byte-identical across both runs, with axioms `propext`, `Classical.choice`, and `Quot.sound`. [Lean proof](../../tests/lean/E2AFirstHarmonicAudit.lean) · [Windows receipt](s-local-first-harmonic-windows-lean-replay.json) · [Colab receipt](s-local-first-harmonic-colab-lean-replay.json)

| Declaration | Checked statement |
| --- | --- |
| `signed_polarization` | The conjugate phase and sign in the mixed norm identity |
| `nested_residual_lower` | The squared residual at the intermediate space is a lower bound for the full squared residual |
| `signed_interval` | Subtraction reverses the endpoints of the second interval |
| `first_pair_misses_budget` | A computed expression greater than 65.23789 exceeds 86 times the rational budget |
| `constant_rounding_budget` | The rounded row sum and the remaining rational budget |

Arb supplies the numerical premise of the budget theorem. The Lean check gives the projection and arithmetic steps needed for the mixed-residual approach. A sharp enclosure of the actual signed infinite-dimensional error remains open. [Colab replay notebook](https://colab.research.google.com/drive/18rCY_2FrYEFlEbPlSJ8kw2CjR51PfHCP)

## Replay

~~~powershell
uv run --no-project --python 3.14 --with python-flint==0.9.0 python tools/s_local_first_harmonic.py --report first-harmonic-106.json
uv run --no-project --python 3.14 --with python-flint==0.9.0 python tools/s_local_first_harmonic.py --precision 160 --subdivisions 2048 --report first-harmonic-160.json
uv run --no-project --python 3.14 --with numpy==2.5.5 python tools/s_local_first_harmonic_nested.py --report first-harmonic-nested-base.json
uv run --no-project --python 3.14 --with numpy==2.5.5 python tools/s_local_first_harmonic_nested.py --refined --report first-harmonic-nested-refined.json
~~~

The two runs use the same variant of the Arb method with 1024 and 2048 coefficient rectangles and 106 and 160 bits of working precision. They bind the outgoing Gram and incoming trial certificates and the G1 source by SHA-256. The recorded norm-product arithmetic was recombined at 192 bits.

[Certificate driver](../../tools/s_local_first_harmonic.py) · [106-bit report](s-local-first-harmonic-106.json) · [160-bit report](s-local-first-harmonic-160.json) · [Nested diagnostic driver](../../tools/s_local_first_harmonic_nested.py) · [Base diagnostic](s-local-first-harmonic-nested-base.json) · [Refined diagnostic](s-local-first-harmonic-nested-refined.json)
