#!/usr/bin/env bash
# Run on EC2 after: cd ~/ai-infra-mlops && git pull
# Captures terminal output per lab step for updating STEPS.md
set -euo pipefail
REPO="${HOME}/ai-infra-mlops"
OUT="${REPO}/docs/terminal-captures"
mkdir -p "$OUT"
export LAB_NUM_RECORDS=1000
export LAB_USE_COMPREHEND=0

run_step() {
  local lab="$1" step="$2"
  shift 2
  local file="${OUT}/lab${lab}-step${step}.txt"
  echo "=== Lab ${lab} Step ${step} ===" | tee "$file"
  echo "\$ $*" | tee -a "$file"
  (cd "$REPO" && eval "$*") >> "$file" 2>&1 || true
  echo "" >> "$file"
}

# Lab 0
run_step 0 2 "python3 --version; git --version; aws --version"
run_step 0 7 "aws sts get-caller-identity; aws configure get region"
run_step 0 11 "cd lab0 && python3 scripts/verify_environment.py"

# Lab 1
run_step 1 3 "aws sts get-caller-identity; aws configure get region"
run_step 1 9 "cd lab1 && python3 scripts/validate_environment.py"

# Lab 2
run_step 2 11 "cd lab2 && python3 scripts/validate_lab2.py"

# Labs 3-10 orchestrators
for n in 3 4 5 6 7 8 9 10; do
  run_step "$n" run "cd lab${n} && python3 scripts/run_lab${n}.py"
  run_step "$n" val "cd lab${n} && python3 scripts/validate_lab${n}.py"
done

echo "Captures written to ${OUT}/"
