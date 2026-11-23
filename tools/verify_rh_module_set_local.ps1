# Recompute the pinned two-module Lean reference receipt twice, offline.
# The only generated file is in ignored outputs/rh-proof-value/validation.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Lean = Join-Path $Root 'outputs\rh-proof-value\lean-4.33.1-windows\bin\lean.exe'
$Archive = Join-Path $Root 'outputs\rh-proof-value\alp-oleans-Main-and-small.tar.gz'
$Expected = Join-Path $Root 'docs\rh-module-set-pilot.json'
$Dir = Join-Path $Root 'outputs\rh-proof-value\validation'
$Candidate = Join-Path $Dir 'rh-module-set-replayed.json'
$Uv = Get-Command uv -ErrorAction Stop
$Py = ((& $Uv.Source python find --offline 3.14) | Select-Object -First 1).Trim()
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $Py -PathType Leaf)) {
  throw 'offline Python 3.14 unavailable'
}
foreach ($p in @($Lean, $Archive, $Expected)) {
  if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "Missing pinned input $p" }
}
New-Item -ItemType Directory -Force -Path $Dir | Out-Null
$ExpectedHash = (Get-FileHash -LiteralPath $Expected -Algorithm SHA256).Hash.ToLowerInvariant()
$ExpectedData = Get-Content -LiteralPath $Expected -Raw -Encoding utf8 | ConvertFrom-Json
if ($ExpectedData.analysis.external_closure -ne 'NOT_RUN') { throw 'Expected scope changed' }
Push-Location $Root
try {
  for ($Attempt = 1; $Attempt -le 2; $Attempt++) {
    Write-Output "MODULE_REPLAY_ATTEMPT $Attempt"
    & $Py -E -S 'tools/replay_rh_module_set.py' --lean $Lean --archive $Archive > $Candidate
    if ($LASTEXITCODE -ne 0) { throw "Module set extractor failed attempt $Attempt" }
    # PowerShell's native stdout redirection used CRLF on this Windows host.
    # Normalize only the ignored verification output to the CLI's LF JSON contract.
    $Txt = [IO.File]::ReadAllText($Candidate)
    [IO.File]::WriteAllText($Candidate, $Txt.Replace("`r`n", "`n"), [Text.UTF8Encoding]::new($false))
    $GotHash = (Get-FileHash -LiteralPath $Candidate -Algorithm SHA256).Hash.ToLowerInvariant()
    $Output = Get-Content -LiteralPath $Candidate -Raw -Encoding utf8 | ConvertFrom-Json
    Write-Output "CURRENT_RECEIPT_SHA256 $GotHash"
    Write-Output "EXPECTED_RECEIPT_SHA256 $ExpectedHash"
    if ($GotHash -ne $ExpectedHash) { throw 'Byte-for-byte module-set receipt mismatch' }
    $Edges = @($Output.analysis.resolved_edges | Where-Object { $_.kind -eq 'value' })
    if ($Edges.Count -ne 2 -or
        $Output.analysis.reached_declarations.riemannHypothesis -ne 'Main' -or
        $Output.analysis.reached_declarations.rhOfAll -ne 'Supplements.Kernels.MainTheorems' -or
        $Output.analysis.reached_declarations.allChi -ne 'Supplements.Kernels.MainTheorems' -or
        $Output.analysis.external_closure -ne 'NOT_RUN' -or
        $Output.claim_authority -ne 'NONE') {
      throw 'Module-set proof-ref boundary contract mismatch'
    }
    Write-Output "MODULE_REPLAY_ATTEMPT $Attempt PASS edges=$($Edges.Count)"
  }
} finally { Pop-Location }
Write-Output 'TWO_MODULE_LEAN_REPLAY_PASS; ORIGINAL_KERNEL_REPLAY_NOT_RUN'
