# Preserve Masullo source PDF at the original Vakil source URL.
$ErrorActionPreference='Stop'
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Folder=Join-Path $Root 'sources\masullo-2026-11-20'
New-Item -ItemType Directory -Force -Path $Folder | Out-Null
$File=Join-Path $Folder 'The_Music_of_the_Primes_Masullo_2026-11-20.pdf'
$Temp=$File+'.partial'
$Url='https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf'
if((Test-Path -LiteralPath $File) -or (Test-Path -LiteralPath $Temp)){throw 'Refusing to overwrite an existing download or partial'}
try {
  Invoke-WebRequest -Uri $Url -OutFile $Temp -TimeoutSec 90 -MaximumRedirection 3 -ErrorAction Stop
  $Length=(Get-Item -LiteralPath $Temp).Length
  if($Length -le 1000000 -or $Length -ge 150MB){throw "PDF length out of range: $Length"}
  $Stream=[IO.File]::OpenRead($Temp)
  try { $Header=New-Object byte[] 5; [void]$Stream.Read($Header,0,5) } finally {$Stream.Dispose()}
  if([Text.Encoding]::ASCII.GetString($Header) -ne '%PDF-'){throw 'Not a PDF by signature'}
  Move-Item -LiteralPath $Temp -Destination $File
  Write-Output 'PDF_DOWNLOADED'
  Write-Output "BYTES $Length"
  Write-Output ("SHA256 "+(Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash.ToLowerInvariant())
} catch {
  Write-Output ("DOWNLOAD_ERROR "+$_.Exception.Message)
  throw
}
