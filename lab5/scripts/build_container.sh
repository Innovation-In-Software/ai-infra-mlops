#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."
echo "🔨 Building banking-ml-inference:latest"
docker build -f lab5/Dockerfile -t banking-ml-inference:latest .
echo "✅ Container build complete"
