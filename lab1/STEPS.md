# Lab 1: Secure MLOps Environment Setup

## Folder · `lab1/`

## Class · `ai-mlops-2026-jun30`
## Duration · 30 minutes
## Region · `us-west-2`
## Repo · [github.com/gjkaur/ai-infra-mlops](https://github.com/gjkaur/ai-infra-mlops)
## Editor · VS Code (Remote SSH to EC2)
## Terminal · bash on EC2
## Delivery · See [CLOUD-DELIVERY.md](../CLOUD-DELIVERY.md)
## Prerequisite · [Lab 0](../lab0/STEPS.md) complete

---

# 30-minute pacing

| Minutes | Step |
|---------|------|
| 0–3 | Steps 1–3 — confirm folders and AWS |
| 3–10 | Steps 4–6 — KMS, S3, IAM (~5–8 min) |
| **10–25** | **Step 7 — SageMaker domain (longest wait)** |
| 25–30 | Steps 8–9 — CloudTrail + validation |

**Important:** Complete **Steps 4–6 before Step 7**. SageMaker needs `kms_keys.json`, `buckets.json`, and `iam_roles.json`.

---

# Terms (full forms)

| Short | Full form |
|-------|-----------|
| **VS Code** | Visual Studio Code |
| **AWS** | Amazon Web Services |
| **CLI** | Command Line Interface |
| **KMS** | AWS Key Management Service |
| **S3** | Simple Storage Service |
| **IAM** | Identity and Access Management |
| **MLOps** | Machine Learning Operations |
| **CloudTrail** | AWS CloudTrail (audit logging service) |
| **SageMaker** | Amazon SageMaker (managed ML platform) |
| **VPC** | Virtual Private Cloud |
| **ARN** | Amazon Resource Name |
| **STS** | AWS Security Token Service |
| **CloudWatch** | Amazon CloudWatch (monitoring and dashboards) |
| **PowerShell** | Cross-platform shell (`pwsh`) |

---

# How to use this guide

Do every step **in order**. Terminal commands run in **Visual Studio Code (VS Code) → PowerShell**. Some verification steps use the **Amazon Web Services (AWS) Console** in your browser.

The full repo was cloned in Lab 0 — **no `git pull`** is needed between labs. This guide is **`lab1/`** in the repo (Lab 1 in the course sequence).

### clear the terminal between steps

Type `clear` and press **Enter** before each new command block.

### Working directory

**EC2:** `~/ai-infra-mlops/lab1` · **Windows:** `D:\Current_work\ai-infra-mlops\lab1`

Outputs: `~/ai-infra-mlops/workspace/lab1/` (gitignored)

---

# What you will build

- **AWS Key Management Service (KMS)** encryption keys (S3 + SageMaker)
- Six banking-compliant **Simple Storage Service (S3)** buckets
- Three **Identity and Access Management (IAM)** roles (data scientist, ML engineer, compliance officer)
- **Amazon SageMaker** Studio domain
- **AWS CloudTrail** audit logging
- Compliance validation report

---

# Step 1 — Confirm `lab1/` files in the repo

**Prerequisite:** [Lab 0](../lab0/STEPS.md) complete (`lab0/`).

The full repo was cloned in Lab 0. You already have `lab1/` — **no `git pull` is needed.**

### Do this (VS Code terminal)

```powershell
clear
cd D:\Current_work\ai-infra-mlops
Get-ChildItem lab1
```

![Step 1 — confirm lab1 folder in repo](images/step-01-git-pull.png)

![Step 1b — lab1 folder contents](images/step-01b-lab1-folder.png)

### Expected result

You see `lab1/STEPS.md`, `lab1/scripts/`, and `lab1/config/`.

---

# Step 2 — Confirm workspace folder

Sets your working directory to `lab1` for the rest of this lab.

### Do this (VS Code terminal)

```powershell
clear
cd D:\Current_work\ai-infra-mlops\lab1
Get-ChildItem ..\workspace\lab1
```

If folders are missing, re-run Lab 0 setup:

```powershell
clear
cd D:\Current_work\ai-infra-mlops\lab0
python scripts\setup_lab_directories.py
```

![Step 2 — workspace\lab1 folders](images/step-02-workspace-lab1.png)

### Expected result

Under `workspace\lab1\` you see `config`, `data`, `logs`, `results`, `scripts`.

---

# Step 3 — Verify AWS access

### Do this (VS Code terminal)

```powershell
clear
aws sts get-caller-identity
aws configure get region
```

![Step 3a — aws sts get-caller-identity](images/step-03a-aws-identity.png)

![Step 3b — region is us-west-2](images/step-03b-aws-region.png)

### Expected result

JSON with your IAM user ARN; region is `us-west-2`.

---

# Step 4 — Create KMS encryption keys

Required before SageMaker and S3.

```bash
clear
cd ~/ai-infra-mlops/lab1
python3 scripts/create_kms_keys.py
```

![Step 4a — KMS keys created](images/step-04a-kms-keys.png)

![Step 4b — KMS key creation complete](images/step-04b-kms-complete.png)

![Step 4c — kms_keys.json in workspace/lab1/config](images/step-04c-kms-config-file.png)

### Expected result

Two keys; `workspace/lab1/config/kms_keys.json`.

---

# Step 5 — Create S3 buckets

```bash
clear
python3 scripts/create_banking_buckets.py
```

![Step 5a — S3 buckets creating](images/step-05a-s3-buckets.png)

![Step 5b — all six buckets created](images/step-05b-s3-buckets-complete.png)

### Expected result

Six `bank-mlops-<account-id>-*` buckets; `workspace/lab1/config/buckets.json`.

---

# Step 6 — Create IAM roles

```bash
clear
python3 scripts/create_banking_iam_roles.py
```

![Step 6 — IAM roles created](images/step-06-iam-roles.png)

### Expected result

`BankingDataScientistRole`, `BankingMLEngineerRole`, `BankingComplianceOfficerRole`; `iam_roles.json`.

**Lab 2 needs this step** — Feature Store uses `BankingDataScientistRole` S3 permissions from here.

---

# Step 7 — Set up Amazon SageMaker Studio (longest step)

Run after Steps 4–6. This can take **15+ minutes** while the domain becomes `InService`.

```bash
clear
python3 scripts/create_sagemaker_studio.py
```

Windows PowerShell: `python scripts\create_sagemaker_studio.py`

![Step 7a — domain waiting for InService](images/step-07a-sagemaker-waiting.png)

![Step 7b — user profiles created](images/step-07b-sagemaker-users.png)

![Step 7c — SageMaker Studio complete](images/step-07c-sagemaker-complete.png)

![Step 7d — copy Studio console URL](images/step-07d-sagemaker-url.png)

Save the Studio URL from the terminal or from `workspace/lab1/config/sagemaker_studio.json`.

### Expected result

Domain created and `InService`. Config: `workspace/lab1/config/sagemaker_studio.json`.

---

# Step 8 — Enable CloudTrail audit logging

### Do this (terminal)

```bash
clear
python3 scripts/enable_audit_logging.py
```

![Step 8a — CloudTrail and audit logging enabled](images/step-08a-audit-logging.png)

![Step 8b — audit logging complete with dashboard URL](images/step-08b-audit-complete.png)

**Save the dashboard URL:** Copy the CloudWatch dashboard link from the terminal output before running `clear`.

**Dashboard note:** The CloudWatch dashboard may show **“No data available”** immediately after setup — that is normal. Change the time range to **3 hours** or **24 hours** and wait a few minutes for metrics to appear.

![Step 8c — audit dashboard (metrics may take time)](images/step-08c-audit-dashboard.png)

### Expected result

CloudTrail trail, S3 access logging, and Amazon CloudWatch dashboard configured. All lines show ✅ (no ❌).

**Instructor re-screenshot — delete then re-create:**

```powershell
clear
python scripts\delete_audit_logging.py
clear
python scripts\enable_audit_logging.py
```

---

# Step 9 — Validate environment

### Do this (VS Code terminal)

```bash
clear
python3 scripts/validate_environment.py
```

![Step 9a — validation checks running](images/step-09a-validation.png)

![Step 9b — 100% compliant, proceed to Lab 2](images/step-09b-validation-pass.png)

Or run the full lab in one command (Steps 4–9):

```bash
clear
python3 scripts/run_lab1.py
```

### Expected result

```
Compliance Score: 100.0%
Status: COMPLIANT
ALL CHECKS PASSED! Environment is compliant.
   Proceed to Lab 2 (`lab2/STEPS.md`)
```

Report saved to `workspace\lab1\results\compliance_report.json`.

---

# Step 10 — Verify in AWS Console (optional)

### Do this (browser)

1. **S3** — confirm six `bank-mlops-*` buckets exist

![Step 10a — S3 buckets in console](images/step-10a-s3-console.png)

2. **IAM → Roles** — search `Banking`

![Step 10b — Banking IAM roles](images/step-10b-iam-console.png)

3. **KMS → Customer managed keys** — confirm two keys exist

![Step 10c — KMS keys in console](images/step-10c-kms-console.png)

4. **SageMaker → Domains** — confirm domain status is **Ready** / **InService** (see Step 7e)

5. **CloudTrail** — search **CloudTrail** in the console, open **Trails**, confirm `BankingMLOpsAuditTrail-<account-id>` shows **Logging**

![Step 10d — search CloudTrail in console](images/step-10d-cloudtrail-search.png)

![Step 10e — CloudTrail trail logging (blue banner is informational)](images/step-10e-cloudtrail-dashboard.png)

**CloudTrail banner note:** A blue banner about **CloudTrail Lake** closing to new customers is an AWS announcement — it does **not** mean your trail failed. Your trail status should show **Logging** with a green checkmark.

![Step 10f — CloudTrail event history](images/step-10f-cloudtrail-events.png)

### Expected result

Resources match the config files in `workspace\lab1\config\`.

---

# Troubleshooting

### ⚠️ “Already exists” vs ❌ errors

| Message | Meaning | Action |
|---------|---------|--------|
| `⚠️ already exists` | Resource from a previous run — script skips safely | Continue, or delete and re-create for clean screenshots |
| `❌ Error` | Something failed — later steps may cascade-fail | Fix the root error, delete partial resources, re-run |

**Why you saw errors on Step 8:** CloudTrail needed extra setup (audit bucket policy, IAM role policy, log group resource policy). Those are now fixed in the script.

### Python DeprecationWarning (yellow text)

If you see `DeprecationWarning: datetime.datetime.utcnow() is deprecated` during Steps 4 or 9, the lab still works — it is a Python 3.13 notice, not an AWS error. Your Lab 0 clone already includes the fix; you can ignore the warning.

### Bucket already exists

Delete the old bucket in S3 console or use a fresh student account.

**Instructor re-screenshot:** from `lab1` folder, delete buckets then re-create:

```powershell
clear
python scripts\delete_banking_buckets.py
clear
python scripts\create_banking_buckets.py
```

### Role already exists

Script skips with a warning — safe to continue if policies are correct.

### SageMaker domain stuck / failed

Check **VPC and subnets** in us-west-2. Re-run Step 7 after fixing.

**Instructor re-screenshot:** from `lab1` folder, delete domain then re-create:

```powershell
clear
python scripts\delete_sagemaker_studio.py
clear
python scripts\create_sagemaker_studio.py
```

Domain deletion can take several minutes. Creation then waits up to 15 minutes for `InService` before user profiles are created.

### Validation failures

Open `workspace\lab1\results\compliance_report.json` for details. Re-run the failed script only.

### Insufficient permissions

Student accounts need **PowerUserAccess** + **IAMFullAccess** (from Lab 0).

---

## Lab 1 complete

Next: **[Lab 2 — Banking Data Management & PII Protection](../lab2/STEPS.md)** (`lab2/`).
