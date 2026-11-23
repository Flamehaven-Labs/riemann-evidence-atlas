# Offline Python compatibility matrix for the standalone source and notebook cells.
# No external packages, networks, or project venv. No tracked output changes.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Uv = Get-Command uv -ErrorAction Stop
Push-Location $Root
try {
  foreach($Version in @('3.10','3.14')) {
    $Py = ((& $Uv.Source python find --offline $Version) | Select-Object -First 1).Trim()
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $Py -PathType Leaf)) { throw "Offline Python $Version unavailable" }
    Write-Output "MATRIX_VERSION $Version"
    & $Py --version
    & $Py -E -S -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw "Unit tests failed for $Version" }
    & $Py -E -S window_kernel.py --verify-report window-results-v2.json
    if ($LASTEXITCODE -ne 0) { throw "Report replay failed for $Version" }
    & $Py -E -S tools/local_notebook_smoke.py
    if ($LASTEXITCODE -ne 0) { throw "Notebook smoke failed for $Version" }
  }
} finally { Pop-Location }
Write-Output 'PYTHON_MATRIX_PASS'
