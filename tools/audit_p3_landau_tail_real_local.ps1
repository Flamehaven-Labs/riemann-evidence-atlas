# Local follow-up to the fixed Landau tail audit.
[CmdletBinding()]
param(
    [string] $Lean,
    [string] $MathlibProject,
    [string] $Python
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (!$Lean) {
    $Lean = Join-Path $Root 'outputs/rh-proof-value/lean-4.33.1-windows/bin/lean.exe'
}
if (!$Python) {
    $Uv = Get-Command uv -ErrorAction SilentlyContinue
    if (!$Uv) {
        Write-Error 'ENV_BLOCKED: uv or an explicit -Python executable is required' -ErrorAction Continue
        exit 2
    }
    $Found = & $Uv.Source python find --offline 3.14
    if ($LASTEXITCODE -ne 0 -or !$Found) {
        Write-Error 'ENV_BLOCKED: offline Python 3.14 was unavailable' -ErrorAction Continue
        exit 2
    }
    $Python = ($Found | Select-Object -First 1).Trim()
}
if (!$MathlibProject) {
    $MathlibProject = Join-Path $Root 'formal/landau'
    $PreservedProject = Join-Path $Root 'outputs/p3-mathlib'
    if (!(Test-Path -LiteralPath (Join-Path $MathlibProject '.lake/packages/mathlib')) -and
            (Test-Path -LiteralPath (Join-Path $PreservedProject '.lake/packages/mathlib'))) {
        $MathlibProject = $PreservedProject
    }
}

$Dir = Join-Path $Root 'outputs/rh-proof-value/validation'
New-Item -ItemType Directory -Path $Dir -Force | Out-Null
$RunId = [guid]::NewGuid().ToString('N')
$Out = Join-Path $Dir "audit-p3-landau-tail-real-$RunId.json"
Push-Location $Root
try {
    Write-Output "MATHLIB_PROJECT $MathlibProject"
    & $Python -E -S tools/verify_landau_tail.py --lean $Lean --mathlib-project $MathlibProject --expect docs/landau-tail-lean-replay.json > $Out
    $Code = $LASTEXITCODE
    if ($Code -ne 0) {
        Write-Output "LANDAU_TAIL_REAL_VERIFIER_EXIT $Code"
        exit $Code
    }
    $Data = Get-Content -LiteralPath $Out -Raw -Encoding utf8 | ConvertFrom-Json
    Write-Output ('MATHLIB_COMMIT ' + $Data.real.mathlib_commit)
    Write-Output ('ACTUAL_OUTPUT_SHA256 ' + (Get-FileHash -LiteralPath $Out -Algorithm SHA256).Hash.ToLowerInvariant())
    Write-Output "REPLAY_RECEIPT $Out"
    Write-Output 'P3_LANDAU_REAL_VERIFIER_REPLAY_PASS'
} finally {
    Pop-Location
}
