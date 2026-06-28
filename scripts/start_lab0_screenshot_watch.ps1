# Watch course screenshots folder every 2 minutes: rename + sync + push.
param(
    [int]$IntervalSeconds = 120,
    [string]$SourceDir = "D:\Current_work\Innovation in Software\MLOps On AWS June 4\screenshots",
    [string]$RepoRoot = (Split-Path $PSScriptRoot -Parent),
    [switch]$NoPush
)

$syncScript = Join-Path $RepoRoot "scripts\lab0_screenshot_sync.py"
$logDir = Join-Path $RepoRoot "lab0\logs"
$logFile = Join-Path $logDir "screenshot_watch.log"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$pushFlag = if ($NoPush) { "" } else { "--push" }

Write-Host "Lab 0 screenshot watch — every $IntervalSeconds s"
Write-Host "  Source: $SourceDir"
Write-Host "  Repo:   $RepoRoot"
Write-Host "  Log:    $logFile"
Write-Host "  Stop:   Ctrl+C in this window"
Write-Host ""

while ($true) {
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logFile -Value "`n=== $stamp ==="
    $args = @($syncScript, "--source", $SourceDir)
    if ($pushFlag) { $args += $pushFlag }
    & python @args 2>&1 | Tee-Object -FilePath $logFile -Append
    Start-Sleep -Seconds $IntervalSeconds
}
