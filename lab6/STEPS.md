# Lab 6: Model Deployment with Blue-Green

## Class · `ai-mlops-2026-jun30` · **30 min** · **us-west-2**
## Platform · **EC2** + [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) + **bash**
## Prerequisite · [Lab 5](../lab5/STEPS.md) complete
## Working directory · `~/ai-infra-mlops/lab6`
## Outputs · `~/ai-infra-mlops/workspace/lab6/`

> **Classroom mode:** Scripts support `--dry-run` to avoid SageMaker endpoint charges while producing deployment artifacts.

---

# Step 1 — Confirm lab6 folder

```bash
clear
cd ~/ai-infra-mlops && ls -1 lab6
```

**Expected output:** `STEPS.md`, `config`, `images`, `requirements.txt`, `scripts`

**Optional screenshot:** `images/step-01-lab6-folder.png`

---

# Step 2 — Prepare deployment state

```bash
clear
cd ~/ai-infra-mlops/lab6
pip install -r requirements.txt
python3 scripts/prepare_deployment.py
cat ../workspace/lab6/config/deployment_state.json | head -15
```

**Expected output:**

```text
   ✅ Model URI resolved from Lab 5 ECR manifest
   ✅ IAM roles loaded from Lab 1
✅ Deployment state ready
{
  "environment": "staging",
  "model_package": "...",
  ...
}
```

**Optional screenshot:** `images/step-02-prepare.png`

---

# Step 3 — Configure blue-green plan

```bash
clear
python3 scripts/configure_blue_green.py --dry-run
```

**Expected output:**

```text
🔄 Blue-Green Plan
============================================================
   Blue variant: banking-model-blue (100%)
   Green variant: banking-model-green (0%)
   Traffic shift: 90/10 → 50/50 → 0/100
✅ Plan saved: config/blue_green_plan.json
```

**Optional screenshot:** `images/step-03-blue-green.png`

---

# Step 4 — Deploy staging endpoint

```bash
clear
python3 scripts/deploy_staging.py --dry-run
```

**Expected output:**

```text
   ✅ Staging endpoint: banking-endpoint-staging (simulated)
   ✅ Instance type: ml.m5.large
✅ Staging deployment complete (dry-run)
```

**Optional screenshot:** `images/step-04-staging.png`

---

# Step 5 — Test staging endpoint

```bash
clear
python3 scripts/test_deployment.py --dry-run --environment staging
```

**Expected output:**

```text
🧪 Endpoint Tests (staging)
============================================================
   ✅ Health: PASS
   ✅ Sample transaction latency: 45ms
   ✅ Error rate: 0%
✅ Staging tests passed
```

**Optional screenshot:** `images/step-05-test-staging.png`

---

# Step 6 — Deploy production (blue-green)

```bash
clear
python3 scripts/deploy_production.py --dry-run
```

**Expected output:**

```text
   ✅ Production endpoint: banking-endpoint-prod
   ✅ Blue/Green variants configured
   ✅ Auto-scaling policy attached (simulated)
✅ Production deployment complete (dry-run)
```

**Optional screenshot:** `images/step-06-production.png`

---

# Step 7 — A/B traffic shift simulation

```bash
clear
python3 scripts/shift_traffic.py --dry-run --steps 90,50,0
```

**Expected output:**

```text
   Step 1: Blue 90% / Green 10%
   Step 2: Blue 50% / Green 50%
   Step 3: Blue 0% / Green 100%
✅ Traffic shift complete (simulated)
```

**Optional screenshot:** `images/step-07-traffic.png`

---

# Step 8 — Rollback drill

```bash
clear
python3 scripts/rollback.py --endpoint-name banking-endpoint-prod-demo --dry-run
```

**Expected output:**

```text
↩️ Rollback
============================================================
   ✅ Restored previous variant weights
   ✅ Rollback logged for audit
✅ Rollback complete (dry-run)
```

**Optional screenshot:** `images/step-08-rollback.png`

---

# Step 9 — Deployment compliance report

```bash
clear
python3 scripts/generate_deployment_report.py
```

**Expected output:**

```text
✅ Deployment report: config/deployment_report.json
   Status: COMPLIANT
   Zero-downtime: verified (simulation)
```

**Optional screenshot:** `images/step-09-report.png`

---

# Step 10 — Validate lab6

```bash
clear
python3 scripts/validate_lab6.py
```

**Expected output:**

```text
Validate Lab 6
============================================================
   ✅ config: deployment_state.json
   ✅ config: blue_green_plan.json
   ✅ config: deployment_report.json
Prerequisites OK — proceed to Lab 7
```

**Optional screenshot:** `images/step-10-validate.png`

---

## Lab 6 complete → [Lab 7](../lab7/STEPS.md)
