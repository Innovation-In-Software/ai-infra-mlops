# Lab 1.1: Secure MLOps Environment Setup

## Class · `ai-mlops-2026-jun30`
## Duration · 30 minutes
## Region · `us-west-2`
## Repo · [github.com/gjkaur/ai-infra-mlops](https://github.com/gjkaur/ai-infra-mlops)
## Editor · Visual Studio Code (VS Code)
## Terminal · PowerShell (integrated terminal only)
## Prerequisite · [Lab 0](../lab0/STEPS.md) complete

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

### clear the terminal between steps

Type `clear` and press **Enter** before each new command block.

### Working directory

From **Step 2** onward, terminal steps assume this prompt:

`PS D:\Current_work\ai-infra-mlops\lab1>`

**Step 2** sets this folder once. Stay here for Steps 3–9 — do not repeat `cd` in each step. If your prompt shows a different path, run `cd D:\Current_work\ai-infra-mlops\lab1` once, then continue.

### Where your outputs go

Lab scripts save config and results under:

`D:\Current_work\ai-infra-mlops\workspace\lab1\`

That folder is gitignored — your AWS resource IDs stay on your machine only.

---

# What you will build

- **AWS Key Management Service (KMS)** encryption keys (S3 + SageMaker)
- Six banking-compliant **Simple Storage Service (S3)** buckets
- Three **Identity and Access Management (IAM)** roles (data scientist, ML engineer, compliance officer)
- **Amazon SageMaker** Studio domain
- **AWS CloudTrail** audit logging
- Compliance validation report

---

# Step 1 — Pull the latest repo

**Prerequisite:** Lab 0 verification passed.

### Do this (VS Code terminal)

```powershell
clear
cd D:\Current_work\ai-infra-mlops
git pull
Get-ChildItem lab1
```

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

### Expected result

JSON with your IAM user ARN; region is `us-west-2`.

---

# Step 4 — Create KMS (Key Management Service) encryption keys

### Do this (VS Code terminal)

```powershell
clear
python scripts\create_kms_keys.py
```

### Expected result

Two keys created (S3 + SageMaker). Config saved to `workspace\lab1\config\kms_keys.json`.

---

# Step 5 — Create S3 (Simple Storage Service) buckets

### Do this (VS Code terminal)

```powershell
clear
python scripts\create_banking_buckets.py
```

### Expected result

Six buckets named `bank-mlops-<account-id>-<type>` (raw, processed, models, monitoring, governance, audit). Config saved to `workspace\lab1\config\buckets.json`.

---

# Step 6 — Create IAM (Identity and Access Management) roles

### Do this (VS Code terminal)

```powershell
clear
python scripts\create_banking_iam_roles.py
```

### Expected result

Roles created: `BankingDataScientistRole`, `BankingMLEngineerRole`, `BankingComplianceOfficerRole`. Config saved to `workspace\lab1\config\iam_roles.json`.

---

# Step 7 — Set up Amazon SageMaker Studio

### Do this (VS Code terminal)

```powershell
clear
python scripts\create_sagemaker_studio.py
```

This step can take **several minutes** while the domain becomes `InService`.

### Expected result

SageMaker Studio domain created. Config saved to `workspace\lab1\config\sagemaker_studio.json`. Console URL printed at the end.

---

# Step 8 — Enable AWS CloudTrail audit logging

### Do this (VS Code terminal)

```powershell
clear
python scripts\enable_audit_logging.py
```

### Expected result

CloudTrail trail, S3 access logging, and Amazon CloudWatch dashboard configured.

---

# Step 9 — Validate environment

### Do this (VS Code terminal)

```powershell
clear
python scripts\validate_environment.py
```

Or run the full lab in one command (Steps 4–9):

```powershell
clear
python scripts\run_lab1.py
```

### Expected result

```
Compliance Score: 100.0%
Status: COMPLIANT
ALL CHECKS PASSED! Environment is compliant.
   Proceed to Lab 1.2
```

Report saved to `workspace\lab1\results\compliance_report.json`.

---

# Step 10 — Verify in AWS Console (optional)

### Do this (browser)

1. **S3** — confirm six `bank-mlops-*` buckets exist
2. **IAM → Roles** — search `Banking`
3. **SageMaker → Studio** — confirm domain status is **InService**
4. **CloudTrail** — confirm trail is logging

### Expected result

Resources match the config files in `workspace\lab1\config\`.

---

# Troubleshooting

### Bucket already exists

Delete the old bucket in S3 console or use a fresh student account.

### Role already exists

Script skips with a warning — safe to continue if policies are correct.

### SageMaker domain stuck / failed

Check **VPC and subnets** in us-west-2. Re-run Step 7 after fixing.

### Validation failures

Open `workspace\lab1\results\compliance_report.json` for details. Re-run the failed script only.

### Insufficient permissions

Student accounts need **PowerUserAccess** + **IAMFullAccess** (from Lab 0).

---

## Lab 1.1 complete

Next: **Lab 1.2 — Banking Data Management & PII Protection** (coming soon).
