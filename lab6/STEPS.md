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

![Lab 5 validation — `python3 scripts/validate_lab5.py`](images/step-00b-lab5-validate.png)

> **Important:** SageMaker starts your ECR image with `docker run <image> serve`. If you pulled a Lab 5 fix after your first ECR push, rebuild and push before deploying:
>
> ```bash
> cd ~/ai-infra-mlops/lab5
> bash scripts/build_container.sh
> python3 scripts/push_to_ecr.py
> ```

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

![Step 1 — `ls -1 lab6`](images/step-01-lab6-folder.png)

---

## Step 2 — Prepare deployment state

**Do this:**

```bash
cd ~/ai-infra-mlops/lab6
python3 -m pip install -r requirements.txt
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

![Step 2 — `prepare_deployment.py`](images/step-02-prepare.png)

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

![Step 3 — `configure_blue_green.py`](images/step-03-blue-green.png)

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

![Step 4 — `deploy_staging.py`](images/step-04-staging.png)

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

![Step 5 — `test_deployment.py`](images/step-05-test-staging.png)

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

![Step 6 — `deploy_production.py`](images/step-06-production.png)

> **If Step 6 fails with `ResourceLimitExceeded`:** paste the complete fix block in [Troubleshooting — Copy-paste complete fix](#copy-paste--resourcelimitexceeded-on-step-6-complete-fix).

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

**Note:** Each step calls `update_endpoint_weights_and_capacities` on your production endpoint (from Step 6).

![Step 7 — `shift_traffic.py`](images/step-07-traffic.png)

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
   ✅ Restored blue variant to 100%
   ✅ Rollback logged for audit
✅ Rollback complete
```

![Step 8 — `rollback.py`](images/step-08-rollback.png)

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

![Step 9 — `generate_deployment_report.py`](images/step-09-report.png)

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

![Step 10 — `validate_lab6.py`](images/step-10-validate.png)

---

## Troubleshooting

### Copy-paste — ResourceLimitExceeded on Step 6 (complete fix)

**When you see this** after `python3 scripts/deploy_production.py`:

```text
ResourceLimitExceeded: ... 'ml.m5.large for endpoint usage' is 4 Instances,
with current utilization of 3 Instances and a request delta of 2 Instances.
```

**Why:** Production blue-green needs **2** `ml.m5.large` instances (blue + green). Deleting staging only frees **1**. If **3 are already in use**, `3 + 2 = 5` exceeds the limit of **4**. Get down to **2 or fewer** in use before Step 6 (`2 + 2 = 4` fits).

> `ValidationException: Could not find endpoint "banking-endpoint-prod-..."` is **normal** before create — ignore it; fix the quota issue below.

**Paste this whole block** in the VS Code terminal on EC2:

```bash
cd ~/ai-infra-mlops/lab6

echo "=== 1. List SageMaker endpoints ==="
aws sagemaker list-endpoints --region us-west-2 \
  --query 'Endpoints[*].[EndpointName,EndpointStatus]' --output table

echo "=== 2. Delete staging endpoint (frees 1 ml.m5.large) ==="
STAGING=$(python3 -c "import json; print(json.load(open('$HOME/ai-infra-mlops/workspace/lab6/config/staging_deployment.json'))['endpoint'])")
echo "Deleting: $STAGING"
aws sagemaker delete-endpoint --endpoint-name "$STAGING" --region us-west-2

echo "=== 3. Wait for delete (2-3 min), then list again ==="
sleep 150
aws sagemaker list-endpoints --region us-west-2 \
  --query 'Endpoints[*].[EndpointName,EndpointStatus]' --output table

echo "=== 4. Retry production deploy ==="
python3 scripts/deploy_production.py
```

**Still `ResourceLimitExceeded` after the block above?** Delete **one more** endpoint from the table, then retry Step 6 only:

```bash
# Paste an endpoint name from the list above (not a placeholder like YYYYMMDD)
EXTRA="banking-endpoint-paste-name-from-table"
aws sagemaker delete-endpoint --endpoint-name "$EXTRA" --region us-west-2
sleep 150
aws sagemaker list-endpoints --region us-west-2 \
  --query 'Endpoints[*].[EndpointName,EndpointStatus]' --output table
cd ~/ai-infra-mlops/lab6
python3 scripts/deploy_production.py
```

**Quota reference**

| Deployment | `ml.m5.large` instances |
|------------|-------------------------|
| Step 4 staging | **1** |
| Step 6 production (blue-green) | **2** |
| Account limit (typical) | **4** |
| **Free slots needed for Step 6** | **2** (utilization must be ≤ 2) |

**Still blocked?** Ask your instructor to delete unused endpoints in the shared account or request a quota increase: **Service Quotas → Amazon SageMaker → `ml.m5.large for endpoint usage`**.

**Endpoints already exist in AWS but lab scripts failed?** On EC2, sync config and finish Steps 7–10:

```bash
cd ~/ai-infra-mlops && git pull
cd lab6
python3 scripts/repair_lab6_from_aws.py
python3 scripts/validate_lab6.py
```

| Issue | Fix |
|-------|-----|
| Lab 5 validation fails | Complete [Lab 5](../lab5/STEPS.md) Steps 1–10 first |
| `Missing Lab 5 ecr_config.json` | Run Lab 5 Steps 6–7 (ECR create + push) |
| Endpoint `Creating` for many minutes | Normal for `ml.m5.large` — wait up to 15 min |
| `ResourceLimitExceeded` on Step 6 | [Copy-paste fix above](#copy-paste--resourcelimitexceeded-on-step-6) — need **2 free** slots; deleting staging alone is not enough if utilization is still 3 |
| Still quota error after deleting staging | Delete **one more** endpoint — production needs +2 instances; `3 in use + 2 = 5` exceeds limit of 4 |
| `Could not find endpoint "banking-endpoint-staging-YYYYMMDD"` on delete | You copied the placeholder literally — run the `ENDPOINT=$(python3 -c ...)` block above; use the real name from JSON (e.g. `banking-endpoint-staging-202607011643`) |
| `ValidationException: Could not find endpoint` before `ResourceLimitExceeded` | Normal — script checks for endpoint before create; fix the quota issue above |
| `Could not access model` / ECR pull error | Confirm image exists in ECR (`Lab 5` Step 7) and `BankingMLEngineerRole` has ECR read |
| Traffic shift fails | Run Step 6 first; production endpoint must be `InService` |
| `AttributeError: update_endpoint_weights` | `git pull` — script uses `update_endpoint_weights_and_capacities` |
| `CannotStartContainerError` / `docker run <image> serve` | Rebuild Lab 5 image (`bash scripts/build_container.sh`), `python3 scripts/push_to_ecr.py`, then re-run `deploy_staging.py` |

---

## Lab 6 complete → [Lab 7](../lab7/STEPS.md)
