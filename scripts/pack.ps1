# Builds release .skill zips from skill folders (assets, NOT committed).
# Each zip bundles shared/ste-limits.json inside the skill so packed installs
# keep verified:true instead of falling back to built-in defaults.
# Usage: powershell -ExecutionPolicy Bypass -File scripts/pack.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$dist = Join-Path $root "dist"
New-Item -ItemType Directory -Path $dist -Force | Out-Null
$skills = @("ste-explain", "diagram-first", "explorable-html", "storyboard-video", "verify-ladder", "understanding-ladder")
foreach ($s in $skills) {
  $stage = Join-Path ([System.IO.Path]::GetTempPath()) ("pack-" + $s)
  if (Test-Path $stage) { Remove-Item -Recurse -Force $stage }
  Copy-Item -Recurse (Join-Path $root ("skills/" + $s)) $stage
  $sharedDst = Join-Path $stage "shared"
  New-Item -ItemType Directory -Path $sharedDst -Force | Out-Null
  Copy-Item (Join-Path $root "skills/shared/ste-limits.json") $sharedDst
  Get-ChildItem -Recurse -Path $stage -Filter "__pycache__" -Directory | Remove-Item -Recurse -Force
  $out = Join-Path $dist ($s + ".skill")
  $zip = Join-Path $dist ($s + ".zip")
  if (Test-Path $out) { Remove-Item -Force $out }
  if (Test-Path $zip) { Remove-Item -Force $zip }
  Compress-Archive -Path ($stage + "/*") -DestinationPath $zip
  Rename-Item -LiteralPath $zip -NewName ($s + ".skill")
  Write-Output "$s -> $out"
}
