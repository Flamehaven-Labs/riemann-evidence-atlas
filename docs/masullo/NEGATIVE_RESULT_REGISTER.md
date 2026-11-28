# Negative Results for the S-Local Trace Comparison

## NR-01 — Two-sided unfolded limits depend on the cutoff schedule

Recorded on 2026-11-26 for the fixed G1 radial test over $\mathbb Q$, with the difference between $S=\{\infty,2\}$ and $S=\{\infty\}$. All values concern the unfolded Fourier integrals derived from (12.4.1.22)–(12.4.1.24).

| Calculation | Limit |
| --- | --- |
| One-sided masks with product tending to infinity | $C=-\log 2/(4\sqrt 2)$ |
| Two-sided bands with upper cutoffs $(L^2,L)$ | $0$, for both the sharp bands and the specified symmetric smoothing |
| Two-sided bands with upper cutoffs $(L,L)$ | $C-2d(1)\in(2.68,13.14)$, for both the sharp bands and the specified symmetric smoothing |

The first two rows follow from the analytic Fourier estimates. Lean checks the limit implications from those estimates. The last row combines the finite-ratio formula with a ball-arithmetic enclosure for $d(1)$, including explicit tails. These results reject schedule independence for the unfolded two-sided expression and recovery of the one-sided value on the quadratic band schedule. [One-sided limit](S_LOCAL_SHARP_CUTOFF.md) · [Two-sided limits](S_LOCAL_BAND_LIMITS.md) · [Balanced enclosure](S_LOCAL_EQUAL_RATIO.md)

If the weighted compression's normalized trace difference tends to $C$ on both schedules, its difference from the unfolded integral has different nonzero limits on the two schedules. For the trivial angular type, the fixed-cutoff weighted compression now has an integrable trace density for both smooth bands. The simultaneous limits of these densities and their comparison with the manuscript's Step III diagonal remain open. [Weighted quotient calculation](S_LOCAL_WEIGHTED_QUOTIENT.md) · [Quotient comparison obligation](https://github.com/mccorvie/riemann-masullo/issues/7354)

The unfolded schedule comparison uses a lower frequency cutoff in addition to the upper cutoff in the printed Step II. The upper and removed lower contributions now have separate formulas. [Upper and lower trace terms](S_LOCAL_TRACE_SPLIT.md)

## NR-02 — The product-norm frequency mask can leave Schwartz–Bruhat space

For $S=\{\infty,2\}$, take $f=a\otimes\mathbf1_{\mathbb Z_2^\times}$, with $a$ an even, nonzero real smooth bump supported away from zero. Its finite Fourier factor is $1/2$ on $\mathbb Z_2$. For every proposed common dyadic depth $N$, there is a real frequency $x=2^Nr$ with $\widehat a(x)\ne0$ and with $q(r)\ne q(0)$. This holds for the upper masks and symmetric bands described in the weighted construction. The values of the masked Fourier transform at $(x,0)$ and $(x,2^N)$ differ. A Schwartz–Bruhat function has a common finite dyadic depth of local constancy in the finite coordinate, uniform over the real coordinate. Thus the masked transform falls outside that space, even for the displayed input from $\mathcal S_{00}$.

The tensor and Fourier arguments supply the analytic counterexample. Two Lean declarations certify the dyadic norm and witness argument in Windows and Colab Linux. The fixed-band core and its weighted completion admit the separately constructed descended gate. [Counterexample and evidence](S_LOCAL_WEIGHTED_QUOTIENT.md#why-the-printed-additive-multiplier-needs-a-domain-argument)
