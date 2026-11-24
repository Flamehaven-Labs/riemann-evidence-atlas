$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Py = ((& uv python find --offline 3.14) | Select-Object -First 1).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Python unavailable' }
Push-Location $Root
try {
    & $Py -E -S landau_second_case.py --emit
    if ($LASTEXITCODE -ne 0) { throw 'Second case failed' }
} finally { Pop-Location }
