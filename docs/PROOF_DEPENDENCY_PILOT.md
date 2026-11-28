# Extracting Direct References from Lean Declarations

The pilot targets `riemannHypothesis` in the original RH project's `Main.lean`.
It extracts direct references. Transitive dependencies, a kernel recheck,
and whether a numerical object is nonconstructive are separate questions.

## Inputs and Extraction Method

From the [Proofs & Reasons build archive](https://proofsandreasons.io/rh-oleans.html),
we downloaded `alp-oleans-Main-and-small.tar.gz` and checked SHA-256 for the archive
and its member `alp-oleans/lib/Main.olean`.
The member SHA-256 `9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad`
matches the [MIT verification record](https://math.mit.edu/~drew/grh/).
External artifacts are preserved under `outputs/`. The ordinary numerical
regressions require neither those files nor Lean.

For the Windows [Lean 4.33.1 distribution](https://github.com/leanprover/lean4/releases/tag/v4.33.1),
we checked `lean-4.33.1-windows.tar.zst` against the official SHA-256
`f63029c0e1e6daed0f4807481b6fcd8f8b77fbce6d63f205c7f9191072387a7a`.
Lean 4.34.0-rc2 rejected the original module due to incompatible headers.

The [Lean extractor](../tools/ProofRefs.lean) reads one compiled artifact with
`Lean.readModuleData`. It applies `Expr.getUsedConstants` separately to
`ConstantInfo.type` and `ConstantInfo.value? (allowOpaque := true)`.
It records the module header's imports in a separate field.
The extractor reads the stored expressions directly. Source compilation
and text-based reference inference are outside this extraction step.

## Original Results

Lean 4.33.1 read the original `Main.olean` and returned the following.
[Execution JSON](rh-proof-refs-pilot.json)

| Location | Direct references |
| --- | --- |
| Module header | Two `Init` entries, `Statements`, `Supplements.Kernels.MainTheoremsAll` |
| Theorem type | `RiemannHypothesis` |
| Proof term | `rhOfAll` |

`Statements` and `Supplements.Kernels.MainTheoremsAll` do not appear in this
declaration's direct type or proof-term references. The extracted direct
references distinguish the declaration's dependencies from the import graph.
The absence of a direct `Classical.choice` reference leaves transitive dependency
open. The MIT record reports transitive axioms separately.

For comparison we checked the SHA-256 of the [public dependency graph](https://proofsandreasons.io/rh-graph.html)
archive and read two nodes.
The body of `riemannHypothesis` points to `rhOfAll`, whose body references
`Formalism.VW.rh_of_every` and `allChi`. The public graph omits Mathlib
and Lean core declarations. An empty signature array in the first node
therefore does not exclude a reference to Mathlib's `RiemannHypothesis`.

## Controls

We compiled the [synthetic fixture](../tests/lean/ProofRefsFixture.lean) with Lean 4.33.1.
The type of `probeTarget` refers to `ProbeProperty` and its value refers to
`probeWitness`. The header import `Lean.Util.FoldConsts` is absent
from both reference lists.

Both `probeUsesChoice` and `probeChosenNat` contain a direct `Classical.choice` reference.
The former proves a proposition. The latter defines a chosen natural number.
Checking direct references alone leaves open whether a numerical evaluation
will need the original cutoff.

## Linking Two Original Modules

From the same pinned archive we read `Main.olean` and
`Supplements/Kernels/MainTheorems.olean`. The second file has SHA-256
`ccf715ec0e2be6075cefe8cae3f43de6e18501959fa768970b1e11d81683d02f`.
[Run record](rh-module-set-pilot.json)

| Declaration | Direct type references | Direct proof-term references |
| --- | --- | --- |
| `riemannHypothesis` | `RiemannHypothesis` | `rhOfAll` |
| `rhOfAll` | `RiemannHypothesis` | `Formalism.VW.rh_of_every`, `allChi` |
| `allChi` | `UpperTheory.EveryCharacter` | `UpperTheory.FinalTheorems.everyCharacter` |

`riemannHypothesis → rhOfAll` connects values read from two compiled files.
`rhOfAll → allChi` is a value reference in the second module.
The bodies of `rh_of_every` and `everyCharacter` remained unresolved in this run.
`RiemannHypothesis` and `EveryCharacter` are type references.
The run confirmed two value edges and leaves other transitive dependencies open.
Reachability of `Classical.choice` and numerical relevance below the open branches
require further evidence.

## Extending Both Branches

We compared the archive hash for the publisher's [per-member SHA-256 list](https://photos.proofsandreasons.io/alp-oleans-357309b5dd12/SHA256SUMS-project-oleans.txt.gz)
against the [published checksums](https://photos.proofsandreasons.io/alp-oleans-357309b5dd12/SHA256SUMS).
We extracted the following files from the public `Formalism` and
`Development-AutomorphicArithmetic` bundles and checked each member's SHA-256.
This run checked the selected members individually. Full bundle rehashing was unrun.

| File | SHA-256 | Declaration read directly |
| --- | --- | --- |
| `CritLine.olean` | `10eb57ebfe01dffd2cff3890214eed84dc5e1373da81ddadb6c98eccc40341e7` | `Formalism.VW.rh_of_every` |
| `MainConclusion.olean` | `96f053d27b81461fcf5ca2fe9a234384bc6ead9697de76cee37e13686aa156df` | `UpperTheory.FinalTheorems.everyCharacter` |

Lean 4.33.1 linked **five declarations in four modules with four internal VALUE edges**.
The new edges are `rhOfAll → Formalism.VW.rh_of_every` and
`allChi → UpperTheory.FinalTheorems.everyCharacter`.
The first branch references `rh_of_right` and `DirichletCharacter.LFunction_modOne_eq`
among other declarations. The second references `everyCharacter_of_row`
and `galoisLocalGlobalStrong_recParameter`.
[Extended run record](rh-branch-module-set.json)

Two LF-normalized JSON outputs matched byte for byte. The scope was five declarations.
Full transitive dependencies and `Classical.choice` paths remained open.

## Next Layer of Both Branches

`RhOfRight.olean` was extracted from the previously preserved start
of the `Formalism` archive and matched the publisher's per-member SHA-256
`cf24f82f3f24144070062b19beedf83f0919c4e894c56759597fa76e2e93bc70`.
`everyCharacter_of_row` was read from the saved `MainConclusion.olean`.
[Next-layer run record](rh-next-layer-module-set.json)

| New VALUE edge | Key direct references of the target |
| --- | --- |
| `Formalism.VW.rh_of_every → Formalism.VW.rh_of_right` | `riemannZeta_one_sub`, `Complex.Gamma_ne_zero_of_re_pos`, `propext` |
| `UpperTheory.FinalTheorems.everyCharacter → UpperTheory.FinalTheorems.everyCharacter_of_row` | `every_character_of_literature_of_vWin`, `UpperTheory.One.vwin_of_row`, `UpperTheory.Zero.LLC.recTExists` |

Lean 4.33.1 read seven declarations in five modules and recorded six
connected VALUE edges. Two LF-normalized outputs matched byte for byte.
`propext` is a direct VALUE reference of `rh_of_right`.
Other axioms and transitive `Classical.choice` reachability require extending
the unresolved references. The original full proof kernel recheck was unrun.

## Origin and Kind of Unresolved VALUE References

The next stage grouped unresolved VALUE references of the seven declarations by name.
Each entry preserves the proofs that reference it.
[Classification results](rh-frontier-classification.json)

- For declarations found in an original `.olean`, record the actual module and declaration kind.
   Extract direct VALUE references when a value is stored.
- For constants found in Lean 4.33.1, record the module and declaration kind supplied by the environment.
   This run does not recursively follow values of toolchain constants.
- A name found only in the public graph remains a candidate source and kind.
   Axiom status remains unconfirmed. Names absent from both inputs
   stay unconfirmed.

| Evidence | Unique references |
| --- | ---: |
| Directly matched in Lean 4.33.1 `Init` | 76 |
| Directly matched in original RH `.olean` files | 2 |
| Candidate source or kind in the public graph | 10 |
| Unconfirmed | 290 |

The direct `propext` reference of `rh_of_right` is an axiom declared in `Init.Core`.
The two helper proofs in the same `RhOfRight.olean`,
`rh_of_right._proof_1_1` and `rh_of_right._proof_1_2`, were also read.
Each has 57 direct references. `vwin_of_row` remains a public graph candidate.
The compiled artifact is needed to read its declaration kind and body directly.

Loading all of Lean and Std exceeded 120 seconds. Both successful runs were
limited to `Init` and the pinned RH files. Their JSON matched byte for byte.
The axiom classification gives each constant's immediate declaration kind.
Complete RH axiom dependencies and transitive `Classical.choice` reachability remain unconfirmed.

## Replay Commands

Run from the repository root with the original pinned Lean 4.33.1.
The Python wrapper checks the `Main.olean` digest and Lean version before
extracting the single original declaration.

```powershell
python -E -S tools/replay_rh_proof_refs.py --lean (Get-Command lean).Source --module outputs/rh-proof-value/alp-oleans/lib/Main.olean
python -E -S tools/replay_rh_module_set.py --lean (Get-Command lean).Source --archive outputs/rh-proof-value/alp-oleans-Main-and-small.tar.gz
python -E -S tools/replay_rh_module_set.py --lean (Get-Command lean).Source --archive outputs/rh-proof-value/alp-oleans-Main-and-small.tar.gz --branch-dir outputs/rh-proof-value/branch-inputs
python -E -S tools/replay_rh_module_set.py --lean (Get-Command lean).Source --archive outputs/rh-proof-value/alp-oleans-Main-and-small.tar.gz --branch-dir outputs/rh-proof-value/branch-inputs --next-layer
python -E -S tools/replay_rh_frontier.py --lean (Get-Command lean).Source --frontier docs/rh-next-layer-module-set.json --archive outputs/rh-proof-value/alp-oleans-Main-and-small.tar.gz --branch-dir outputs/rh-proof-value/branch-inputs --graph outputs/rh-proof-value/verified-rh-graph.json.gz
lean -o outputs/rh-proof-value/ProofRefsFixture.olean tests/lean/ProofRefsFixture.lean
lean --run tools/ProofRefs.lean outputs/rh-proof-value/ProofRefsFixture.olean probeTarget
```
