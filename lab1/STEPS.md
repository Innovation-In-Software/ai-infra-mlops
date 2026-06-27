# Lab 1: Secure MLOps Environment Setup

## Class · `ai-mlops-2026-jun30` · **30 min** · **us-west-2**
## Platform · **EC2** + [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) + **bash**
## Prerequisite · [Lab 0](../lab0/STEPS.md) complete
## Working directory · `~/ai-infra-mlops/lab1`
## Outputs · `~/ai-infra-mlops/workspace/lab1/`

---

## Pacing (30 min)

| Min | Steps |
|-----|-------|
| 0–3 | 1–3 confirm repo + AWS |
| 3–10 | 4–6 KMS, S3, IAM |
| 10–25 | **7 SageMaker (longest)** |
| 25–30 | 8–9 CloudTrail + validate |

Run **Step 7** as soon as Steps 4–6 finish — domain creation takes the most time.

---

# Step 1 — Confirm lab1 in repo

```bash
clear
cd ~/ai-infra-mlops
ls -1 lab1
```

**Expected output:**

```text
STEPS.md
config
images
requirements.txt
scripts
```

**Optional screenshot:** `images/step-01-lab1-folder.png`

---

# Step 2 — Confirm workspace

```bash
clear
cd ~/ai-infra-mlops/lab1
ls -1 ../workspace/lab1
```

**Expected output:**

```text
config
data
logs
results
scripts
```

If missing: `cd ~/ai-infra-mlops/lab0 && python3 scripts/setup_lab_directories.py`

**Optional screenshot:** `images/step-02-workspace-lab1.png`

---

# Step 3 — Verify AWS CLI

```bash
clear
aws sts get-caller-identity
aws configure get region
```

**Expected output:**

```text
{
    "Account": "028417007274",
    "Arn": "arn:aws:iam::028417007274:user/..."
}
us-west-2
```

**Optional screenshot:** `images/step-03-aws-identity.png`

---

# Step 4 — Create KMS keys

```bash
clear
cd ~/ai-infra-mlops/lab1
python3 scripts/create_kms_keys.py
```

**Expected output:**

```text
🔐 Creating KMS Keys for Banking Compliance
============================================================
✅ S3 KMS Key Created: <uuid>
✅ SageMaker KMS Key Created: <uuid>
✅ S3 Key Policy Applied
============================================================
✅ KMS Key Creation Complete!
```

Config: `workspace/lab1/config/kms_keys.json`

**Optional screenshot:** `images/step-04-kms.png`

---

# Step 5 — Create S3 buckets

```bash
clear
python3 scripts/create_banking_buckets.py
```

**Expected output:**

```text
📦 Creating Banking-Compliant S3 Buckets
...
✅ All Banking-Compliant Buckets Created!
   RAW: bank-mlops-<account-id>-raw
   PROCESSED: bank-mlops-<account-id>-processed
   ...
```

Config: `workspace/lab1/config/buckets.json`

**Optional screenshot:** `images/step-05-s3.png`

---

# Step 6 — Create IAM roles

```bash
clear
python3 scripts/create_banking_iam_roles.py
```

**Expected output:**

```text
🔑 Creating Banking-Compliant IAM Roles
...
   ✅ Data Scientist policy attached
   ✅ ML Engineer policy attached
   ✅ Compliance Officer policy attached
============================================================
✅ Banking IAM Roles Created!
   DATA_SCIENTIST: arn:aws:iam::<account-id>:role/BankingDataScientistRole
```

Config: `workspace/lab1/config/iam_roles.json`

**Optional screenshot:** `images/step-06-iam.png`

---

# Step 7 — SageMaker Studio (longest step)

```bash
clear
python3 scripts/create_sagemaker_studio.py
```

**Expected output:**

```text
🖥️ Setting Up SageMaker Studio with Banking Security
...
⏳ Waiting for domain to become InService (up to 15 minutes)...
   ✅ Domain is ready!
...
✅ SageMaker Studio Configuration Complete!
   Domain ID: d-xxxxxxxxxxxx
📋 To access SageMaker Studio:
   https://us-west-2.console.aws.amazon.com/sagemaker/home?region=us-west-2#/studio/d-...
```

Config: `workspace/lab1/config/sagemaker_studio.json`

**Optional screenshot:** `images/step-07-sagemaker.png`

---

# Step 8 — CloudTrail audit logging

```bash
clear
python3 scripts/enable_audit_logging.py
```

**Expected output:**

```text
📝 Enabling Audit Logging for Banking Compliance
...
✅ Audit Logging Enabled!
   CloudTrail Trail: BankingMLOpsAuditTrail-<account-id>
📋 Audit Dashboard URL:
   https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#dashboards:name=Banking-MLOps-Audit-Dashboard
```

**Optional screenshot:** `images/step-08-cloudtrail.png`

---

# Step 9 — Validate environment

```bash
clear
python3 scripts/validate_environment.py
```

**Expected output:**

```text
🔍 Validating Banking MLOps Environment
...
📋 COMPLIANCE REPORT SUMMARY
============================================================
Total Checks: 13
Passed: 13
Failed: 0
Compliance Score: 100.0%
Status: COMPLIANT

✅ ALL CHECKS PASSED! Environment is compliant.
   Proceed to Lab 2 (lab2/STEPS.md)
```

Or run all steps: `python3 scripts/run_lab1.py`

**Optional screenshot:** `images/step-09-validation-pass.png`

---

# Step 10 — Console check (optional)

Browser: S3 (6 buckets), IAM (Banking roles), SageMaker (domain Ready), CloudTrail (Logging).

**Optional screenshot:** `images/step-10-console.png`

---

## Lab 1 complete → [Lab 2](../lab2/STEPS.md)
