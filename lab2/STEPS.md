# Lab 2: Banking Data Management & PII Protection

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30 minutes (Step 8 Feature Store wait up to 10 min) |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | [Lab 1](../lab1/STEPS.md) complete — validation **13/13 COMPLIANT** |
| **Working directory** | `~/ai-infra-mlops/lab2` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab2/` |

> **Run Steps 1–11 once, in order.** Steps 4–8 build on each other; Step 8 calls AWS SageMaker Feature Store.  
> All commands run in the **VS Code terminal on EC2** (`whoami` = `ec2-user`). Do not use Windows PowerShell on the ProTech VM.

---

## Before you start

1. Connect VS Code to EC2 ([Lab 0 Step 13](../lab0/STEPS.md)).
2. Pull the latest course repo:

```bash
cd ~/ai-infra-mlops && git pull
whoami
```

**Expected:** `ec2-user`

![git pull on EC2 before Lab 2](images/step-00a-git-pull.png)

3. Confirm Lab 1 still passes:

```bash
cd ~/ai-infra-mlops/lab1 && python3 scripts/validate_environment.py
```

**Expected:** `Compliance Score: 100.0%` and `✅ ALL CHECKS PASSED!`

![Lab 1 validation 13/13 COMPLIANT](images/step-00b-lab1-validate.png)

4. Set classroom variables (once per terminal session — speeds up the lab, skips Comprehend API calls):

```bash
export LAB_NUM_RECORDS=1000
export LAB_USE_COMPREHEND=0
cd ~/ai-infra-mlops/lab2
```

---

## Lab 2 roadmap

| Step | What you create |
|------|-----------------|
| **1–3** | Confirm repo, workspace, and Lab 1 prerequisites |
| **4** | Synthetic banking dataset (customers + transactions) |
| **5** | PII detection and anonymization |
| **6** | Data quality validation reports |
| **7** | Engineered ML features + preprocessor pipeline |
| **8** | SageMaker Feature Store groups + ingest (**longest — up to 10 min wait**) |
| **9** | Data drift baseline and monitoring |
| **10** | Compliance documentation |
| **11** | Final validation |

---

# Step 1 — Confirm lab2 in repo

**What you do:** Verify the Lab 2 course files are in the repo.

```bash
cd ~/ai-infra-mlops
ls -1 lab2
```

**Expected:**

```text
STEPS.md
config
images
requirements.txt
scripts
```

![Lab 2 folder listing](images/step-01-lab2-folder.png)

---

# Step 2 — Confirm workspace

**What you do:** Verify Lab 0 created your Lab 2 output folders under `workspace/`.

```bash
cd ~/ai-infra-mlops/lab2
ls -1 ../workspace/lab2
```

**Expected:**

```text
config
data
logs
results
scripts
```

If the folder is missing, re-run [Lab 0 Step 16](../lab0/STEPS.md) (`setup_lab_directories.py`), then return here.

![Lab 2 workspace folders](images/step-02-workspace-lab2.png)

---

# Step 3 — Verify Lab 1 prerequisites

**What you do:** Confirm Lab 1 config files exist and Lab 2 is ready to run.

```bash
cd ~/ai-infra-mlops/lab2
python3 scripts/validate_lab2.py
```

**Expected (before Steps 4–10):**

```text
Validate Lab 2
============================================================
   ✅ Lab 1 config: buckets.json
   ✅ Lab 1 config: iam_roles.json
   ⚠️ not yet created: customers.csv
   ...
Prerequisites OK — run lab2 scripts in STEPS.md order.
```

If you see `❌ Missing Lab 1 config`, complete [Lab 1](../lab1/STEPS.md) first.

![Lab 2 prerequisites check](images/step-03-prerequisites.png)

---

# Step 4 — Generate banking dataset

**What you do:** Create synthetic customer and transaction CSV files with embedded PII fields.

```bash
python3 scripts/download_banking_data.py
```

**Expected:**

```text
🏦 Generating Banking Transaction Dataset
   Records: 1000 (set LAB_NUM_RECORDS to change)

📊 Generating Transaction Records...
✅ Generated 100 customer records
✅ Generated 1000 transaction records
✅ Dataset metadata saved
```

![Banking dataset generated](images/step-04-dataset.png)

---

# Step 5 — PII detection & anonymization

**What you do:** Scan for PII using pattern matching (classroom mode) and write anonymized CSV files.

```bash
python3 scripts/pii_detection_anonymization.py
```

**Expected:**

```text
🏦 Processing Banking Data with PII Protection
   Detection mode: patterns only (classroom mode)
...
✅ PII Detection and Anonymization Complete!
   Total PII Instances Anonymized: 3700
✅ Banking Data Processing Complete!
   Total PII Anonymized: 3700
```

The script also uploads a PII compliance report to your Lab 1 **governance** S3 bucket.

![PII anonymization complete — 3700 instances](images/step-05-pii.png)

---

# Step 6 — Data validation

**What you do:** Run banking compliance checks on the anonymized data.

```bash
python3 scripts/data_validation.py
```

**Expected:**

```text
✅ Data Validation Complete!
   Customer Quality Score: 57.1%
   Transaction Quality Score: 70.0%
```

`REVIEW_REQUIRED` on customers is **expected** in classroom mode (anonymized fields fail strict type/pattern checks). Scores above 50% confirm the pipeline ran correctly.

![Data validation quality scores](images/step-06-validation.png)

---

# Step 7 — Feature engineering

**What you do:** Build ML features from anonymized data and save a sklearn preprocessor pipeline.

```bash
python3 scripts/feature_engineering.py
```

**Expected:**

```text
✅ Feature Engineering Complete!
   Training Data: .../data/engineered_banking_data.csv
   Feature Pipeline: .../config/preprocessor.pkl
   Feature Metadata: .../config/feature_metadata.json
```

![Feature engineering — 52 features](images/step-07-features.png)

---

# Step 8 — SageMaker Feature Store

**What you do:** Create two Feature Store groups and ingest engineered features. This step calls AWS and may take **5–10 minutes** on first run.

```bash
python3 scripts/feature_store_setup.py
```

**Expected:**

```text
🏦 Setting Up Banking Feature Store
   ✅ Feature group created: banking-transaction-features
   ⏳ Waiting for banking-transaction-features to become active...
   ✅ Feature group active: banking-transaction-features
   ...
   ✅ Ingested 1000 records into banking-transaction-features
   ✅ Ingested 100 records into banking-customer-features
✅ Feature Store Setup Complete!
```

On re-run, you may see `Feature group already exists` or ingest warnings — that is OK if Step 11 passes.

![Feature Store ingest complete](images/step-08-feature-store.png)

---

# Step 9 — Drift detection

**What you do:** Compare baseline vs. simulated current data and save a drift report.

```bash
python3 scripts/data_drift_detection.py
```

**Expected:**

```text
📊 Drift Detection Summary:
   Total Features: 50
   Features with Drift: 0
   Drift Percentage: 0.0%
   Status: NORMAL
✅ Drift Detection Complete!
```

A CloudWatch alarm warning (`SNS topic may not exist`) is **expected** — the alarm is optional in this lab.

![Drift detection — 0% drift NORMAL](images/step-09-drift.png)

---

# Step 10 — Compliance report

**What you do:** Aggregate all Lab 2 reports into a final compliance document.

```bash
python3 scripts/generate_compliance_doc.py
```

**Expected:**

```text
📋 COMPLIANCE REPORT SUMMARY
============================================================
✅ PII Protection: 3700 instances anonymized
✅ Data Quality Score: 57.1%
✅ Features Managed: 52
✅ Drift Monitoring: NORMAL
```

![Compliance report summary](images/step-10-compliance.png)

---

# Step 11 — Final validation

**What you do:** Confirm all Lab 2 outputs exist.

```bash
python3 scripts/validate_lab2.py
ls -1 ../workspace/lab2/data
ls -1 ../workspace/lab2/config
```

**Expected:**

```text
Validate Lab 2
============================================================
   ✅ Lab 1 config: buckets.json
   ✅ Lab 1 config: iam_roles.json
   ✅ data: customers.csv
   ✅ data: transactions.csv
   ✅ data: anonymized_customers.csv
   ✅ data: anonymized_transactions.csv
   ✅ data: engineered_banking_data.csv
   ✅ data: compliance_report_final.json
   ✅ config: dataset_metadata.json
   ✅ config: pii_report.json
   ✅ config: pii_compliance_report.json
   ✅ config: feature_metadata.json
   ✅ config: feature_store_config.json
   ✅ config: drift_report.json
   ✅ config: data_quality_report_customers.json
   ✅ config: data_quality_report_transactions.json

============================================================
Prerequisites OK — run lab2 scripts in STEPS.md order.
```

You should also see `preprocessor.pkl` under `config/` from Step 7.

![Final validation — all checks green](images/step-11a-validate.png)

![Lab 2 data and config files](images/step-11b-validate-files.png)

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `whoami` = `Administrator` | Reconnect VS Code Remote-SSH to EC2 ([Lab 0 Step 13](../lab0/STEPS.md)) |
| `❌ Missing Lab 1 config` | Complete [Lab 1](../lab1/STEPS.md) Steps 4–9 first |
| `No such file: customers.csv` | Run Step 4 before Steps 5–11 |
| `No such file: engineered_banking_data.csv` | Run Step 7 before Step 8 |
| `No such file: buckets.json` / `iam_roles.json` | Re-run Lab 1 Steps 5–6 |
| Feature Store timeout | Wait 5 min, run Step 8 **once more** (groups may already exist) |
| Ingest error / already ingested | OK on re-run if record counts match in Step 11 |
| `ModuleNotFoundError` (pandas, sagemaker, etc.) | [Lab 0 Step 18](../lab0/STEPS.md) — `pip install -r lab2/requirements.txt` |
| `PythonDeprecationWarning` | [Lab 0 Step 17a](../lab0/STEPS.md) — upgrade to Python 3.11 |

---

## Appendix — Fresh start (optional)

Use only when re-testing Lab 2 from scratch.

**Workspace only** (keeps SageMaker Feature Groups in AWS):

```bash
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab2
cd lab2
```

Then re-run **Steps 4–11**.

**Full Lab 2 reset** (also deletes Feature Store groups in AWS):

```bash
cd ~/ai-infra-mlops/lab2
python3 scripts/cleanup_lab2.py --aws
```

Then re-run **Steps 4–11**. Feature groups are recreated in Step 8.

---

## Lab 2 complete → [Lab 3](../lab3/STEPS.md)
