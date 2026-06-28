#!/usr/bin/env bash
# Run before git push — fails if likely secrets are staged
set -euo pipefail
PATTERNS='AKIA[0-9A-Z]{16}|aws_secret_access_key\s*=\s*[^Y]|Secret Access Key:\s*[A-Za-z0-9+/]{20,}'
if git diff --cached -G"$PATTERNS" --name-only | grep -q .; then
  echo "ERROR: Staged changes may contain AWS credentials. Unstage and remove secrets."
  git diff --cached -G"$PATTERNS" --name-only
  exit 1
fi
echo "OK: no credential patterns in staged files."
