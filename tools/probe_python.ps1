$ErrorActionPreference='Stop'
Write-Output ('USERPROFILE: ' + $env:USERPROFILE)
Write-Output ('LOCALAPPDATA: ' + $env:LOCALAPPDATA)
foreach($name in @('py','python','python3','uv','conda','pixi')) {
 $c=Get-Command $name -ErrorAction SilentlyContinue
 if($null -ne $c){Write-Output ("CMD "+$name+" = "+$c.Source)}
}
$Uv = Get-Command uv -ErrorAction SilentlyContinue
if($null -ne $Uv) {
  Write-Output 'UV_OFFLINE_PYTHON_FIND'
  & $Uv.Source python find --offline
  Write-Output ('UV_FIND_EXIT ' + $LASTEXITCODE)
  Write-Output 'UV_ONLY_INSTALLED'
  & $Uv.Source python list --only-installed
  Write-Output ('UV_LIST_EXIT ' + $LASTEXITCODE)
}
foreach($folder in @("$env:LOCALAPPDATA\Programs\Python", "$env:USERPROFILE\miniconda3", "$env:USERPROFILE\anaconda3", "$env:USERPROFILE\.local\share\uv\python", "C:\Program Files\Python314", "C:\Python314", "$env:USERPROFILE\.pyenv\pyenv-win\versions")) {
 if(Test-Path -LiteralPath $folder -PathType Container){
   Write-Output "FOLDER $folder"
   Get-ChildItem -LiteralPath $folder -Force -ErrorAction SilentlyContinue | Select-Object -First 12 -ExpandProperty Name | ForEach-Object { Write-Output " ITEM $_" }
 }
}
