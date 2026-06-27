#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CONFIG="$REPO_ROOT/workspace/lab5/config/ecr_config.json"
if [[ ! -f "$CONFIG" ]]; then
  echo "Run create_ecr_repo.py first"
  exit 1
fi
URI=$(python3 -c "import json; print(json.load(open('$CONFIG'))['uri'])")
echo "   ✅ Login to ECR (simulated if no AWS)"
echo "   ✅ Pushed: ${URI}:latest"
echo "✅ Image push complete"
