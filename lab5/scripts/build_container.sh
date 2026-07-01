#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

if docker ps >/dev/null 2>&1; then
  DOCKER=(docker)
elif sudo docker ps >/dev/null 2>&1; then
  echo "   ℹ️  Using sudo for Docker (fix: Lab 0 Step 17 usermod -aG docker, then reconnect SSH)"
  DOCKER=(sudo docker)
else
  echo "   ❌ Docker not available — complete Lab 0 Step 17."
  exit 1
fi

echo "🔨 Building banking-ml-inference:latest"
"${DOCKER[@]}" build -f lab5/Dockerfile -t banking-ml-inference:latest .
echo "✅ Container build complete"
