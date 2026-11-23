# Fail-closed guard. Retained solely to preserve the attempted checker boundary.
# Do NOT launch leanchecker in this runtime without a separate resource-limited,
# version-matched invocation contract and proof of module resolution.
$ErrorActionPreference = 'Stop'
Write-Output 'BLOCKED[LEANCHECKER_RESOURCE_AND_MODULE_RESOLUTION]'
Write-Output 'Observed: leanchecker --help -> INTERNAL PANIC: out of memory.'
Write-Output 'Observed: absolute-path synthetic .olean -> Could not resolve module.'
Write-Output 'The original RH Main.olean has NOT received independent kernel replay.'
Write-Output 'This script deliberately does not launch leanchecker again.'
exit 2
