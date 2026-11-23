$ErrorActionPreference='Stop'
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Pdf=Join-Path $Root 'sources\masullo-2026-11-20\The_Music_of_the_Primes_Masullo_2026-11-20.pdf'
$Info=Get-Command pdfinfo -ErrorAction Stop
Write-Output 'PDF_INFO'
& $Info.Source $Pdf | Select-Object -First 24
$Bin=Split-Path $Info.Source -Parent
Write-Output 'PDF_TOOLS_SAME_DIRECTORY'
Get-ChildItem -LiteralPath $Bin -File -Filter '*pdf*.exe' | Select-Object -ExpandProperty Name
foreach($Name in @('pdftotext.exe','pdftoppm.exe','pdftocairo.exe','mutool.exe')){Write-Output ("EXIST_"+$Name+" "+(Test-Path -LiteralPath (Join-Path $Bin $Name)))}
