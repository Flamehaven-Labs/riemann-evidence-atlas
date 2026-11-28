# Rational Exterior-Zero Proof Composition

The target is the rational exterior-zero sum from the Masullo formalization's
`traceFormula_exteriorZeros_rat_of_dirichletGRH`. The checked conditional declaration
takes the archived Dirichlet nonvanishing proposition as an input. It retains the upstream
norm section, test-function vanishing, and positive-width assumptions. Binding that input
to Alpöge's actual proof remains **AMBER**.

| Check | Colab Linux result |
| --- | --- |
| Alpöge original `Main.olean` import and theorem audit under 4.33.1 | Blocked by the project import closure |
| Archived GRH premise against its unfolded statement | PASS under 4.33.1 and 4.36.0 |
| Fixed Masullo source replay and axiom audit under 4.36.0 | PASS using verified cached imports |
| Application to the archived GRH premise under 4.36.0 | PASS with the GRH hypothesis |
| Composition with the actual Alpöge theorem | AMBER, first missing shared-environment dependency below |

- Alpöge original Lean 4.33.1 commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6` and Mathlib
  `0df444a360eaa60ab8c11dca51a86af692955474`.
- Masullo commit `6dfe34ef2ef48f1f2c2cfd2274b73663a0eac07c`, Lean 4.36.0, Mathlib
  `fc4f59e577feb1a4956671bc04ac18aaaf8cd842`.
- The source import scan reaches 175,187 of 175,187 Alpöge project modules from `Main` and 307
  of 626 Masullo source modules from `RationalExteriorZeros`. The scan counts module imports.
  A declaration-level proof slice remains a separate task.

The Colab import probe matched the published SHA-256 of both Alpöge object files. With the
small project archive and the full pinned dependency archive on `LEAN_PATH`, Lean exited 1
at `unknown module prefix 'Formalism'`. The corresponding log SHA-256 is
`9ec7c95b77b570e4e05adc86d74dd601071f11731f956528ce5ecfc7c4f66681`.
The run did not reach `#print axioms LFunction_ne_zero_of_half_lt_re`. The upstream MIT
audit records that declaration's axioms as `propext`, `Classical.choice`, and `Quot.sound`.

The diagnostic import identified the first absent object as
`Formalism.GammaFactorNonvanishing.CritLine.olean`. A second run added the
hash-verified object (`10eb57ebfe01dffd2cff3890214eed84dc5e1373da81ddadb6c98eccc40341e7`)
and progressed to `unknown module prefix 'Development'`. The two log hashes are
`a8b9288cf4b27f311fae06a34b10453ea6c3b4aac8c9939d0097ef9ec4a049b0` and
`91bc2e2726dc94a161bbc6b72f7582ce4a29e5a08e6fcd75c39dada3f57205b5`.

Lean 4.33.1 accepted `original_statement_defeq` by `rfl` (exit 0).
The archived proposition body was kept byte-for-byte after replacing `import Mathlib`
with `Mathlib.NumberTheory.LSeries.DirichletContinuation` and
`Mathlib.NumberTheory.LSeries.RiemannZeta`. This probe checks the unfolded GRH premise,
including `(χ ≠ 1 ∨ s ≠ 1)`. A preliminary probe loading the full archived
`Statements.olean` timed out at 300 seconds. The successful narrow probe audit
lists `propext`, `Classical.choice`, and `Quot.sound`.

The shared Lean 4.36.0 source probe also checked the archived
`Supplements/Kernels/MainTheoremsAll.lean` bytes. It stopped at its first
unavailable compiled dependency, `Supplements.Kernels.MainTheoremsCritical`
(exit 1, log SHA-256
`5f214228ec675c676eb54481dad2f6ef5042941d70bd5abc07ad2de331a4d982`).
The dependency count above explains the scope of rebuilding this module path.

The full composition remains **AMBER**. The local candidate uses the isolated
`AtlasAlpoge.Main` module name so that Lake cannot silently take a same-named module
from the Masullo project. The imported Alpöge module must be built from the hash-verified
original `Main.lean` under the same Lean and Mathlib as the rational reduction.

## Masullo source replay

The target source SHA-256 is
`3512f4a932fdca7ed033b6a2d9b7ceb2090c22e0dc46c33ea37667c4445b759a`.
The lock SHA-256 is `cd7d2b7afecd00b17f4465bb2b939ac29d21f7a276556e10e94984e8a827941e`.
Both were verified against the pinned GitHub commit. The dependency cache came from
[upstream CI](https://github.com/mccorvie/riemann-masullo/actions/runs/46069415911).
The GitHub comparison records that its commit differs from the source pin only in two
Markdown files and two progress-report files.

Lean 4.36.0 compiled the pinned `RationalExteriorZeros.lean` source with exit 0 and
no diagnostics, producing public object SHA-256
`ed80a5e3654c5804bea8157fcf7914713d775ce4b04413bcafceb89185e710f5`. This replay
used cached imports. The first attempted axiom audit used separate roots for the rebuilt
module and the cached imports. Lean resolved the shared `RiemannMasullo` prefix to the
first root and could not load `Ch12_TraceGeometric.Sec5`. A second audit puts the rebuilt
object and its private companion in the cache's module tree.

The second audit exited 0 and printed the complete theorem signature. Its axiom
set is `propext`, `Classical.choice`, and `Quot.sound`.
The axiom log SHA-256 is `da125264767e34dae2aa3a22f67de309af3e0c480990dc186c181596b1c45dca`.
The rebuilt private companion SHA-256 is
`04714fd670da5c1fe28d3f5ff372e7089e732df662df4ed49d90414faefdb335`.

The shared 4.36.0 replay compiled `atlas_exterior_zeros_of_archived_statement` with
exit 0 using the newly rebuilt upstream theorem. The source SHA-256 is
`dd3fa1e0356cb450250508af424bc1b95ee2cbbd98eefe40a0f2c4ccbfb3c3ab` and the complete
statement and axiom log SHA-256 is
`5b5d09bf40e870ef0574a7691b911aef00f86d67086fd5840c6324c8b579aae7`.
It reports the same three axioms as the upstream declaration. The 4.36.0
`original_statement_defeq` output is byte-identical to the 4.33.1 output.
The separate build of all dependencies from source was stopped after the scoped replay passed.

## Local source custody

The local [Masullo manuscript](https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf)
matches its existing SHA-256 `e039d3f6cf0a4b14f03c7edb85097752dd65c0a2fe543c76fe992be234f97bf5`.
The archive of the pinned formalization, target Lean source, license, toolchain, and Lake
lock are now preserved separately under [the Lean snapshot manifest](../evidence/rational-exterior/source-sha256.json).
The target source and lock hashes match the Colab compilation inputs.

The local evidence ZIP contains 22 entries, including the checked source, complete
statement and axiom logs, import errors, and checksum manifest. Its SHA-256 is
`17859977e1639dbb5907aff664db6698a4f6bfe4de2846277b446fb3491f87d3`. It was packaged
locally using byte-for-byte reconstructions of the Colab logs, verified against the
SHA-256 printed in Colab. The ZIP generated within Colab has its own hash.

## Public replay files

The saved Colab source, complete statement and axiom output, receipt, and first
blocked import logs are in [the evidence directory](../evidence/rational-exterior/).
Run `sha256sum --check docs/evidence/rational-exterior/SHA256SUMS` from the repository
root to check the archived bytes. The 4.36.0 records document the separate Colab run.

## Replay inputs and commands

In Colab, the notebook sections starting at the [Masullo setup cell](https://colab.research.google.com/drive/18rCY_2FrYEFlEbPlSJ8kw2CjR51PfHCP#scrollTo=xHPkWpytBA9z)
contain the pinned inputs and separate audit commands. Local copies of the audit inputs
and captured logs are under `outputs/rh-proof-value/proof-composition/`. The original
4.33.1 import audit can be reproduced by running `lean -j1 OriginalAudit.lean` on the
official toolchain with the project and dependency archives on `LEAN_PATH`.

For the Masullo audit, check out the pin and restore its Lake lock. Then run:

```sh
lake exe cache get
lake build +RiemannMasullo.Ch13_ZerosHecke.RationalExteriorZeros
lake env lean -j1 MasulloAudit.lean
```

After building both source closures under a shared lock, put the isolated Alpöge build
directory first on the Lean search path and run
`lean -j1 ComposeExteriorZerosIsolated.lean` within that environment. Keep the final
signature and axiom output with the two source hashes and Lake lock. The isolation
guard must confirm that `AtlasAlpoge/Main.olean` was built from the archived source
before the composition is checked.

[Alpöge release verification](https://math.mit.edu/~drew/grh/) ·
[Alpöge compiled input archives](https://proofsandreasons.io/rh-oleans.html) ·
[Masullo's pinned rational reduction](https://github.com/mccorvie/riemann-masullo/blob/6dfe34ef2ef48f1f2c2cfd2274b73663a0eac07c/RiemannMasullo/Ch13_ZerosHecke/RationalExteriorZeros.lean#L648)
