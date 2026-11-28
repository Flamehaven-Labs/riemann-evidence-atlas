# The Cosine Factor in the RH Reflection Step

## Original proof

`Formalism.VW.rh_of_right` assumes $\zeta(z)\ne0$ whenever $\operatorname{Re}z>1/2$ and $z\ne1$. If a zero $s$ on the left survives the exclusions for trivial zeros and poles, then $t=1-s$ is on the right. The original proof applies Mathlib's functional equation at $t$.

$$
\zeta(s)=2(2\pi)^{-t}\,\Gamma(t)\,\cos(\pi t/2)\,\zeta(t).
$$

The last factor on the right is nonzero by the initial hypothesis. The gamma factor is nonzero because $t$ has positive real part. After checking the complex powers of nonzero bases, the remaining step is to show that the cosine factor is nonzero. The original proof shows why $s=0$ and the trivial zeros need separate treatment.

In the original `RhOfRight.lean`, line 5 gives the theorem, line 28 applies the functional equation, lines 34–59 handle the cosine, and line 60 multiplies the factors to reach a contradiction. The file was extracted from `lean/src/Formalism/GammaFactorNonvanishing/RhOfRight.lean` in the release archive. Its SHA-256 is `7e2c0b519ee420192cad8fb281c2d2bfebae2ba553342fd579c81c2aa0bd3dc5`. [Archive pins](evidence/source-index/lean-archive-manifest.json) · [Original declaration references](rh-next-layer-module-set.json)

## Exact scope of the auxiliary lemma

Mathlib's `Complex.cos_eq_zero_iff` gives the complex cosine zeros $(2k+1)\pi/2$ for integral $k$. Substituting $\pi(1-s)/2$ and canceling $\pi\ne0$ gives

$$
\cos\bigl(\pi(1-s)/2\bigr)=0
\quad\Longleftrightarrow\quad s=-2k\quad(k\in\mathbb Z).
$$

Thus $\operatorname{Re}s<2$ implies $k\ge0$. If $k=0$, then $s=0$. If $k>0$, $s$ is a negative even integer. The original proof excludes the first case using $\zeta(0)=-1/2$ and the others using the nontrivial-zero hypothesis.

For the cosine factor alone the real-part restriction can be relaxed to $\operatorname{Re}s<2$. The cosine vanishes at $s=2$, which is outside the form $-2n$, so the classification excludes the boundary. The full reflection argument still needs $\operatorname{Re}s<1/2$ to apply the initial nonvanishing hypothesis at $\operatorname{Re}(1-s)>1/2$.

## Replay and proof-term inspection

- Reading the original `RhOfRight.olean` with Lean 4.33.1 confirmed `Complex.cos_eq_zero_iff` as a direct proof-term reference of `rh_of_right`. The source uses it to turn the cosine condition into an integer condition.
- Reading only Mathlib's `Complex.olean` exposed the lemma as bodyless `axiomInfo`. Passing `Complex.olean` and `Complex.olean.private` to Lean's `readModuleDataParts` in that order exposed a `thmInfo` with the same type and a proof body. Check which module parts were read before inferring axiom dependencies from a missing body.
- The independent Lean file verifies the exact zero classification, the case $\operatorname{Re}s<2$, cosine nonvanishing in the original branch, and the boundary example $s=2$. The four declarations use `propext`, `Classical.choice`, and `Quot.sound`. [Verified Lean source](../tests/lean/E2ARhReflectionCos.lean)

On 2026-11-24, Colab Linux recompiled the four declarations with pinned Lean 4.33.1 and Mathlib. All four axiom output lines matched the Windows baseline. The Colab output SHA-256 is `a062993d32ef6d25882cb836896d7fb7a90b9a7a90105f23d669fe69407779ad`. The run covered the auxiliary proof file. A kernel recheck of the full original RH proof remains open. [Replay inputs and scope](ROADMAP.md#replay-at-phase-transitions)

Run the Lean source from a Lake working directory with the pinned Mathlib available.

~~~sh
cd formal/landau
lake env lean -j 2 ../../tests/lean/E2ARhReflectionCos.lean
~~~
