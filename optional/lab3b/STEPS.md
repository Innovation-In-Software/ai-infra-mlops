# Lab 3b optional — SageMaker Training Job (post-course)

| | |
|---|---|
| **Duration** | ~45–60 minutes |
| **Region** | `us-west-2` |
| **Platform** | EC2 · VS Code Remote SSH · bash |
| **Prerequisite** | [Lab 3](../../lab3/STEPS.md) complete (`best_model.pkl`, train CSVs) |
| **Working directory** | `~/ai-infra-mlops/optional/lab3b` |
| **Outputs** | `~/ai-infra-mlops/workspace/optional-lab3b/` |
| **Cost** | SageMaker `ml.m5.large` (~few minutes of billing) |

> **Optional post-course module.** Main Lab 3 trains on EC2; this lab runs the **same Random Forest** on **SageMaker managed training**.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
cd ~/ai-infra-mlops/lab3 && python3 scripts/validate_lab3.py
cd ~/ai-infra-mlops/optional/lab3b
python3 -m pip install -r requirements.txt
```

**Expected:** Lab 3 validation passes; packages install without error.

---

## Lab 3b roadmap

| Step | What happens on AWS |
|------|---------------------|
| **1** | Upload `X_train.csv` / `y_train.csv` to S3 |
| **2** | Launch SageMaker Training Job (`ml.m5.large`) |
| **3** | Validate job status in API + console |
| **4** | Optional cleanup notes |

---

# Step 1 — Upload training data to S3

```bash
python3 scripts/upload_training_data.py
```

**Expected:**

```text
📤 Upload training data for SageMaker
============================================================
   ✅ Uploaded: s3://bank-mlops-<account-id>-processed/training/sagemaker-lab3b/X_train.csv
   ✅ Uploaded: s3://bank-mlops-<account-id>-processed/training/sagemaker-lab3b/y_train.csv
✅ Training data ready in S3
```

Verify in S3 console: **processed** bucket → `training/sagemaker-lab3b/`.

---

# Step 2 — Run SageMaker managed job

```bash
python3 scripts/run_training_job.py
```

**Expected:**

```text
🏋️ SageMaker Managed Training (Lab 3b)
============================================================
   Role: arn:aws:iam::<account-id>:role/BankingDataScientistRole
   Input: s3://bank-mlops-<account-id>-processed/training/sagemaker-lab3b/
   Output: s3://bank-mlops-<account-id>-models/experiments/lab3b/
   Mode: SageMaker Processing Job (ml.t3.medium)
   Note: Training Job quota is 0 on many sandbox accounts — Processing is equivalent managed compute.

   ⏳ Starting SageMaker job (typically 3–8 minutes)...
   ✅ SageMaker job: banking-rf-lab3b-... (processing)
   ✅ Output: s3://bank-mlops-<account-id>-models/experiments/lab3b/...
✅ SageMaker managed training complete
```

> **Sandbox accounts:** AWS often sets **Training Job quota to 0**. This lab uses a **Processing Job** on `ml.t3.medium` instead — still SageMaker-managed EC2 in AWS.  
> Console: SageMaker → **Processing** → **Processing jobs** (not Training jobs).

Optional — force classic Training Job (only if your account has quota):

```bash
LAB3B_USE_TRAINING=1 python3 scripts/run_training_job.py
```

If IAM logs errors appear, re-apply Lab 1 roles once:

```bash
python3 scripts/patch_iam_for_sagemaker.py
```

---

# Step 3 — Validate Lab 3b

```bash
python3 scripts/validate_lab3b.py
```

**Expected:**

```text
Validate Lab 3b (SageMaker Training Job)
============================================================
   ✅ Training job in AWS: banking-rf-lab3b-...
   ✅ Status: Completed
   ✅ Model artifact: s3://...

============================================================
Lab 3b OK — training job visible in SageMaker console
```

---

# Step 4 — Cleanup (optional)

```bash
python3 scripts/teardown_lab3b.py
```

Removes nothing automatically — documents where artifacts live. Delete S3 objects under `experiments/lab3b/` if you want to reduce storage cost.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ResourceLimitExceeded` … **training job usage** is **0** | Expected on sandbox accounts — script uses **Processing Job** automatically; `git pull` for latest `run_training_job.py` |
| `Missing X_train.csv` | Complete Lab 3 Step 4 |
| `AccessDenied` on processing/training | Run `python3 scripts/patch_iam_for_sagemaker.py` (adds CloudWatch Logs to Data Scientist role) |
| Job stuck **InProgress** | Wait up to 10 min; check CloudWatch logs under `/aws/sagemaker/ProcessingJobs` |
| `ResourceLimitExceeded` on processing too | Request quota increase in Service Quotas → SageMaker → processing job usage |

---

## Compare with main Lab 3

| | Lab 3 (main) | Lab 3b (this module) |
|---|--------------|----------------------|
| Compute | EC2 CPU | SageMaker `ml.m5.large` |
| Experiment tracking | Yes (Experiments API) | Training job + artifact in S3 |
| Model file | `workspace/lab3/models/best_model.pkl` | `model.tar.gz` in models bucket |

---

## Next → [Lab 4b — Real CodePipeline](../lab4b/STEPS.md)
