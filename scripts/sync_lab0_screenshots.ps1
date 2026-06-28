# Sync Lab 0 screenshots from course screenshots folder into lab0/images/
param(
    [string]$SourceDir = "D:\Current_work\Innovation in Software\MLOps On AWS June 4\screenshots",
    [string]$RepoRoot = (Split-Path $PSScriptRoot -Parent)
)

$dst = Join-Path $RepoRoot "lab0\images"
New-Item -ItemType Directory -Force -Path $dst | Out-Null

# Raw capture -> lab0/images filename (skip 003036 — contains handout passwords)
$renameMap = [ordered]@{
    "Screenshot 2026-06-28 003154.png" = "step-01-protech-portal.png"
    "Screenshot 2026-06-28 005210.png" = "step-04a-aws-signin-url.png"
    "Screenshot 2026-06-28 005344.png" = "step-04b-aws-signin-form.png"
    "Screenshot 2026-06-28 005425.png" = "step-05-aws-signin-filled.png"
    "Screenshot 2026-06-28 005432.png" = "step-05-console-home.png"
    "Screenshot 2026-06-28 005441.png" = "step-06a-region-us-west-2.png"
    "Screenshot 2026-06-28 120041.png" = "step-06b-ec2-search.png"
    "Screenshot 2026-06-28 115127.png" = "step-06c-ec2-dashboard.png"
    "Screenshot 2026-06-28 120205.png" = "step-07a-key-pairs-empty.png"
    "Screenshot 2026-06-28 120231.png" = "step-07b-create-key-pair.png"
    "Screenshot 2026-06-28 120242.png" = "step-07c-create-key-pair-options.png"
    "Screenshot 2026-06-28 120257.png" = "step-07d-key-pair-success.png"
    "Screenshot 2026-06-28 120312.png" = "step-07e-pem-in-downloads.png"
    "Screenshot 2026-06-28 120318.png" = "step-07f-pem-move-to-ssh.png"
    "Screenshot 2026-06-28 120330.png" = "step-07g-pem-in-ssh-folder.png"
    "Screenshot 2026-06-28 120403.png" = "step-07h-key-pair-listed.png"
    "Screenshot 2026-06-28 120411.png" = "step-08a-security-groups-default.png"
    "Screenshot 2026-06-28 120443.png" = "step-08b-create-sg-basic.png"
    "Screenshot 2026-06-28 120559.png" = "step-08c-create-sg-inbound-empty.png"
    "Screenshot 2026-06-28 120607.png" = "step-08d-create-sg-ssh-rule.png"
}

$copied = 0
foreach ($entry in $renameMap.GetEnumerator()) {
    $from = Join-Path $SourceDir $entry.Key
    if (-not (Test-Path $from)) {
        Write-Warning "Missing: $($entry.Key)"
        continue
    }
    $to = Join-Path $dst $entry.Value
    Copy-Item $from $to -Force
    Write-Host "OK $($entry.Value)"
    $copied++
}

Write-Host "`nSynced $copied screenshot(s) to $dst"
