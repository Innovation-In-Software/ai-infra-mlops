# Lab 1.2: Banking Data Management & PII Protection

## Class · `ai-mlops-2026-jun30`
## Duration · 30 minutes
## Region · `us-west-2`
## Repo · [github.com/gjkaur/ai-infra-mlops](https://github.com/gjkaur/ai-infra-mlops)
## Editor · Visual Studio Code (VS Code)
## Terminal · PowerShell (integrated terminal only)
## Prerequisite · [Lab 1.1](../lab1/STEPS.md) complete (`Compliance Score: 100%`)

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

The full repo was cloned in Lab 0 — **no `git pull`** is needed between labs.

### clear the terminal between steps

Type `clear` and press **Enter** before each new command block.

### Working directory

From **Step 2** onward:

`PS D:\Current_work\ai-infra-mlops\lab2>`

**Step 2** sets this folder once. Stay here for Steps 3–10.

### Where your outputs go

`D:\Current_work\ai-infra-mlops\workspace\lab2\`

Lab 1.1 configs are read from `workspace\lab1\config\` (buckets, IAM roles).

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

# Step 1 — Confirm Lab 1.2 files in the repo

**Prerequisite:** [Lab 1.1](../lab1/STEPS.md) complete (`Compliance Score: 100%`).

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

---

# Step 3 — Verify Lab 1.1 prerequisites

```powershell
clear
python scripts\validate_lab2.py
```

Also confirm Lab 1.1 passed:

```powershell
clear
cd ..\lab1
python scripts\validate_environment.py
cd ..\lab2
```

### Expected result

`validate_lab2.py` shows `✅ Lab 1.1 config: buckets.json` and `iam_roles.json`.  
Lab 1.1 validation shows `Compliance Score: 100.0%`.

**You do not re-run Lab 1.1 scripts here.** Lab 1.1 Step 6 already created the IAM roles and policies needed for Step 8.

---

# Step 4 — Generate banking dataset

```powershell
clear
python scripts\download_banking_data.py
```

### Expected result

- `workspace\lab2\data\customers.csv`
- `workspace\lab2\data\transactions.csv`
- `workspace\lab2\config\dataset_metadata.json`

---

# Step 5 — Detect and anonymize PII

```powershell
clear
python scripts\pii_detection_anonymization.py
```

Uses regex patterns and **Amazon Comprehend** (`detect_pii_entities`). Comprehend warnings are OK — pattern matching still anonymizes data.

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

```powershell
clear
python scripts\feature_store_setup.py
```

This step can take **several minutes**. Uses Lab 1.1 S3 buckets and IAM roles. Customer features are ingested from the engineered training dataset (one row per `customer_id`).

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

### Missing Lab 1.1 config

Complete [Lab 1.1](../lab1/STEPS.md) first. `workspace\lab1\config\buckets.json` must exist.

### Comprehend access denied

Pattern-based PII detection still runs. Ensure your student role can call `comprehend:DetectPiiEntities` or ignore Comprehend warnings if anonymization counts are > 0.

### Feature Store errors

1. Re-run Step 8 after the SageMaker domain is `InService` from Lab 1.1.
2. Feature groups are idempotent on re-run. If ingest fails because records already exist, that warning is OK — check that `config\feature_store_config.json` was saved.

### Instructor re-screenshot

Delete `workspace\lab2\data\*` and `workspace\lab2\config\*.json`, then re-run steps from Step 4.

---

## Lab 1.2 complete

Return to **[README.md](../README.md)** for the next lab in the course sequence.
