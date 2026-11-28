# Riemann Lean Evidence — Local Development Validation on 2026-11-23

**Status** — LOCAL_DEVELOPMENT_VALIDATION / claim_authority: NONE
**Baseline** — v0.1.0 annotated tag → 8192cf0923995e200185f271fba76b2387db9d67.
**Development objective** — Strengthen verification of the v0.2.0 proof-reference pilot. Release acceptance was pending at this snapshot.

## 1. Implementation Scope

- riemann_evidence/proof_dependency.py validates the direct-reference schema and follows VALUE edges within the same module. It keeps type, value, and import references separate and marks external references unresolved.
- tools/replay_proof_dependency.py checks the official Lean 4.33.1 binary and input .olean SHA-256, extracts direct references repeatedly, and analyzes VALUE paths within one module. readModuleData reads stored expressions.
- tests/lean/ChoiceDependenceFixture.lean exercises Classical.choice in a direct proof and in paths to a chosen value through computational definitions or theorems, in both Lean source and .olean.
- tests/test_proof_dependency.py adds 10 regressions for import exclusion, proof/data Choice paths, missing/external references, cycles, malformed schemas, duplicate edges, budget overruns, and the earlier Main result.
- tools/local_notebook_smoke.py runs the actual RH_Window.ipynb code cells using the standard library in a temporary directory. It compares the generated report and digest to window-results-v2.json. This executes locally.
- tools/validate_local_pilot.ps1 verifies with official Windows Lean 4.33.1, the saved Main.olean, and offline Python, with result JSON under the ignored outputs/ directory.
- tools/validate_python_matrix.ps1 finds offline Python 3.10 and 3.14 with uv and runs unittest, saved report verification, and notebook cell replay under each version.
- .github/workflows/checks.yml adds an offline notebook smoke test to the then-current Windows/Linux Python 3.10/3.13 matrix. Remote GitHub CI was unrun in this validation.

## 2. Execution Receipts

| Check | Observation | Receipt |
| --- | --- | --- |
| Original Main.olean direct references | Type RiemannHypothesis, value rhOfAll. Imports are kept separate. | r_03fa109c-24e9-4fc8-9495-ecd0caaa78fb |
| Lean version | Lean 4.33.1 Windows, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6 | Same |
| Python version | CPython 3.14.10 Windows | Same |
| Python unittest | **17/17 passed** | Same |
| Recomputed numerical JSON | REPORT MATCH for ten cases | Same |
| Offline notebook cells | Ten cases and the same SHA-256 as the saved JSON | Same |
| Synthetic Lean fixture | .olean compilation succeeded | Same |
| Synthetic Choice path split | At least one data-definition path and one direct proof-value path | Same |
| Offline Python matrix | Python 3.10.22 and 3.14.10 each passed 17 tests, report comparison, and notebook smoke | r_2cb8d4e3-8827-4176-81d7-2c828f1b0323 |
| Separate leanchecker attempt | Memory error on --help. An absolute path to the synthetic .olean did not resolve as a module. | r_17211129-eca5-4c10-b744-d6275a642141 |

### File and Receipt Identity

- Original Main.olean SHA-256 — **9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad**.
- Preserved pilot JSON — docs/rh-proof-refs-pilot.json.
- Original declaration analysis — outputs/rh-proof-value/validation/original-main-value-paths.json.
  SHA-256 **ac23095dd157c9d194cc98951d3ae753ab73c88504b0255343e4d23e980190a9**.
- Synthetic fixture analysis — outputs/rh-proof-value/validation/choice-fixture-value-paths.json.
  SHA-256 **f417e7a64cf455945fabf5042ea0726dde85895c9e7b120194599689ba9a420e**.
- Saved numerical result and generated notebook result SHA-256 — **ad3d31ceaf5a9a78e5f17f5c25ac087394eb57ebfb3cfdd977aa57c61ac66bf1**.
- Original RH_Window.ipynb SHA-256 — **e55a9f45b0a4d190d154050eb3184d83fa975aac75a53a9d19c3b2af34289eb1**.

## 3. Two Kinds of Classical.choice Reference

Observed VALUE reference paths in the synthetic Lean fixture follow.

~~~text
auditProofCallsChoice (theorem) → Classical.choice
  position: PROOF_VALUE_PATH_CANDIDATE

auditProofMentionsComputed (theorem)
  → auditComputedFromChosen (definition)
  → auditChosenNat (definition)
  → Classical.choice
  position: DATA_DEFINITION_PATH_CANDIDATE
~~~

This classifies syntactic and definition dependencies in the source and proof terms. Whether evaluation must use the chosen value, or the original function admits a derivative bound, requires a separate argument. The output states **numeric_relevance: NOT_ESTABLISHED**.

The original riemannHypothesis has the recorded state below.

~~~text
type → RiemannHypothesis
value → rhOfAll (EXTERNAL_OR_UNRESOLVED)
transitive original closure → NOT_RUN
independent original kernel replay → NOT_RUN
~~~

An import without a direct reference does not become a proof edge.

## 4. Failures and Blockers

### Python Executable Resolution — Resolved

The MCP python-unittest profile hit the Windows Store python alias and failed to start. A PowerShell retry through the default alias returned 9009. Explicit offline uv-managed Python 3.10.22 and 3.14.10 both succeeded without external packages or network access.

### leanchecker Resources and Module Resolution — Open

An additional Lean 4.33.1 leanchecker.exe check failed at --help with **INTERNAL PANIC: out of memory**. An absolute path to the synthetic .olean did not resolve as a module name. The checker had yet to reach the original result.

tools/check_leanchecker_fixture.ps1 records the blocked retry. Before trying again, establish the supported CLI and module resolution, .olean dependency closure, memory budget, and process limits. Status **BLOCKED[LEANCHECKER_RESOURCE_AND_MODULE_RESOLUTION]** records an execution blocker.

## 5. Commands and Unverified Areas

Run from the workspace root in Windows PowerShell 7.

~~~powershell
pwsh -NoProfile -File .\tools\validate_python_matrix.ps1
pwsh -NoProfile -File .\tools\validate_local_pilot.ps1
~~~

Numerical modules and notebook smoke require only the Python standard library. Original .olean extraction needs the official Lean 4.33.1 build and the exact Main.olean, separately preserved under outputs/ outside Git.

**Pending at this snapshot**
1. An actual Google Colab upload, replay, and receipt for RH_Window.ipynb. No authenticated session was available. **NOT_RUN**.
2. Transitive proof-value closure of the original RH proof, including rhOfAll and lower imported declarations with missing original .olean files. **OPEN**.
3. Full original RH kernel or independent checker replay. **BLOCKED / NOT_RUN**.
4. Actual remote GitHub CI. **NOT_RUN**.
5. Source-pinned Lean bridge for the NSRW MB06 ratio lower bound and transfer to TOE. **NOT_RUN**.

## 6. Acceptance Criteria for Later Stages

- **v0.1.0** — Ten-case standalone numerical baseline, locally validated at the original annotated tag.
- **v0.2.0 pilot** — One original declaration's direct type/value references and the synthetic intra-module transitive Choice paths replayed. Imported theorem expansion and original Mathlib closure are separate.
- **v0.2.0 release candidate** — Read at least one imported declaration from another pinned .olean, link it, and inspect cross-module value dependencies through definitions, opaque declarations, and axioms. Obtain independent replay evidence.
- **v0.3.0** — Pinned Lean compilation and kernel evidence for a small exponential or ratio bound tied to exact source definitions and assumptions.

As of 2026-11-23, the verified scope was standalone numerical replay, local notebook execution, direct theorem-reference extraction, and synthetic Choice-path classification. The full original RH proof remained outside the run.
