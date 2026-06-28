#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CONFIG="$REPO_ROOT/workspace/lab5/config/ecr_config.json"
REGION="${AWS_REGION:-us-west-2}"

if [[ ! -f "$CONFIG" ]]; then
  echo "Run create_ecr_repo.py first"
  exit 1
fi

URI=$(python3 -c "import json; print(json.load(open('$CONFIG'))['uri'])")
ACCOUNT="${URI%%.*}"

aws ecr get-login-password --region "$REGION" \
  | docker login --username AWS --password-stdin "${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com"

docker tag banking-ml-inference:latest "${URI}:latest"
docker push "${URI}:latest"

echo "   ✅ Login to ECR succeeded"
echo "   ✅ Pushed: ${URI}:latest"
echo "✅ Image push complete"
