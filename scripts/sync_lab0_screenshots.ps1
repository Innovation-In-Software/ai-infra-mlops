# One-shot: rename screenshots in course folder and sync to lab0/images/
param(
    [string]$SourceDir = "D:\Current_work\Innovation in Software\MLOps On AWS June 4\screenshots",
    [switch]$Push
)

$repoRoot = Split-Path $PSScriptRoot -Parent
$py = Join-Path $repoRoot "scripts\lab0_screenshot_sync.py"
$args = @($py, "--source", $SourceDir)
if ($Push) { $args += "--push" }
python @args
