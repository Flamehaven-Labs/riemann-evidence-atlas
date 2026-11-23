# P3.1a rational endpoint algebra. No actual Real.exp or integral bridge.
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$LeanHome=Join-Path $Root 'outputs\rh-proof-value\lean-4.33.1-windows'
$Lean=Join-Path $LeanHome 'bin\lean.exe'
$env:LEAN_PATH=(Join-Path $LeanHome 'lib\lean')
$Out=Join-Path $Root 'outputs\rh-proof-value\validation'
$Source=Join-Path $Root 'tests\lean\E2ATailEndpointAlgebra.lean'
$Olean=Join-Path $Out 'E2ATailEndpointAlgebra.olean'
if(-not (Test-Path -LiteralPath $Lean -PathType Leaf)){throw 'LEAN_4_33_1_ENV_BLOCKED'}
$Version=(& $Lean --version) -join ''
if($Version -notlike '*version 4.33.1*'){throw "LEAN_VERSION_MISMATCH $Version"}
New-Item -ItemType Directory -Force -Path $Out | Out-Null
Push-Location $Root
try {
 Write-Output "LEAN_VERSION $Version"
 & $Lean -j 2 -o $Olean $Source
 if($LASTEXITCODE -ne 0){throw 'TAIL_ENDPOINT_LEAN_COMPILE_FAIL'}
 Write-Output 'RAT_ENDPOINT_ALGEBRA_LEAN_COMPILE_PASS'
 $Uv=Get-Command uv -ErrorAction Stop
 foreach($V in @('3.10','3.14')){
  $Py=((& $Uv.Source python find --offline $V)|Select-Object -First 1).Trim()
  if($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $Py -PathType Leaf)){throw ('PYTHON_'+$V+'_ENV_BLOCKED')}
  & $Py -E -S -m unittest discover -s tests -p test_tail_endpoint_algebra.py -v
  if($LASTEXITCODE -ne 0){throw ('PYTHON_'+$V+'_ENDPOINT_TEST_FAIL')}
  Write-Output ('PYTHON_'+$V+'_ENDPOINT_TEST_PASS')
 }
 Write-Output 'P3_1A_RAT_ENDPOINT_ALGEBRA_PASS'
 Write-Output 'P3_1_REAL_CHECK_NOT_RUN_BY_THIS_SCRIPT'
} finally {Pop-Location}
