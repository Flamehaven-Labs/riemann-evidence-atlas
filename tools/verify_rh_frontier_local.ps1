# Replay the bounded value-frontier classification under pinned Lean 4.33.1, twice.
# Writes ONLY ignored outputs/rh-proof-value/validation.
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Base=Join-Path $Root 'outputs\rh-proof-value'
$LeanHome=Join-Path $Base 'lean-4.33.1-windows'
$Lean=Join-Path $LeanHome 'bin\lean.exe'
$env:LEAN_PATH=Join-Path $LeanHome 'lib\lean'
$Archive=Join-Path $Base 'alp-oleans-Main-and-small.tar.gz'
$Graph=Join-Path $Base 'verified-rh-graph.json.gz'
$Branches=Join-Path $Base 'branch-inputs'
$Seed=Join-Path $Root 'docs\rh-next-layer-module-set.json'
$Reference=Join-Path $Root 'docs\rh-frontier-classification.json'
$OutputDir=Join-Path $Base 'validation'
$Result=Join-Path $OutputDir 'rh-frontier-classification-replayed.json'
$Uv=Get-Command uv -ErrorAction Stop
$Python=((& $Uv.Source python find --offline 3.14)|Select-Object -First 1).Trim()
if($LASTEXITCODE -ne 0){throw 'uv Python 3.14 discovery failed'}
foreach($file in @($Lean,$Archive,$Graph,$Seed,$Reference,$Python,(Join-Path $Branches 'RhOfRight.olean'))){
 if(-not (Test-Path -LiteralPath $file -PathType Leaf)){throw "Missing pinned input: $file"}
}
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$ReferenceHash=(Get-FileHash -LiteralPath $Reference -Algorithm SHA256).Hash.ToLowerInvariant()
Push-Location $Root
try {
 for($n=1;$n -le 2;$n++){
  Write-Output "FRONTIER_REPLAY_ATTEMPT $n"
  & $Python -E -S tools/replay_rh_frontier.py --lean $Lean --frontier $Seed --archive $Archive --branch-dir $Branches --graph $Graph > $Result
  if($LASTEXITCODE -ne 0){throw "Frontier extractor failed attempt $n"}
  $Body=[IO.File]::ReadAllText($Result)
  [IO.File]::WriteAllText($Result,$Body.Replace([Environment]::NewLine,[string][char]10),[Text.UTF8Encoding]::new($false))
  $CurrentHash=(Get-FileHash -LiteralPath $Result -Algorithm SHA256).Hash.ToLowerInvariant()
  Write-Output "CURRENT_SHA256 $CurrentHash"
  Write-Output "REFERENCE_SHA256 $ReferenceHash"
  if($CurrentHash -ne $ReferenceHash){throw 'Canonical frontier output differs from pinned record'}
  $Data=Get-Content -LiteralPath $Result -Raw -Encoding utf8 | ConvertFrom-Json
  $Counts=$Data.evidence_counts
  $A=@($Data.frontier | Where-Object {$_.name -eq 'propext'})
  $Aux=@($Data.frontier | Where-Object {$_.evidence -eq 'PINNED_RH_OLEAN'})
  $GraphCandidate=@($Data.frontier | Where-Object {$_.name -eq 'UpperTheory.One.vwin_of_row'})
  if($Data.distinct_original_value_references -ne 378 -or @($Data.frontier).Count -ne 378 -or
     $Counts.LEAN_TOOLCHAIN_ENVIRONMENT -ne 76 -or $Counts.PINNED_RH_OLEAN -ne 2 -or
     $Counts.PUBLISHED_GRAPH_CATALOG -ne 10 -or $Counts.UNCONFIRMED -ne 290 -or
     $Data.transitive_closure -ne 'NOT_RUN' -or $Data.original_proof_kernel_replay -ne 'NOT_RUN' -or
     $Data.claim_authority -ne 'NONE' -or
     $A.Count -ne 1 -or $A[0].kind -ne 'axiom' -or $A[0].module -ne 'Init.Core' -or
     $A[0].evidence -ne 'LEAN_TOOLCHAIN_ENVIRONMENT' -or
     $Aux.Count -ne 2 -or (@($Aux | Where-Object {@($_.value_refs).Count -ne 57})).Count -ne 0 -or
     $GraphCandidate.Count -ne 1 -or $GraphCandidate[0].evidence -ne 'PUBLISHED_GRAPH_CATALOG' -or
     $GraphCandidate[0].axiom_status -ne 'UNCONFIRMED'){
     throw 'Frontier classification invariants failed'
  }
  Write-Output "FRONTIER_REPLAY_ATTEMPT $n PASS evidence=76+2+10+290 propext=Init.Core/AXIOM helper_refs=57/57"
 }
} finally {Pop-Location}
Write-Output 'FRONTIER_LOCAL_VERIFICATION_PASS; FULL_TRANSITIVE_CLOSURE_NOT_RUN; RH_KERNEL_NOT_RUN'
