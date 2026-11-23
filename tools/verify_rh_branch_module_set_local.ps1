# Offline replay for four pinned RH .olean modules and five stored declarations.
# Reproduces the JSON twice; writes only ignored outputs/ files.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Base = Join-Path $Root 'outputs\rh-proof-value'
$Lean = Join-Path $Base 'lean-4.33.1-windows\bin\lean.exe'
$Archive = Join-Path $Base 'alp-oleans-Main-and-small.tar.gz'
$BranchDir = Join-Path $Base 'branch-inputs'
$Expected = Join-Path $Root 'docs\rh-branch-module-set.json'
$OutputDir = Join-Path $Base 'validation'
$Output = Join-Path $OutputDir 'rh-branch-module-set-replayed.json'
$Uv = Get-Command uv -ErrorAction Stop
$Py = ((& $Uv.Source python find --offline 3.14) | Select-Object -First 1).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Offline Python unavailable' }
foreach ($Path in @($Py, $Lean, $Archive, $Expected,
    (Join-Path $BranchDir 'CritLine.olean'), (Join-Path $BranchDir 'MainConclusion.olean'))) {
  if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
    throw "Pinned source missing: $Path"
  }
}
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$ExpectedHash = (Get-FileHash -LiteralPath $Expected -Algorithm SHA256).Hash.ToLowerInvariant()
$ExpectedData = Get-Content -LiteralPath $Expected -Raw -Encoding utf8 | ConvertFrom-Json
if ($ExpectedData.analysis.external_closure -ne 'NOT_RUN' -or $ExpectedData.claim_authority -ne 'NONE') {
  throw 'Expected evidence boundary changed'
}
Push-Location $Root
try {
  for ($Attempt = 1; $Attempt -le 2; $Attempt++) {
    Write-Output "RH_BRANCH_REPLAY_ATTEMPT $Attempt"
    & $Py -E -S tools/replay_rh_module_set.py --lean $Lean --archive $Archive --branch-dir $BranchDir > $Output
    if ($LASTEXITCODE -ne 0) { throw "Lean direct reference replay failed on attempt $Attempt" }
    # Native PowerShell redirection produces CRLF: restore JSON CLI LF contract.
    $Text = [IO.File]::ReadAllText($Output)
    [IO.File]::WriteAllText($Output, $Text.Replace([Environment]::NewLine, [string][char]10), [Text.UTF8Encoding]::new($false))
    $ActualHash = (Get-FileHash -LiteralPath $Output -Algorithm SHA256).Hash.ToLowerInvariant()
    Write-Output "ACTUAL_SHA256 $ActualHash"
    Write-Output "EXPECTED_SHA256 $ExpectedHash"
    if ($ActualHash -ne $ExpectedHash) { throw 'Saved branch receipt byte mismatch' }
    $Data = Get-Content -LiteralPath $Output -Raw -Encoding utf8 | ConvertFrom-Json
    $ValueEdges = @($Data.analysis.resolved_edges | Where-Object { $_.kind -eq 'value' })
    $Reached = @($Data.analysis.reached_declarations.PSObject.Properties)
    $Modules = @($Data.module_inputs.PSObject.Properties)
    if ($ValueEdges.Count -ne 4 -or $Reached.Count -ne 5 -or $Modules.Count -ne 4 -or
        $Data.analysis.external_closure -ne 'NOT_RUN' -or $Data.claim_authority -ne 'NONE') {
      throw 'Source/value/import or open-boundary invariants violated'
    }
    if ('Formalism.VW.rh_of_right' -notin @($Data.analysis.external_or_unresolved_references) -or
        'UpperTheory.FinalTheorems.everyCharacter_of_row' -notin @($Data.analysis.external_or_unresolved_references)) {
      throw 'Open reference frontier was not preserved'
    }
    Write-Output "RH_BRANCH_REPLAY_ATTEMPT $Attempt PASS modules=4 declarations=5 value_edges=4"
  }
} finally {
  Pop-Location
}
Write-Output 'RH_BRANCH_REPLAY_PASS; RH_KERNEL_NOT_RUN; COLAB_NOT_RUN'
