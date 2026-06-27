# Lab 2: Banking Data Management & PII Protection

## Folder · `lab2/`

## Class · `ai-mlops-2026-jun30`
## Duration · 30 minutes
## Region · `us-west-2`
## Repo · [github.com/gjkaur/ai-infra-mlops](https://github.com/gjkaur/ai-infra-mlops)
## Editor · VS Code (Remote SSH to EC2)
## Terminal · bash on EC2
## Delivery · See [CLOUD-DELIVERY.md](../CLOUD-DELIVERY.md)
## Prerequisite · [Lab 1](../lab1/STEPS.md) complete (`Compliance Score: 100%`)

---

# Fresh start (repeat Lab 2)

```bash
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab2
cd lab2
python3 scripts/cleanup_lab2.py --aws    # delete Feature Groups if re-running Step 8
```

Then run Steps 4–11 below.

---

# 30-minute pacing

| Minutes | Step |
|---------|------|
| 0–3 | Steps 1–3 |
| 3–5 | Step 4 — generate data (1000 rows default) |
| 5–10 | Step 5 — PII (`LAB_USE_COMPREHEND=0` in class) |
| 10–15 | Steps 6–7 — validation + features |
| 15–25 | Step 8 — Feature Store |
| 25–30 | Steps 9–11 |

**Classroom env (on EC2 AMI):**

```bash
export LAB_NUM_RECORDS=1000
export LAB_USE_COMPREHEND=0
```

Set `LAB_USE_COMPREHEND=1` only for deep testing (adds significant time).

---

# Terms (full forms)

| Short | Full form |
|-------|-----------|
| **VS Code** | Visual Studio Code |
| **AWS** | Amazon Web Services |
| **PII** | Personally Identifiable Information |
| **GDPR** | General Data Protection Regulation |
| **S3** | Simple Storage Service |
| **Comprehend** | Amazon Comprehend (NLP and PII detection service) |
| **Feature Store** | Amazon SageMaker Feature Store |
| **MLOps** | Machine Learning Operations |
| **PowerShell** | Cross-platform shell (`pwsh`) |

---

# How to use this guide

Do every step **in order**. Terminal commands run in **VS Code → PowerShell**.

The full repo was cloned in Lab 0 — **no `git pull`** is needed between labs. This guide is **`lab2/`** in the repo (Lab 2 in the course sequence).

### clear the terminal between steps

Type `clear` and press **Enter** before each new command block.

### Working directory

**EC2:** `~/ai-infra-mlops/lab2` · **Windows:** `D:\Current_work\ai-infra-mlops\lab2`

Outputs: `~/ai-infra-mlops/workspace/lab2/` · Lab 1 configs: `workspace/lab1/config/`

---

# What you will build

- Synthetic banking customer and transaction datasets (with PII)
- Anonymized datasets and PII compliance reports
- Data quality validation reports
- Engineered feature dataset for ML
- SageMaker Feature Store feature groups
- Data drift baseline and monitoring config
- Final compliance documentation (local + S3)

---

# Step 1 — Confirm `lab2/` files in the repo

**Prerequisite:** [Lab 1](../lab1/STEPS.md) complete in `lab1/` (`Compliance Score: 100%`).

The full repo was cloned in Lab 0. You already have `lab2/` — **no `git pull` is needed.**

```powershell
clear
cd D:\Current_work\ai-infra-mlops
Get-ChildItem lab2
```

### Expected result

You see `lab2/STEPS.md`, `lab2/scripts/`, and `lab2/config/`.

---

# Step 2 — Confirm workspace folder

Sets your working directory to `lab2` for the rest of this lab.

```powershell
clear
cd D:\Current_work\ai-infra-mlops\lab2
Get-ChildItem ..\workspace\lab2
```

If folders are missing, re-run Lab 0 setup:

```powershell
clear
cd D:\Current_work\ai-infra-mlops\lab0
python scripts\setup_lab_directories.py
cd ..\lab2
```

### Expected result

Under `workspace\lab2\` you see `config`, `data`, `logs`, `results`, `validation`.

![Step 2 — workspace\lab2 folders](images/step-02-workspace-lab2.png)

---

# Step 3 — Verify Lab 1 prerequisites (`lab1/`)

```powershell
clear
python scripts\validate_lab2.py
```

Also confirm Lab 1 passed in `lab1/`:

```powershell
clear
cd ..\lab1
python scripts\validate_environment.py
cd ..\lab2
```

### Expected result

`validate_lab2.py` shows `✅ Lab 1 config: buckets.json` and `iam_roles.json`.  
Lab 1 validation shows `Compliance Score: 100.0%`.

**You do not re-run Lab 1 scripts here.** Lab 1 Step 6 already created the IAM roles and policies needed for Step 8.

![Step 3 — Lab 1 prerequisites validated](images/step-03-prerequisites.png)

---

# Step 4 — Generate banking dataset

```bash
clear
cd ~/ai-infra-mlops/lab2
python3 scripts/download_banking_data.py
```

Generates **1000** customers / transactions by default (`LAB_NUM_RECORDS`).

### Expected result

- `workspace\lab2\data\customers.csv`
- `workspace\lab2\data\transactions.csv`
- `workspace\lab2\config\dataset_metadata.json`

---

# Step 5 — Detect and anonymize PII

```bash
clear
python3 scripts/pii_detection_anonymization.py
```

**Classroom:** `LAB_USE_COMPREHEND=0` uses regex patterns (~5 min).  
**Optional:** `LAB_USE_COMPREHEND=1` adds Amazon Comprehend (much slower).

### Expected result

- `anonymized_customers.csv`, `anonymized_transactions.csv`
- `config\pii_report.json`, `config\pii_compliance_report.json`

---

# Step 6 — Validate data quality

```powershell
clear
python scripts\data_validation.py
```

### Expected result

Quality scores printed for customers and transactions. Reports saved to `config\data_quality_report_*.json`.

---

# Step 7 — Engineer features

```powershell
clear
python scripts\feature_engineering.py
```

### Expected result

- `data\engineered_banking_data.csv`
- `config\feature_metadata.json`
- `config\preprocessor.pkl`

---

# Step 8 — Set up SageMaker Feature Store

```bash
clear
python3 scripts/feature_store_setup.py
```

About **5–15 minutes** at classroom data size. Waits for feature groups to become active, then ingests to the **offline store**.

### Expected result

Transaction and customer feature groups created (or already exist).  
`config\feature_store_config.json` saved.

---

# Step 9 — Configure drift detection

```powershell
clear
python scripts\data_drift_detection.py
```

### Expected result

`config\drift_report.json` and baseline CSV in `data\`. CloudWatch alarm may warn if SNS topic is missing — safe to continue.

---

# Step 10 — Generate compliance report

```powershell
clear
python scripts\generate_compliance_doc.py
```

### Expected result

`data\compliance_report_final.json` and upload to governance S3 bucket.

Or run Steps 4–10 in one command:

```powershell
clear
python scripts\run_lab2.py
```

---

# Step 11 — Verify outputs (optional)

```powershell
clear
python scripts\validate_lab2.py
Get-ChildItem ..\workspace\lab2\data
Get-ChildItem ..\workspace\lab2\config
```

### Expected result

All data and config files from Steps 4–10 exist.

---

# Troubleshooting

### Missing Lab 1 config

Complete [Lab 1](../lab1/STEPS.md) in `lab1/` first. `workspace\lab1\config\buckets.json` must exist.

### Comprehend access denied

Pattern-based PII detection still runs. Ensure your student role can call `comprehend:DetectPiiEntities` or ignore Comprehend warnings if anonymization counts are > 0.

### Feature Store errors

1. SageMaker domain must be **InService** from Lab 1.
2. Re-run Lab 1 Step 7: `python3 scripts/create_banking_iam_roles.py` (Feature Store S3 permissions).
3. Feature group name clash: `python3 scripts/cleanup_lab2.py --aws`, then Step 8 again.
4. Ingest warnings on re-run are OK if `feature_store_config.json` exists.

### Start from scratch

```bash
python3 scripts/cleanup_lab2.py --aws
python3 scripts/reset_course.py --labs lab2
```

Then re-run from Step 4.

### Instructor re-screenshot

Delete `workspace/lab2/data/*` and `workspace/lab2/config/*.json`, or use `cleanup_lab2.py` above.

---

## Lab 2 complete

Return to **[README.md](../README.md)** for the next lab in the course sequence.
