# The Principal Value on the Unit Shell at the Prime 2

## Conditions in the source

Equation (12.5.1.2) on p. 519 of the pinned Masullo manuscript uses local principal values at finite places. Lemma B.4.4.5 on p. 622 integrates $f(u)-f(1)$ within the unit group. As noted on p. 623, local constancy of $f$ makes the difference zero near 1. The local different for $F_v=\mathbb Q_2$ is trivial. [Manuscript and SHA-256](README.md)

Normalize the multiplicative Haar measure on $U=\mathbb Z_2^\times$ by $\nu(U)=1$. On the unit shell, $|u|_2^{1/2}=1$, so its principal-value contribution divided by $\log 2$ is

$$
\int_U \frac{f(u)-f(1)}{|1-u|_2}\,d\nu(u).
$$

Theorem 12.5.1.1 assumes $\varphi|_{C_F^1}=0$. Since local units map to norm-one idele classes, the manuscript's test function vanishes everywhere on $U$ under this hypothesis, making the unit term zero. The local condition $f(1)=0$ alone eliminates the subtraction and can leave a nonzero contribution. For $f=\mathbf 1_{3+4\mathbb Z_2}$ the value is $\log 2$, since the coset has Haar mass $1/2$ and the inverse norm is 2.

## Conductor exponent for a ramified character

For a local comparison, take $f=\mathbf 1_U\chi$ with $\chi$ a nontrivial continuous character of $U$. Let $a$ be the smallest index for which $\chi$ is trivial on $U_a=1+2^a\mathbb Z_2$. Then $f(1)=1$.

For each $r\ge1$, the units with $v_2(1-u)=r$ form $U_r\setminus U_{r+1}$. Since $\nu(U_r)=2^{1-r}$, the shell mass $2^{-r}$ times the weight $2^r$ is 1. Haar invariance makes the integral of a nontrivial restriction of $\chi$ to $U_r$ vanish. A trivial restriction integrates to $\nu(U_r)$.

| Shell | Integral of $\chi(u)-1$ multiplied by $2^r$ |
| --- | ---: |
| $1\le r<a-1$ | $-1$ |
| $r=a-1$ | $-2$ |
| $r\ge a$ | $0$ |

In the second row, the character integral is zero on $U_{a-1}$ and is $2^{1-a}$ on $U_a$. The character integral on their difference is therefore minus the shell mass. Summing gives the unit contribution **$-a\log 2$**. For the primitive character modulo 4, $a=2$ gives $-\log 4$.

## Exact sums and Euler-factor comparison

| Local test | Unit contribution divided by $\log 2$ |
| --- | ---: |
| Trivial character on the units | $0$ |
| Primitive character modulo 4 | $-2$ |
| Primitive character modulo 8, $\chi(1),\chi(3),\chi(5),\chi(7)=(1,-1,-1,1)$ | $-3$ |
| $\mathbf 1_{3+4\mathbb Z_2}$ | $1$ |

The exact sum assigns equal mass to odd classes modulo $2^N$ and omits the class of 1. The results hold for $N=3,\ldots,10$. For the primitive character modulo 4, the unweighted unit average is zero, while the weighted sum without subtracting $f(1)$ was $N-3$ because the weight varies across units. [Rational comparison code](../../tools/prime_two_unit_shell.py)

~~~sh
python -E -S tools/prime_two_unit_shell.py
~~~

On 2026-11-24, Python 3.13.18 on Colab Linux replayed five local inputs across eight truncation depths. The four inputs above and a zero-function control for vanishing on norm-one classes matched the Windows baseline. The output SHA-256 is `86d486239a64eec975e9dd2d41f866f1e377b51630de8c0332138488768b1c1c`. [Replay inputs and scope](../ROADMAP.md#replay-at-phase-transitions)

At the stated level in Alpöge's calculation, both the primitive and principal characters modulo 4 have $L_2(s)=1$. Restricted to the units, the primitive character is nontrivial with conductor exponent 2, while the principal character is trivial. The local controls give $-\log4$ and 0, respectively. Comparing the full expression (12.5.1.2) with an Euler factor requires the manuscript's global test conditions, non-unit shells, and Mellin normalization. [Level and conductor comparison](P2_CHARACTER_COMPARISON.md)
