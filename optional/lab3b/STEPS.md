# Lab 3b optional — SageMaker Managed Training (post-course)

| | |
|---|---|
| **Duration** | ~45–60 minutes |
| **Region** | `us-west-2` |
| **Platform** | EC2 · VS Code Remote SSH · bash |
| **Prerequisite** | [Lab 3](../../lab3/STEPS.md) complete (`best_model.pkl`, train CSVs) |
| **Working directory** | `~/ai-infra-mlops/optional/lab3b` |
| **Outputs** | `~/ai-infra-mlops/workspace/optional-lab3b/` |
| **Cost** | SageMaker Processing `ml.t3.medium` (~few minutes of billing) |

> **Optional post-course module.** Main Lab 3 trains on EC2; this lab runs the **same Random Forest** on **SageMaker managed compute** (Processing Job on sandbox accounts).

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
cd ~/ai-infra-mlops/lab3 && python3 scripts/validate_lab3.py
cd ~/ai-infra-mlops/optional/lab3b
python3 -m pip install -r requirements.txt
```

**Expected:** Lab 3 validation passes; packages install without error.

![git pull — `cd ~/ai-infra-mlops && git pull`](images/step-00a-git-pull.png)

![Lab 3 validation — `python3 scripts/validate_lab3.py`](images/step-00b-lab3-validate.png)

---

## Lab 3b roadmap

| Step | What happens on AWS |
|------|---------------------|
| **1** | Upload `X_train.csv` / `y_train.csv` to S3 |
| **2** | Launch SageMaker Processing Job (`ml.t3.medium`) |
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

![Step 1 — `python3 scripts/upload_training_data.py`](images/step-01-upload.png)

---

# Step 2 — Run SageMaker managed job

```bash
python3 scripts/run_training_job.py
```

**Expected:**

```text
🏋️ SageMaker Managed Training (Lab 3b)
============================================================
   Mode: SageMaker Processing Job (ml.t3.medium)
   ...
   Model saved to /opt/ml/processing/output/model.joblib (800 rows)
   ✅ SageMaker job: banking-rf-lab3b-... (processing)
✅ SageMaker managed training complete
```

> **Sandbox accounts:** Training Job quota is often **0** — the script uses a **Processing Job** instead. Console: SageMaker → **Processing** → **Processing jobs**.

If IAM/S3 errors appear:

```bash
python3 scripts/patch_iam_for_sagemaker.py
sleep 10
python3 scripts/run_training_job.py
```

![Step 2 — `python3 scripts/run_training_job.py` (Processing job complete)](images/step-02-processing-job.png)

---

# Step 3 — Validate Lab 3b

```bash
python3 scripts/validate_lab3b.py
```

**Expected:**

```text
Validate Lab 3b (SageMaker managed job)
============================================================
   ✅ Processing job in AWS: banking-rf-lab3b-...
   ✅ Status: Completed
   ✅ Job type: processing
   ✅ Instance: ml.t3.medium

============================================================
Lab 3b OK — SageMaker job visible in AWS console
```

![Step 3 — `python3 scripts/validate_lab3b.py`](images/step-03-validate.png)

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
| `ResourceLimitExceeded` … **training job usage** is **0** | Expected — script uses **Processing Job**; `git pull` for latest `run_training_job.py` |
| `Missing X_train.csv` | Complete Lab 3 Step 4 |
| `s3:ListBucket` / `not authorized` on `sagemaker-us-west-2-*` | Run `python3 scripts/patch_iam_for_sagemaker.py`, wait 10s, retry |
| `TypeError: unexpected keyword argument 'source_dir'` | `git pull` — fixed in `f96958b` |
| Job stuck **InProgress** | Wait up to 10 min; check CloudWatch logs under `/aws/sagemaker/ProcessingJobs` |

---

## Compare with main Lab 3

| | Lab 3 (main) | Lab 3b (this module) |
|---|--------------|----------------------|
| Compute | EC2 CPU | SageMaker Processing `ml.t3.medium` |
| Experiment tracking | Yes (Experiments API) | Processing job + model in S3 |
| Model file | `workspace/lab3/models/best_model.pkl` | `model.joblib` under `experiments/lab3b/` |

---

## Next → [Lab 4b — Real CodePipeline](../lab4b/STEPS.md)
