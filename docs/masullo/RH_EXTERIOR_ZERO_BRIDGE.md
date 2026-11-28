# A Dirichlet GRH Bridge for Exterior Zeros

This is a source-dependent test of the exterior-zero obligation over $\mathbb Q$. It uses the statement attached to Alpöge's compiled `LFunction_eq_zero_re`. The independent weighted S-local trace investigation concerns the descended operator, its diagonal, and the joint cutoff limit. [Alpöge's main declarations](https://math.mit.edu/~drew/grh/#what-was-verified) · [Masullo exterior-zero obligation](https://github.com/mccorvie/riemann-masullo/issues/5571)

## Match the two declarations

| Source | Observed statement | Consequence for the bridge |
| --- | --- | --- |
| Alpöge's archived `Statements.lean` | `DirichletLZerosOnLine` applies to a Dirichlet $L$-function zero with $0<\Re s<1$ | Positive divisor order needs both open-strip membership and a Dirichlet zero at the same $s$ |
| Alpöge's pinned `Main.olean` | `LFunction_eq_zero_re` has type reference `DirichletLZerosOnLine` and value reference `claimAll` | The archived proposition used as a hypothesis has the type reference observed in the original compiled theorem |
| Masullo `Sec5.lean` at `b343e185` | Exterior indices require positive order for `continuedCompletedHeckeL` and $\alpha\le|\Re s-\tfrac12|$ | The index contains the edges and has no open-critical-strip premise |
| Alpöge's `landau_window_ineq` | A real signed integral enters the bound alongside a compact window and a controlled tail | It suggests retaining a signed density. The trace operator would still require its own density and a uniform remainder estimate |

[Archived Alpöge statements](https://math.mit.edu/~drew/grh/#what-was-verified) · [Signed Landau window estimate](../../rh-proof-trace.json) · [Masullo's exterior index and target](https://github.com/mccorvie/riemann-masullo/blob/b343e185c4296c7691cd86bb58ea3fd6e0b7aa61/RiemannMasullo/Ch12_TraceGeometric/Sec5.lean#L67)

## Conditions checked in Lean

Use the same positive-order predicate and the same non-strict exterior inequality as the upstream index. The character type is a parameter so that it can later be instantiated with characters trivial on the chosen norm section. For every such character and every $s$ of positive completed divisor order, the bridge assumes two facts.

1. The zero lies in $0<\Re s<1$.
2. A Dirichlet character of positive modulus represents the given character for zero transfer, and its Mathlib `LFunction` vanishes at the same $s$.

`exterior_empty` applies `DirichletLZerosOnLine` under these assumptions. It rules out the exterior for every $\alpha>0$, including equality in the exterior inequality. `exterior_hasSum_zero` then gives `HasSum term 0` for any complex weight, including a multiplicity times a Fourier–Mellin value. The third declaration supplies a synthetic positive order at $s=0$. It passes any test restricted to the open critical strip and still yields an exterior element. This control tests the logical role of the strip condition.

The upstream private proof `exteriorZeros_isEmpty_of_half_le` already uses the strict strip bounds on this same positive divisor. It converts positive divisor to positive meromorphic order, uses `exteriorZero_re_lt_one`, and reflects across $s\mapsto1-s$ by the functional equation to obtain the lower edge. This is a source-level route to the first input. The local replay checks the bridge from that input and the Dirichlet zero transfer. [Upstream strict-strip argument](https://github.com/mccorvie/riemann-masullo/blob/b343e185c4296c7691cd86bb58ea3fd6e0b7aa61/RiemannMasullo/Ch12_TraceGeometric/Sec5.lean#L241-L288)

**ACCEPT** for the conditional implication. **AMBER** for the correspondence from the actual completed Hecke divisor over $\mathbb Q$ to a Mathlib Dirichlet zero. It requires the rational character identification, matching the analytic continuations at the same $s$, and verifying the completion factors on the open strip. The global-to-local trace comparison and the quotient-kernel limit remain independent obligations. The upstream project keeps this external-result route outside the accepted scope of its proof-repair effort. [Global-to-local comparison](https://github.com/mccorvie/riemann-masullo/issues/7353) · [Quotient-kernel comparison](https://github.com/mccorvie/riemann-masullo/issues/7354)

## Source and replay scope

The archive check verified all 14 part hashes and the joined SHA-256 in the pinned manifest. A streamed tar scan matched the four source members for `Main.lean`, `Statements.lean`, `landauWindow.lean`, and `landauWindowIneq.lean`. Path keywords provide a source inventory for follow-up comparisons. [Archive scan receipt](rh-exterior-archive-scan.json)

The local extractor read the original theorem references from `Main.olean`. On Colab, Lean 4.33.1 and pinned Mathlib `0df444a360eaa60ab8c11dca51a86af692955474` compiled the archived `Statements.lean` body byte-for-byte after replacing its broad `import Mathlib` with two specific Mathlib imports. The bridge takes that exact proposition as a hypothesis. All three declarations passed with only `propext`, `Classical.choice`, and `Quot.sound`. The Colab receipt was reconstructed from the printed JSON and checked against the runtime's receipt hash. The Windows attempts stopped while loading Mathlib `.olean.private` files. [Original artifact references](dirichlet-exterior-original-references.json) · [Colab run](https://colab.research.google.com/drive/18rCY_2FrYEFlEbPlSJ8kw2CjR51PfHCP#scrollTo=xHPkWpytBA9z)

~~~powershell
python tools/verify_dirichlet_exterior_bridge.py --lean outputs/rh-proof-value/lean-4.33.1-windows/bin/lean.exe --mathlib-project outputs/p3-mathlib --main outputs/rh-proof-value/alp-oleans/lib/Main.olean --report bridge-replay.json
~~~

[Lean bridge](../../tests/lean/E2ADirichletExteriorBridge.lean) · [Colab kernel replay receipt](dirichlet-exterior-bridge-replay.json)
