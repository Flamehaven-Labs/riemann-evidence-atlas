# Geometric Trace Comparison over the Rationals

## What the manuscript needs

The pinned 2026-11-20 draft uses the normalized S-local cutoff formula of Theorem 12.4.1.1 on p. 514. The proof of Theorem 12.5.1.1 on p. 520 then identifies the global diagonal with the local expression after subtracting two Mellin terms. Section 12.3, where the global-to-local comparison belongs, consists of a heading and an editorial instruction. The same proof also identifies the global diagonal with a negative sum over the interior of an open strip. These are distinct equalities. [Pinned manuscript](README.md) · [Global-to-local comparison](https://github.com/mccorvie/riemann-masullo/issues/7353)

For strip half-width $\alpha$, let $S_\alpha(\varphi)$ denote the interior spectral sum, with multiplicity, and let $P(\varphi)$ be the sum of the two polar Mellin terms in (12.5.1.3). With the manuscript's Haar normalizations, the target equality is $L(\varphi)=P(\varphi)-S_\alpha(\varphi)$, where $L$ denotes its local terms. Comparing with the all-zero explicit formula also requires the vanishing of the sum over zeros satisfying $|\Re\rho-1/2|\ge\alpha$, including the two edges. The all-character radial argument gives convergence under its stated hypotheses. The public discussion documents the strength of the exterior assertion, including a fixed-width equivalence with absence of exterior zeros when cancellation is required for every admissible test. [All-character radial trace](GLOBAL_CHARACTER_TRACE.md) · [Exterior-zero obligation](https://github.com/mccorvie/riemann-masullo/issues/5571) · [Summary of the equivalence and current scope](https://github.com/mccorvie/riemann-masullo/issues/5571#issuecomment-7179988782)

## A test with two vanishing moments and a nonzero prime term

Take $F=\mathbb Q$ and $t=\log|g|_{\mathbb Q}$. Fix

$$
h(t)=\operatorname{smoothTransition}\bigl(2-32(t-\log 2)^2\bigr).
$$

The Mathlib transition is zero on $(-\infty,0]$ and one on $[1,\infty)$. Hence $h$ is supported in $[\log 2-1/4,\log 2+1/4]$ and equals one near $\log 2$. The bounds $\log 2\ge1/2$ and $\log 3-\log 2\ge1/3$ put the support bracket strictly inside $(0,\log 3)$. Define

$$
k(t)=h''(t)-\tfrac14 h(t),\qquad \varphi(g)=k\bigl(\log|g|_{\mathbb Q}\bigr).
$$

The norm-one subgroup is compact. Thus this radial test is compactly supported on $C_\mathbb Q$, smooth on the quotient by the norm-one subgroup, and zero on the norm-one classes. Normalize the Haar measure of the norm-one subgroup to one. Integration by parts twice gives

$$
M_k(z)=\int_{\mathbb R}k(t)e^{zt}\,dt
       = (z^2-\tfrac14)\int_{\mathbb R}h(t)e^{zt}\,dt .
$$

In particular $M_k(1/2)=M_k(-1/2)=0$. For a control, the test with $k=h\ge0$ also vanishes on the norm-one classes and has strictly positive values at both polar Mellin moments.

At each finite place $p$, only non-unit shells can contribute because $\varphi$ vanishes at $t=0$. The log-norm values are $-m\log p$ on $p^m\mathbb Z_p^\times$. The support condition leaves exactly one shell, $2^{-1}\mathbb Z_2^\times$. On this shell $\lvert g\rvert_2=2$ and $\lvert1-g\rvert_2=2$. In (12.5.1.2) the shell's multiplicative Haar mass equals that of $\mathbb Z_2^\times$ and cancels the unit-volume denominator. Since $h''(\log 2)=0$ and $h(\log 2)=1$, the sum of the finite-place terms is exactly

$$
\frac{\log 2}{\sqrt 2}\,k(\log 2)
=-\frac{\log 2}{4\sqrt 2}.
$$

The local expression for $S=\{\infty,2\}$ therefore differs from the archimedean expression by exactly $-\log 2/(4\sqrt 2)$. For the support condition on p. 520, choose $T$ strictly between $\exp(\log 2+1/4)$ and $3$. With $S=\{\infty,2\}$, the prime norms outside $S$ are greater than $T$, and local units act by norm-one classes. The $S=\{\infty\}$ expression serves as a local comparison with the prime term omitted. [Local principal value at 2](P2_UNIT_SHELL.md) · [Equations (12.5.1.1)–(12.5.1.4)](https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf#page=519)

Only the trivial norm-one character survives for this radial test. On $|\Re z|\le 1/2$, two integrations by parts applied to $k$ give $|M_k(z)|\ll_k (1+|\Im z|)^{-2}$. The zeta zero count per unit-height interval is $O(\log(2+|T|))$, so both the interior and omitted sums are absolutely convergent for the test. The value of the omitted sum remains open within the manuscript's argument. [Zero-count input](GLOBAL_CHARACTER_TRACE.md#characters-selected-by-the-test-function)

## Verification status

The manuscript locations were checked by extracting pp. 514 and 519–520 from the local PDF and hashing it against its pinned SHA-256. On 2026-11-26, seven declarations about the fixed test replayed in Lean 4.33.1 on Windows and Colab Linux with Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`. Each run exited 0 with empty stderr. Every declaration uses `propext`, `Classical.choice`, and `Quot.sound`. The receipt fields match apart from the host in the Lean version banner. GitHub CI replay is pending. [Colab notebook](https://colab.research.google.com/drive/136WjjTdAXoTsyX-3q7W21BEuq8SjOClw)

| Lean declaration | Verified statement |
| --- | --- |
| `kernel_smooth_and_supported` | Smoothness and support in the fixed compact bracket |
| `kernel_eq_zero_outside` | Zero values outside $(0,\log 3)$ |
| `kernel_zero_on_other_shells` | Zero at $-m\log p$ for integers $p\ge2$ and $m\in\mathbb Z$ except $(p,m)=(2,-1)$ |
| `kernel_at_log_two` | $k(\log 2)=-1/4$ |
| `kernel_mellin` | The real-axis Mellin multiplier identity |
| `polar_moments_eq_zero` | Both polar moments vanish |
| `prime_two_term` | The shell coefficient $\log 2/\sqrt 2$ times $k(\log 2)$ equals $-\log 2/(4\sqrt 2)$ |

Lean verifies the exact product of the shell coefficient from the manuscript's Haar normalization and the fixed test. The follow-up derives that coefficient from the unfolded Fourier integral and bounds its one-sided cutoff error. The local trace calculation still requires identifying the actual quotient kernel and justifying its diagonal and cutoff limit. The global comparison uses the same test at a fixed $0<\alpha<1/2$. Exterior-zero cancellation remains a separate proof obligation. [Sharp cutoff calculation](S_LOCAL_SHARP_CUTOFF.md) · [S-local kernel and trace obligations](https://github.com/mccorvie/riemann-masullo/issues/7354)

At fixed cutoffs the trivial-angular weighted compression has an integrable trace density, with the descended smooth frequency gate and both orthogonal projection legs. Its joint cutoff limit and identification with the manuscript's Step III regularization remain open. [Weighted S-local quotient](S_LOCAL_WEIGHTED_QUOTIENT.md)

### Replay

Use the Lean toolchain and dependency lock in `formal/landau`. With its pinned Mathlib artifacts restored for the imports in the proof, run from that directory.

~~~sh
lake env lean --root=../.. -j 1 ../../tests/lean/E2AGeometricTraceTest.lean
~~~

The Windows run checked the pinned package revisions and used their build directories via `LEAN_PATH`. Missing Mathlib imports were built from the pinned sources. The Colab notebook embedded the same proof bytes and dependency lock, pinned all Lake package revisions, and compared all seven axiom lines. The local Colab receipt was reconstructed and checked byte-for-byte by matching the SHA-256 printed by the running notebook.

| Artifact | SHA-256 |
| --- | --- |
| Windows receipt | `73e0594a988f3e0cdbbdc9fd7bb9382f77dc7baaeccff77114650a498c43b1a0` |
| Colab receipt | `6a9a4207351a3e1385163e70aa158a432ba8ec80c981015873655c4b59d83a62` |
| Colab input notebook | `e94322a0b7d0b31d8822fbbc2e88205c41f3d17e698f399d12d1dd7f268d8096` |

[Lean source](../../tests/lean/E2AGeometricTraceTest.lean) · [Windows replay receipt](geometric-trace-test-windows-replay.json) · [Colab replay receipt](geometric-trace-test-colab-replay.json)
