# Re-emit five-module Lean proof-value surface twice; no tracked output changes.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Base = Join-Path $Root 'outputs\rh-proof-value'
$Lean = Join-Path $Base 'lean-4.33.1-windows\bin\lean.exe'
$Archive = Join-Path $Base 'alp-oleans-Main-and-small.tar.gz'
$BranchDir = Join-Path $Base 'branch-inputs'
$Expected = Join-Path $Root 'docs\rh-next-layer-module-set.json'
$OutDir = Join-Path $Base 'validation'
$OutFile = Join-Path $OutDir 'rh-next-layer-module-set-replayed.json'
$Uv = Get-Command uv -ErrorAction Stop
$Py = ((& $Uv.Source python find --offline 3.14) | Select-Object -First 1).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Pinned offline Python unavailable' }
foreach($p in @($Lean,$Archive,$Py,$Expected,
    (Join-Path $BranchDir 'CritLine.olean'),
    (Join-Path $BranchDir 'MainConclusion.olean'),
    (Join-Path $BranchDir 'RhOfRight.olean'))) {
  if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "Input unavailable $p" }
}
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$ExpectedHash = (Get-FileHash -LiteralPath $Expected -Algorithm SHA256).Hash.ToLowerInvariant()
Push-Location $Root
try {
  for($attempt=1;$attempt -le 2;$attempt++) {
    Write-Output "NEXT_LAYER_REPLAY_ATTEMPT $attempt"
    & $Py -E -S tools/replay_rh_module_set.py --lean $Lean --archive $Archive --branch-dir $BranchDir --next-layer > $OutFile
    if($LASTEXITCODE -ne 0) { throw "Lean extraction failed on attempt $attempt" }
    # Restore Python's LF-only JSON output after Windows PowerShell redirect.
    $Body=[IO.File]::ReadAllText($OutFile)
    [IO.File]::WriteAllText($OutFile,$Body.Replace([Environment]::NewLine,[string][char]10),[Text.UTF8Encoding]::new($false))
    $GotHash=(Get-FileHash -LiteralPath $OutFile -Algorithm SHA256).Hash.ToLowerInvariant()
    Write-Output "RESULT_SHA256 $GotHash"
    Write-Output "PIN_SHA256 $ExpectedHash"
    if($GotHash -ne $ExpectedHash) { throw 'JSON byte identity differs from pinned record' }
    $data=Get-Content -LiteralPath $OutFile -Raw -Encoding utf8 | ConvertFrom-Json
    $modules=@($data.module_inputs.PSObject.Properties)
    $records=@($data.records)
    $edges=@($data.analysis.resolved_edges | Where-Object { $_.kind -eq 'value' })
    $unresolved=@($data.analysis.external_or_unresolved_references)
    $right=@($records | Where-Object { $_.declaration -eq 'Formalism.VW.rh_of_right' })
    if($modules.Count -ne 5 -or $records.Count -ne 7 -or $edges.Count -ne 6 -or
       $right.Count -ne 1 -or 'propext' -notin $right[0].value_refs -or
       $data.analysis.external_closure -ne 'NOT_RUN' -or
       $data.analysis.original_proof_kernel_replay -ne 'NOT_RUN' -or
       $data.claim_authority -ne 'NONE') {
      throw 'Proof-value scope/identity invariant mismatch'
    }
    if ('UpperTheory.One.vwin_of_row' -notin $unresolved -or 'Formalism.VW.rh_of_right' -in $unresolved) {
      throw 'Expected open/closed edge scope mismatch'
    }
    Write-Output "NEXT_LAYER_REPLAY_ATTEMPT $attempt PASS modules=5 declarations=7 value_edges=6 unresolved=$($unresolved.Count) propext=OBSERVED"
  }
} finally { Pop-Location }
Write-Output 'NEXT_LAYER_LOCAL_REPLAY_PASS; KERNEL_RH_NOT_RUN; COLAB_NOT_RUN'
