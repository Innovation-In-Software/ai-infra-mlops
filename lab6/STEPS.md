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

> **Quick run:** `python3 scripts/run_lab6.py` runs all script steps in order.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
cd lab6
```

Run `clear` before each step for clean terminal screenshots.

---

## Step 1 — Confirm lab6 folder

**Do this:**

```bash
clear
cd ~/ai-infra-mlops && ls -1 lab6
```

**Expected result:** `Validate Lab 6`


**Screenshot (optional):** `images/step-01-lab6-folder.png`

---

## Step 2 — Prepare deployment state

**Do this:**

```bash
clear
cd ~/ai-infra-mlops/lab6
pip install -r requirements.txt
python3 scripts/prepare_deployment.py
cat ../workspace/lab6/config/deployment_state.json | head -15
```

**Expected result:**

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


**Screenshot (optional):** `images/step-02-prepare.png`

---

## Step 3 — Configure blue-green plan

**Do this:**

```bash
clear
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
clear
python3 scripts/deploy_staging.py
```

**Expected result:**

```text
✅ Staging endpoint: banking-endpoint-staging-20260628
✅ Staging deployment complete
```


**Screenshot (optional):** `images/step-04-staging.png`

---

## Step 5 — Test staging endpoint

**Do this:**

```bash
clear
python3 scripts/test_deployment.py --environment staging
```

**Expected result:**

```text
🧪 Endpoint Tests (staging)
============================================================
   ✅ Health: PASS
   ✅ Sample transaction latency: 45ms
   ✅ Error rate: 0%
✅ Staging tests passed
```


**Screenshot (optional):** `images/step-05-test-staging.png`

---

## Step 6 — Deploy production (blue-green)

**Do this:**

```bash
clear
python3 scripts/deploy_production.py
```

**Expected result:**

```text
✅ Production endpoint configured
✅ Production deployment complete
```


**Screenshot (optional):** `images/step-06-production.png`

---

## Step 7 — A/B traffic shift simulation

**Do this:**

```bash
clear
python3 scripts/shift_traffic.py --steps 90,50,0
```

**Expected result:**

```text
Step 1: Blue 90% / Green 10%
   Step 2: Blue 50% / Green 50%
   Step 3: Blue 0% / Green 100%
✅ Traffic shift complete (simulated)
```


**Screenshot (optional):** `images/step-07-traffic.png`

---

## Step 8 — Rollback drill

**Do this:**

```bash
clear
python3 scripts/rollback.py --endpoint-name banking-endpoint-prod-demo
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
clear
python3 scripts/generate_deployment_report.py
```

**Expected result:**

```text
✅ Deployment report: config/deployment_report.json
   Status: COMPLIANT
   Zero-downtime: verified (simulation)
```


**Screenshot (optional):** `images/step-09-report.png`

---

## Step 10 — Validate lab6

**Do this:**

```bash
clear
python3 scripts/validate_lab6.py
```

**Expected result:**

```text
Validate Lab 6
============================================================
   ✅ config: deployment_state.json
   ✅ config: blue_green_plan.json
   ✅ config: deployment_report.json
Prerequisites OK — proceed to Lab 7
```


**Screenshot (optional):** `images/step-10-validate.png`

---

## Lab 6 complete → [Lab 7](../lab7/STEPS.md)
