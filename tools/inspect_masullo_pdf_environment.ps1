$ErrorActionPreference='Stop'
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Pdf=Join-Path $Root 'sources\masullo-2026-11-20\The_Music_of_the_Primes_Masullo_2026-11-20.pdf'
Write-Output ('PDF_EXISTS '+(Test-Path -LiteralPath $Pdf))
if(Test-Path -LiteralPath $Pdf){Write-Output ('PDF_SHA256 '+(Get-FileHash -LiteralPath $Pdf -Algorithm SHA256).Hash.ToLowerInvariant())}
foreach($prog in @('pdfinfo','pdftotext','mutool','gswin64c')) { $c=Get-Command $prog -ErrorAction SilentlyContinue; if($null -ne $c){Write-Output ('CMD_'+$prog+' '+$c.Source)} }
$Uv=Get-Command uv -ErrorAction SilentlyContinue
if($null -ne $Uv){
 $py=((& $Uv.Source python find --offline 3.14)|Select-Object -First 1).Trim()
 Write-Output ('PYTHON '+$py)
 & $py -c "import importlib.util; print('PDF_MODULES '+repr({x:bool(importlib.util.find_spec(x)) for x in ('fitz','pymupdf','pypdf','PyPDF2','pypdfium2','pdfplumber')}))"
}
