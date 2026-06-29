# Lab 6: Blue-Green Deployment

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30 minutes |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | [Lab 5](../lab5/STEPS.md) |
| **Working directory** | `~/ai-infra-mlops/lab6` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab6/` |

> All commands run in the **VS Code integrated terminal** on EC2. Do not use local Windows PowerShell for lab steps.

> **Quick run:** `python3 scripts/run_lab6.py` runs all script steps in order (same as Steps 3–8).

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
whoami   # must be ec2-user
cd ~/ai-infra-mlops/lab5 && python3 scripts/validate_lab5.py
cd ~/ai-infra-mlops/lab6
```

**Expected:** `Prerequisites OK — proceed to Lab 6` from Lab 5 validation.

> **Time:** Staging + production SageMaker endpoints each take **~5–10 minutes** (`ml.m5.large`). Plan ~45 minutes for Lab 6 if you run every step.

---

## Step 1 — Confirm lab6 folder

**Do this:**

```bash
cd ~/ai-infra-mlops && ls -1 lab6
```

**Expected result:**

```text
STEPS.md
config
images
requirements.txt
scripts
```

**Screenshot (optional):** `images/step-01-lab6-folder.png`

---

## Step 2 — Prepare deployment state

**Do this:**

```bash
cd ~/ai-infra-mlops/lab6
pip install -r requirements.txt
python3 scripts/prepare_deployment.py
cat ../workspace/lab6/config/deployment_state.json | head -15
```

**Expected result:**

```text
Preparing deployment configuration
============================================================
   ✅ Model artifact found in Lab 3 workspace
   ✅ IAM role: arn:aws:iam::<account-id>:role/BankingMLEngineerRole
   ✅ Image URI: <account-id>.dkr.ecr.us-west-2.amazonaws.com/banking-ml-inference:latest
✅ Deployment state ready
```

**Screenshot (optional):** `images/step-02-prepare.png`

---

## Step 3 — Configure blue-green plan

**Do this:**

```bash
python3 scripts/configure_blue_green.py
```

**Expected result:**

```text
🔄 Blue-Green Plan
============================================================
   Blue variant: banking-model-blue (100%)
   Green variant: banking-model-green (0%)
✅ Plan saved: config/blue_green_plan.json
```

**Screenshot (optional):** `images/step-03-blue-green.png`

---

## Step 4 — Deploy staging endpoint

**Do this:**

```bash
python3 scripts/deploy_staging.py
```

**Expected result:**

```text
   ✅ Creating endpoint: banking-endpoint-staging-YYYYMMDD (typically 5–10 min)
   ... endpoint banking-endpoint-staging-YYYYMMDD status: Creating
   ... endpoint banking-endpoint-staging-YYYYMMDD status: InService
   ✅ Staging endpoint: banking-endpoint-staging-YYYYMMDD
✅ Staging deployment complete
```

**Screenshot (optional):** `images/step-04-staging.png`

---

## Step 5 — Test staging endpoint

**Do this:**

```bash
python3 scripts/test_deployment.py --environment staging
```

**Expected result:**

```text
🧪 Endpoint Tests (staging)
============================================================
   ... waiting for /ping (model load may take up to 60s)
   ... sample inference with 30 features (matches Lab 3 model)
   ✅ Health: PASS
   ✅ Sample transaction latency: <N>ms
   ✅ Error rate: 0%
✅ Staging tests passed
```

**Screenshot (optional):** `images/step-05-test-staging.png`

---

## Step 6 — Deploy production (blue-green)

**Do this:**

```bash
python3 scripts/deploy_production.py
```

**Expected result:**

```text
   ✅ Creating production endpoint: banking-endpoint-prod-YYYYMMDD
   ... endpoint status: InService
   ✅ Production endpoint: banking-endpoint-prod-YYYYMMDD
✅ Production deployment complete
```

**Screenshot (optional):** `images/step-06-production.png`

---

## Step 7 — A/B traffic shift (SageMaker)

**Do this:**

```bash
python3 scripts/shift_traffic.py --steps 90,50,0
```

**Expected result:**

```text
   Step 1: Blue 90% / Green 10%
   Step 2: Blue 50% / Green 50%
   Step 3: Blue 0% / Green 100%
✅ Traffic shift complete
```

**Note:** Each step calls `update_endpoint_weights` on your production endpoint (from Step 6).

**Screenshot (optional):** `images/step-07-traffic.png`

---

## Step 8 — Rollback drill

**Do this:**

```bash
python3 scripts/rollback.py
```

**Expected result:**

```text
↩️ Rollback
============================================================
   ✅ Restored previous variant weights
   ✅ Rollback logged for audit
✅ Rollback complete
```

**Screenshot (optional):** `images/step-08-rollback.png`

---

## Step 9 — Deployment compliance report

**Do this:**

```bash
python3 scripts/generate_deployment_report.py
```

**Expected result:**

```text
✅ Deployment report: config/deployment_report.json
   Status: COMPLIANT
   Zero-downtime staging+prod: True
```

**Screenshot (optional):** `images/step-09-report.png`

---

## Step 10 — Validate lab6

**Do this:**

```bash
python3 scripts/validate_lab6.py
```

**Expected result:**

```text
Validate Lab 6
============================================================
   ✅ config: deployment_state.json
   ✅ config: blue_green_plan.json
   ✅ config: staging_deployment.json
   ✅ config: test_staging.json
   ✅ config: production_deployment.json
   ✅ config: deployment_report.json

============================================================
Prerequisites OK — proceed to Lab 7
```

**Screenshot (optional):** `images/step-10-validate.png`

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Lab 5 validation fails | Complete [Lab 5](../lab5/STEPS.md) Steps 1–10 first |
| `Missing Lab 5 ecr_config.json` | Run Lab 5 Steps 6–7 (ECR create + push) |
| Endpoint `Creating` for many minutes | Normal for `ml.m5.large` — wait up to 15 min |
| `ResourceLimitExceeded` / instance quota | Check Service Quotas → SageMaker → endpoint instances; try later or ask instructor |
| `Could not access model` / ECR pull error | Confirm image exists in ECR (`Lab 5` Step 7) and `BankingMLEngineerRole` has ECR read |
| Traffic shift fails | Run Step 6 first; production endpoint must be `InService` |

---

## Lab 6 complete → [Lab 7](../lab7/STEPS.md)
