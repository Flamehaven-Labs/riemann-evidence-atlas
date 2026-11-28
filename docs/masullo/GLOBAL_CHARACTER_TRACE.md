# Spectral Trace over All Character Components

## Manuscript statements under review

The pinned manuscript is the 2026-11-20 PDF with SHA-256 `e039d3f6cf0a4b14f03c7edb85097752dd65c0a2fe543c76fe992be234f97bf5`. Page 63 defines Bruhat smoothness through compact-subgroup invariance and smoothness on Lie quotients. Page 419 takes $\varphi\in D(C_F)$ to be a smooth compactly supported test function and defines its translation average in (9.3.1.2). Theorem 10.3.2.1(2), pp. 453–454, gives a diagonal sum over characters and zeros. Part (1) also claims convergence of specific finite biorthogonal sums. The argument below uses block direct sums and orthogonal compression. [Pinned manuscript, p. 63](https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf#page=63) · [p. 419](https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf#page=419) · [pp. 453–454](https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf#page=453)

## Characters selected by the test function

Let $K=C_F^1$ and use the normalized positive real section $\tau$ to write $C_F\simeq\mathbb R\times K$. Let $t=\log|\cdot|_F$ and $h\in K$. Extend each $\omega\in\widehat K$ to a unitary character $\chi_\omega$ trivial on $\tau$. Absorb the Haar constant into $d\mu_K$. With the positive Mellin sign on the dual modes,

$$
 k_\omega(t)=\int_K\varphi(\tau(e^t)h)\omega(h)\,d\mu_K(h),
 \qquad
 M_{k_\omega}(z)=\int_{C_F}\varphi(g)\chi_\omega(g)|g|_F^z\,d\mu(g).
$$

If $\varphi$ is invariant under a compact subgroup $K_0$, then $K_0\subset K$ because its image under the logarithm of the norm is a compact subgroup of $\mathbb R$. Haar substitution by $u\in K_0$ gives $k_\omega(t)=\omega(u)k_\omega(t)$. Thus components with $\omega|_{K_0}\ne1$ vanish, leaving the character group $\widehat{K/K_0}$.

- **Over $F=\mathbb Q$**, $K\simeq\widehat{\mathbb Z}^{\times}$ is profinite and its compact abelian Lie quotient $K/K_0$ is finite. For example, a test invariant under units congruent to $1\bmod q$ only retains characters of conductor dividing $q$. The finite set of blocks needs only individual zero counts. Use the zeta count for the trivial character and the Dirichlet $L$-function count for the others. [Zeta zero count](https://arxiv.org/abs/2107.06506) · [Dirichlet zero counts](https://arxiv.org/abs/2005.02989)
- **Over a general fixed number field**, $K/K_0\simeq\mathbb T^d\times A$ with $A$ finite abelian, so the remaining characters are indexed by $(m,\nu)\in\mathbb Z^d\times\widehat A$. Invariance under units at almost all finite places, as used on p. 520, does not force $d=0$. [Pinned manuscript, p. 520](https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf#page=520)

## Fourier decay on the torus and zero counts

A single compact radial interval $J$ containing the support of the test function contains the supports of every $k_\omega$ and its derivatives. Integrating by parts with $(1-\Delta)^N$ for the torus Laplacian gives uniform bounds for $j=0,1,2$.

$$
\sup_{t\in J}|k_{m,\nu}^{(j)}(t)|
 \le C_{\varphi,N}(1+\|m\|^2)^{-N}.
$$

Fix $\alpha$ and choose $b>\alpha+1/2$ with $b\ge\alpha+1$. The common bound $\|U_t\|\le e^{(\alpha+1/2)|t|}$ on all radial blocks gives $\|D_{k_\omega}\|\ll_{\varphi,N,\alpha,b}(1+\|m\|^2)^{-N}$ for $D_{k_\omega}=T_{b^2k_\omega+2bk'_\omega+k''_\omega}$. The fixed-character energy estimate and the Schatten inequality give

$$
\|T_\omega\|_1
 \le \|D_{k_\omega}\|\|R_{b,\omega}\|_2^2,\qquad
\|R_{b,\omega}\|_2^2
 \le \frac{b+\alpha}{b-\alpha-1/2}
       \sum_{\rho}\frac{n_I(\rho)}{1+(\Im\rho)^2}
$$

where $n_I$ denotes the retained multiplicity in the radial model. We work on strips with $0<\alpha<1/2$. [Fixed-character trace](FIXED_CHARACTER_TRACE.md) · [Hilbert–Schmidt estimate](RESOLVENT_HILBERT_SCHMIDT.md)

The conductors are uniformly bounded on this quotient. The group of finite idelic units is profinite, and the compact Lie group $K/K_0$ has no sufficiently small nontrivial subgroups. The kernel of the map from the unit group to the quotient thus contains an open congruence subgroup. In the archimedean logarithmic and angular directions, differentiation of a torus character through a fixed group homomorphism bounds the gamma shifts by $O_{F,K_0}(1+\|m\|)$. The finite component $\nu$ has finitely many values. [Brumley–Lesesvre–Milićević on archimedean characters and conductors](https://arxiv.org/abs/2105.02068)

For the zero count, use the functional equation of the completed Hecke $L$-function, its order-one Hadamard product, and the Euler product in the right half-plane. For the trivial character with poles, multiply by $s(s-1)$ to obtain an entire function. Write $\rho$ for the zeros of the resulting entire function.

$$
\sum_\rho \Re(2+iT-\rho)^{-1}
=\Re\frac{\Xi_\omega'}{\Xi_\omega}(2+iT).
$$

Logarithmically differentiate the Hadamard product and subtract the real-part formula at a nonzero point of the function on the critical line. The constant cancels. Symmetry from the functional equation makes the real-part zero sum at that point zero. Both real-part series converge absolutely because zero real parts are bounded and the order-one product gives $\sum_{|\rho|\ge1}|\rho|^{-2}<\infty$. A nontrivial zero with $|\Im\rho-T|\le1$ contributes at least $1/5$ to the left side. On $\Re s=2$, the absolute Euler coefficients of $\zeta_F$ bound the finite logarithmic derivative. In a fixed positive real half-plane the gamma logarithmic derivative is $O(\log(2+|T|+\|m\|))$, and the conductor and pole terms satisfy the same bound. Counting with multiplicity gives

$$
N_\omega([T-1,T+1])\ll_{F,K_0}\log(3+|T|+\|m\|),
\qquad
\sum_\rho \frac{n_I(\rho)}{1+(\Im\rho)^2}
 \ll_{F,K_0} 1+\log(2+\|m\|).
$$

This argument applies directly to the archimedean parameters of the character. The Hadamard and gamma estimates are the analytic inputs in the derivation. [Coleman on gamma terms and the Hadamard expansion for Hecke characters of infinite order](https://matwbn.icm.edu.pl/ksiazki/aa/aa85/aa8537.pdf)

## Direct sum and truncation

The shell $2^j\le1+\|m\|<2^{j+1}$ contains $O(2^{dj})$ characters. Each block satisfies $\|T_\omega\|_1\ll (1+j)2^{-2Nj}$, so the shell total is $O((1+j)2^{-(2N-d)j})$. It suffices that $2N>d$. To use Lean's geometric comparison directly, apply $1+j\le2^j$ and take $2N>d+1$. In particular, if $2N\ge d+2$, the trace norm tail starting at $J_0$ is $O(2^{-J_0})$. The implied constant depends on the test function and number field among the fixed inputs. It is left unquantified here.

Therefore $T=\bigoplus_\omega T_\omega$ on $E=\bigoplus_\omega E_\omega$ is trace-class in this radial model. The trace norm of a finite direct sum equals the sum of its block norms. For the orthogonal projection $P_{<J_0}$ onto the preceding shells, $\|T-P_{<J_0}TP_{<J_0}\|_1$ equals the trace norm tail. In each block, the sum of absolute orthonormal diagonal entries is bounded by $\|T_\omega\|_1$, so the double sum converges absolutely.

$$
\operatorname{Tr}_E T=\sum_\omega\sum_\rho
 n_I(\rho)\,M_{k_\omega}(\rho-\tfrac12).
$$

Cancellation of signed block traces cannot control this norm. For example, the blocks $\operatorname{diag}(1/n,-1/n)$ for $n\ge1$ each have trace zero and yield the divergent trace norm sum $2\sum_n 1/n$.

The conclusion uses the earlier radial generator and basis assumptions at center $a=1/2$. Identification with the idelic quotient requires the manuscript's density input. The open-strip sum restricts the space to interior zero modes. The closed-strip formula in Theorem 10.3.2.1(2) includes truncated multiplicities at the edges. Identifying the open strip of Theorem 12.5.1.1 with the all-zero explicit formula requires a separate treatment of exterior and edge zeros. The biorthogonal partial sums and the trace of the geometric truncation are further proof obligations. [Idelic quotient and zero modes](ADELIC_QUOTIENT.md) · [Open strip and geometric trace problem](https://github.com/mccorvie/riemann-masullo/issues/5571)

Starting from the all-zero explicit formula with the same Haar normalization and pole terms, the additional identity needed for the open-strip formula is $\sum_{\omega,\rho:\ |\Re\rho-1/2|\ge\alpha} n(\rho)M_{k_\omega}(\rho-1/2)=0$. The convergence estimate above makes this sum well-defined. Vanishing requires a separate argument.

## Lean verification scope

The three declarations establish coefficient cancellation under Haar invariance, the geometric shell comparison, and absolute summability of the double diagonal. Torus differentiation, Hecke zero counts, and the Schatten direct-sum argument are analytic.

On 2026-11-25, Colab Linux replayed the three declarations with Lean 4.33.1 and Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`. The run exited 0 with zero bytes on stderr. Each axiom record lists `propext`, `Classical.choice`, and `Quot.sound`. The inputs were an archive of `0cb5cd9b872c72328cfbddbb3ddf5e9427d300ff` and an overlay of the new source, verifier, and shared helper.

| File | SHA-256 |
| --- | --- |
| Lean source | `f3165d056b16885236a5a7c1c475f1db8963be452f0a641f4f2b1d21b8750e40` |
| Colab input ZIP | `acdc3bd11ddb9d9b41ada8a9a2b7a663ff3a0176449a0da4a741c5581920fbe6` |
| Colab receipt | `2fc93408827cd87484b3054723b86c91cef1c48d6759cb9272cdeadf86b4e5d6` |
| Windows receipt | `462e3f9a0627ab5251ad6b995782888cd7e15060f02fead1c99f68a515f455dc` |

Initial Windows attempts stopped while loading Lean and Lake module files. After checking the package revisions and working trees against the lock, the replay set `LEAN_PATH` to the package build directories and compiled the same source directly with `lean -j 1`. The run exited 0 with empty stderr. Windows and Colab receipts match apart from the host string in the Lean version banner. A new GitHub CI run is pending.

~~~sh
python -E -S tools/verify_global_character_trace.py \
  --lean "$(cd formal/landau && elan which lean)" --mathlib-project formal/landau \
  --expect docs/masullo/global-character-trace-colab-replay.json
~~~

[Lean source](../../tests/lean/E2AGlobalCharacterTrace.lean) · [Verifier](../../tools/verify_global_character_trace.py) · [Colab receipt](global-character-trace-colab-replay.json) · [Windows receipt](global-character-trace-windows-replay.json)
