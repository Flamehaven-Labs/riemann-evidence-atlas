# P2 — Characters and Levels at the Prime 2

**Disposition** — Rational calculation and replay GREEN. Correspondence with the manuscript's trace formula HELD.

## Pinned inputs and results

For $p=2$ and $s=2$, set $x=\chi(2)/4$. Then $L_2(s)=(1-\chi(2)2^{-s})^{-1}$ and $d_2(s)=-L_2'(s)/(L_2(s)\log 2)$. The calculator evaluates $L_2(2)=1/(1-x)$ and $d_2(2)=x/(1-x)$ in exact rational arithmetic. It also checks $d_2(2)=\sum_{j=1}^{8}x^j+x^9/(1-x)$ for each character.

| Character | Modulus | Conductor | $\chi(2)$ at the stated level | $(L_2,d_2)$ at level | $(L_2,d_2)$ at conductor |
| --- | ---: | ---: | ---: | --- | --- |
| Trivial character | 1 | 1 | $1$ | $(4/3,1/3)$ | $(4/3,1/3)$ |
| Quadratic character modulo 3 | 3 | 3 | $-1$ | $(4/5,-1/5)$ | $(4/5,-1/5)$ |
| Primitive character modulo 4 | 4 | 4 | $0$ | $(1,0)$ | $(1,0)$ |
| Principal character modulo 4 | 4 | 1 | $0$ | $(1,0)$ | $(4/3,1/3)$ |

The principal character modulo 4 has conductor 1. Raising the level here multiplies the primitive local factor by $1-2^{-s}$. At $s=2$, this factor is $3/4$ and contributes $-1/3$ to the normalized logarithmic derivative. Thus $L_2=(3/4)(4/3)=1$ and $d_2=1/3-1/3=0$. The primitive character modulo 4 is already ramified at 2 at its conductor and starts with $(1,0)$.

~~~sh
python -E -S tools/prime_two_local_surface.py --characters --verify-report docs/masullo/P2_CHARACTER_COMPARISON.json
~~~

The verifier recomputes the record at the pinned levels and conductors. It rejects a reversed quadratic sign, an added factor at a ramified prime, and substitution of the modulus for the conductor. Baseline replay checks the digests of the historical trivial-character report and the four-character report separately. [Results JSON](P2_CHARACTER_COMPARISON.json) · [Regression tests](../../tests/test_prime_two_local_surface.py)

## Correspondence with the primary sources

**Alpöge Lean source.** In the pinned archive, lines 7–21 of `Development/AutomorphicArithmetic/CharacterBoxes/ClaimStrip.lean` show in `Claim.factor_ne_zero` that $1-\psi(p)p^{-s}$ is nonzero for $\Re s>0$. Lines 23–32 of `Claim.prim_zero` use `DirichletCharacter.LFunction_changeLevel` to relate $\chi$ to its primitive inducing character and use the finite-factor result to exclude zeros introduced by the level. The $s=2$ calculation is an arithmetic example for the finite factor. Zero transfer in `prim_zero` separately assumes $0<\Re s<1$. The pinned Mathlib declaration identifies the induced $L$-function as the primitive $L$-function multiplied by the finite factors over primes dividing the level. For a trivial primitive character it requires $s\ne1$, which the fixed $s=2$ satisfies. [Archived source digests](../../lean-extract-manifest.json) · [Pinned Mathlib declaration](https://github.com/leanprover-community/mathlib4/blob/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/NumberTheory/LSeries/DirichletContinuation.lean#L150)

**Masullo manuscript.** In Theorem 12.5.1.1, equation (12.5.1.2) on p. 519, the prime-2 term over $\mathbb Q$ is a principal-value integral multiplied by $\log 2/\mu_2(\mathbb Z_2^\times)$. Its integrand is $\varphi(g_2)|g_2|_2^{1/2}/|1-g_2|_2$. For $g_2=2^m u$ with $m\ne0$, we have $|1-2^mu|_2=\max(1,2^{-m})$, so the weight on $\varphi$ is $2^{-|m|/2}$. Applying cancellation of a ramified character on this shell requires checking whether the remaining test function separates from the unit variable. For $m=0$, every unit satisfies $|1-u|_2\le1/2$ and the denominator depends on $u$. The hypothesis $\varphi(C_{\mathbb Q}^{1})=0$ includes the image of norm-one units. Relating it to the level-change factor requires choosing the test function and applying the local integration definition together. [Pinned manuscript, p. 519](https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf#page=519)

The local principal value is checked. The cross-source correspondence remains held. Using the definition on p. 622, the unit-shell calculation distinguishes an indicator function from a ramified character. [Unit-shell calculation](P2_UNIT_SHELL.md)

The footnote on p. 514 calls for revising the cutoff and checking convergence in (12.4.1.23). The argument on p. 520 requires $S$ to contain the places where the character ramifies and assumes unit-translation invariance outside $S$. Hence a character ramified at 2 requires $2\in S$. The argument also invokes Theorem 12.4.1.1. An equality between the two sources requires an explicit $\varphi$, compatible Mellin normalizations for the positive and negative shells, and justification of the cutoff limit. The missing final theorem statement on p. 522 is recorded separately. [Manuscript version and locations](README.md)
