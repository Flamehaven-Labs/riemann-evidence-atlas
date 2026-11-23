# Fully offline; all generated .olean files are within ignored outputs/.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$LeanHome = Join-Path $Root 'outputs\rh-proof-value\lean-4.33.1-windows'
$Lean = Join-Path $LeanHome 'bin\lean.exe'
$Module = Join-Path $Root 'outputs\rh-proof-value\alp-oleans\lib\Main.olean'
$OutDir = Join-Path $Root 'outputs\rh-proof-value\validation'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
if (-not (Test-Path -LiteralPath $Lean -PathType Leaf)) { throw 'Lean 4.33.1 executable unavailable' }
if (-not (Test-Path -LiteralPath $Module -PathType Leaf)) { throw 'Main.olean unavailable' }
$env:LEAN_PATH = (Join-Path $LeanHome 'lib\lean')
$Uv = Get-Command uv -ErrorAction SilentlyContinue
if ($null -eq $Uv) { throw 'uv offline Python locator unavailable' }
$Py = ((& $Uv.Source python find --offline) | Select-Object -First 1).Trim()
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $Py -PathType Leaf)) {
  throw 'No offline local Python interpreter'
}
Write-Output 'LEAN_VERSION'
& $Lean --version
if ($LASTEXITCODE -ne 0) { throw 'Lean version failed' }
Write-Output 'PYTHON_VERSION'
& $Py --version
if ($LASTEXITCODE -ne 0) { throw 'Python version failed' }
Push-Location $Root
try {
  Write-Output 'PYTHON_REGRESSION_TESTS'
  & $Py -E -S -m unittest discover -s tests -v
  if ($LASTEXITCODE -ne 0) { throw 'Python unit tests failed' }
  Write-Output 'SAVED_NUMERICAL_REPORT_REPLAY'
  & $Py -E -S window_kernel.py --verify-report window-results-v2.json
  if ($LASTEXITCODE -ne 0) { throw 'Saved numeric report mismatch' }
  Write-Output 'LOCAL_NOTEBOOK_CELL_EXECUTION'
  & $Py -E -S tools/local_notebook_smoke.py
  if ($LASTEXITCODE -ne 0) { throw 'Notebook cell smoke failed' }
} finally { Pop-Location }
$OriginalRaw = & $Py -E -S (Join-Path $Root 'tools\replay_proof_dependency.py') --lean $Lean --module $Module --target riemannHypothesis --expected-sha256 '9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad'
if ($LASTEXITCODE -ne 0) { throw 'Original Main.olean replay failed' }
$OriginalJson = $OriginalRaw -join [Environment]::NewLine
$Original = $OriginalJson | ConvertFrom-Json
if ($Original.analyses.riemannHypothesis.direct_type_refs[0] -ne 'RiemannHypothesis' -or $Original.analyses.riemannHypothesis.direct_value_refs[0] -ne 'rhOfAll' -or $Original.analyses.riemannHypothesis.external_closure -ne 'NOT_RUN') {
  throw 'Original direct reference contract mismatch'
}
[IO.File]::WriteAllText((Join-Path $OutDir 'original-main-value-paths.json'), $OriginalJson + [Environment]::NewLine, [Text.UTF8Encoding]::new($false))
Write-Output 'ORIGINAL_MAIN_REFS PASS (direct only)'
$Fixture = Join-Path $Root 'tests\lean\ChoiceDependenceFixture.lean'
$FixtureOlean = Join-Path $OutDir 'ChoiceDependenceFixture.olean'
& $Lean -o $FixtureOlean $Fixture
if ($LASTEXITCODE -ne 0) { throw 'Choice fixture Lean compile failed' }
$FixtureRaw = & $Py -E -S (Join-Path $Root 'tools\replay_proof_dependency.py') --lean $Lean --module $FixtureOlean --target auditProofMentionsComputed --target auditComputedFromChosen --target auditChosenNat --target auditProofCallsChoice --target auditIndependent
if ($LASTEXITCODE -ne 0) { throw 'Choice dependence replay failed' }
$FixtureJson = $FixtureRaw -join [Environment]::NewLine
$FixtureGraph = $FixtureJson | ConvertFrom-Json
$DataPath = @($FixtureGraph.analyses.auditComputedFromChosen.choice_paths | Where-Object { $_.position -eq 'DATA_DEFINITION_PATH_CANDIDATE' })
$ProofPath = @($FixtureGraph.analyses.auditProofCallsChoice.choice_paths | Where-Object { $_.position -eq 'PROOF_VALUE_PATH_CANDIDATE' })
if ($DataPath.Count -lt 1 -or $ProofPath.Count -lt 1) { throw 'Choice discriminant not observed' }
[IO.File]::WriteAllText((Join-Path $OutDir 'choice-fixture-value-paths.json'), $FixtureJson + [Environment]::NewLine, [Text.UTF8Encoding]::new($false))
Write-Output "CHOICE_CLASSIFICATION PASS data=$($DataPath.Count) proof=$($ProofPath.Count)"
Write-Output 'COMPLETE_LOCAL_VALIDATION PASS; original kernel replay NOT_RUN; Colab NOT_RUN'
