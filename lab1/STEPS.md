# Lab 1: Secure MLOps Environment Setup

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30–45 minutes (SageMaker domain wait up to 15 min) |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | [Lab 0](../lab0/STEPS.md) complete (9/9 verify) |
| **Working directory** | `~/ai-infra-mlops/lab1` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab1/` |

> All commands in **Steps 1–9** run in the **VS Code integrated terminal on EC2** (`whoami` = `ec2-user`). Do not use Windows PowerShell on the ProTech VM for these steps.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
whoami
hostname
cd lab1
```

**Expected:** `ec2-user` and hostname `ip-172-31-...us-west-2.compute.internal`. If you see `Administrator` or `COMPUTER540`, reconnect [Lab 0 Step 13](../lab0/STEPS.md) (Remote-SSH to EC2).

Confirm Lab 0 passed:

```bash
cd ~/ai-infra-mlops/lab0 && python3 scripts/verify_environment.py
```

**Expected:** `Passed: 9` / `Failed: 0` — then `cd ../lab1`.

If lab scripts print **`PythonDeprecationWarning`** (Boto3 / Python 3.9), complete [Lab 0 Step 17a](../lab0/STEPS.md) and re-run [Lab 0 Step 18](../lab0/STEPS.md) before continuing.

Run `clear` before each step for clean terminal screenshots.

---

## Fresh start (after teardown or failed partial run)

If you ran [course teardown](../scripts/teardown_course.py) or Lab 1 failed halfway:

1. **AWS:** Teardown schedules KMS keys for deletion (7–30 days). You can still create **new** keys in Step 4; do not expect old key IDs to work.
2. **Workspace:** Clear local Lab 1 config so scripts start clean:

```bash
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab1
cd lab1
```

3. Re-run **Steps 4–9** in order. If SageMaker or CloudTrail already exist in AWS, scripts print `already exists` warnings — that is OK.

> **Do not re-run Step 4** on a successful Lab 1 just to “refresh” — it creates **new** KMS keys each time and overwrites `kms_keys.json`.

---

## Pacing (30–45 min)

| Min | Steps |
|-----|-------|
| 0–5 | 1–3 confirm repo + AWS |
| 5–12 | 4–6 KMS, S3, IAM |
| 12–30 | **7 SageMaker (longest — up to 15 min wait)** |
| 30–40 | 8–9 CloudTrail + validate |
| 40+ | 10 console check (optional) |

Start **Step 7** as soon as Steps 4–6 finish. Steps 5–8 depend on earlier config files — do not skip ahead.

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

If missing: run [Lab 0 Step 21](../lab0/STEPS.md) (`python3 scripts/setup_lab_directories.py` from `lab0/`).

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
    "UserId": "AIDAXXXXXXXXXXXXXXXXX",
    "Account": "028417007274",
    "Arn": "arn:aws:iam::028417007274:user/Instructor01"
}
us-west-2
```

Account ID and ARN must match your handout (instructor example: `028417007274`). Region must be **`us-west-2`**.  
If you used an **instance profile** in Lab 0, the ARN may show `assumed-role/EC2MLOpsLabRole/...` instead — OK if your instructor confirms lab permissions.

**Optional screenshot:** `images/step-03-aws-identity.png`

---

# Step 4 — Create KMS keys

**Requires:** Step 3 (`aws` works).

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

Config written to: `~/ai-infra-mlops/workspace/lab1/config/kms_keys.json`

**Optional screenshot:** `images/step-04-kms.png`

---

# Step 5 — Create S3 buckets

**Requires:** Step 4 (`kms_keys.json` exists).

```bash
clear
python3 scripts/create_banking_buckets.py
```

**Expected output:**

```text
📦 Creating Banking-Compliant S3 Buckets
...
✅ All Banking-Compliant Buckets Created!

📋 Bucket Summary:
   RAW: bank-mlops-<account-id>-raw
   PROCESSED: bank-mlops-<account-id>-processed
   ...
```

Config: `~/ai-infra-mlops/workspace/lab1/config/buckets.json`

**Optional screenshot:** `images/step-05-s3.png`

---

# Step 6 — Create IAM roles

**Requires:** Step 5 (`buckets.json` exists).

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

📋 Role Summary:
   DATA_SCIENTIST: arn:aws:iam::<account-id>:role/BankingDataScientistRole
   ML_ENGINEER: arn:aws:iam::<account-id>:role/BankingMLEngineerRole
   COMPLIANCE_OFFICER: arn:aws:iam::<account-id>:role/BankingComplianceOfficerRole
```

Config: `~/ai-infra-mlops/workspace/lab1/config/iam_roles.json`

**Optional screenshot:** `images/step-06-iam.png`

---

# Step 7 — SageMaker Studio (longest step)

**Requires:** Step 6 (`iam_roles.json` exists — uses `BankingDataScientistRole`).

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

Config: `~/ai-infra-mlops/workspace/lab1/config/sagemaker_studio.json`

If you see `Timed out` or `not ready yet`, wait 5 minutes and **re-run this step** (same command).

**Optional screenshot:** `images/step-07-sagemaker.png`

---

# Step 8 — CloudTrail audit logging

**Requires:** Step 5 (`buckets.json` — audit bucket).

```bash
clear
cd ~/ai-infra-mlops/lab1
python3 scripts/enable_audit_logging.py
```

**Expected output:**

```text
📝 Enabling Audit Logging for Banking Compliance
...
   ⏳ Waiting 12s for IAM role propagation...
   ✅ CloudTrail trail created: BankingMLOpsAuditTrail-<account-id>
   ✅ Logging started
   ✅ S3 object-level logging enabled for data buckets
...
✅ Audit Logging Enabled!
   CloudTrail Trail: BankingMLOpsAuditTrail-<account-id>
📋 Audit Dashboard URL:
   https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#dashboards:name=Banking-MLOps-Audit-Dashboard
```

> **If you see** `InvalidCloudWatchLogsRoleArnException` **(Access denied — trust relationships):**  
> IAM propagation delay right after the CloudTrail role is created. Wait **60 seconds**, then re-run:
> ```bash
> python3 scripts/enable_audit_logging.py
> ```
> The script also retries automatically (up to 5 times). S3 access logging above the error is OK.

> **If you see** `InvalidCloudWatchLogsLogGroupArnException` **(cannot validate log group ARN):**  
> Run `git pull` on EC2 for the latest `enable_audit_logging.py`, then re-run Step 8.  
> A failed partial run is safe to re-run — the script updates an existing trail if needed.

**Optional screenshot:** `images/step-08-cloudtrail.png`

---

# Step 9 — Validate environment

```bash
clear
python3 scripts/validate_environment.py
```

**Expected output (shape — your IDs will differ):**

```text
🔍 Validating Banking MLOps Environment
============================================================

📋 Validating KMS Keys...
✅ KMS Key s3_key_id: Enabled: <uuid>
✅ KMS Key sm_key_id: Enabled: <uuid>

📋 Validating S3 Buckets...
✅ Bucket raw: Exists and encrypted: bank-mlops-<account-id>-raw
✅ Bucket processed: Exists and encrypted: bank-mlops-<account-id>-processed
✅ Bucket models: Exists and encrypted: bank-mlops-<account-id>-models
✅ Bucket monitoring: Exists and encrypted: bank-mlops-<account-id>-monitoring
✅ Bucket governance: Exists and encrypted: bank-mlops-<account-id>-governance
✅ Bucket audit: Exists and encrypted: bank-mlops-<account-id>-audit

📋 Validating IAM Roles...
✅ Role data_scientist: Exists: BankingDataScientistRole
✅ Role ml_engineer: Exists: BankingMLEngineerRole
✅ Role compliance_officer: Exists: BankingComplianceOfficerRole

📋 Validating SageMaker Studio...
✅ SageMaker Studio: InService: d-xxxxxxxxxxxx

📋 Validating Audit Logging...
✅ CloudTrail: Logging enabled: BankingMLOpsAuditTrail-<account-id>

============================================================
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

Or run all setup + validation in one go: `python3 scripts/run_lab1.py`

Report saved to: `~/ai-infra-mlops/workspace/lab1/results/compliance_report.json`

**Optional screenshot:** `images/step-09-validation-pass.png`

---

# Step 10 — Console check (optional)

On the **ProTech VM browser** (not the EC2 terminal), region **us-west-2**:

| Service | What to confirm |
|---------|-----------------|
| **S3** | Six `bank-mlops-<account-id>-*` buckets |
| **IAM** | Roles `BankingDataScientistRole`, `BankingMLEngineerRole`, `BankingComplianceOfficerRole` |
| **SageMaker** | Domain `banking-mlops-domain-<account-id>` — **InService** |
| **CloudTrail** | Trail `BankingMLOpsAuditTrail-<account-id>` — **Logging** |

**Optional screenshot:** `images/step-10-console.png`

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `whoami` = `Administrator` | Reconnect VS Code Remote-SSH to EC2 ([Lab 0 Step 13](../lab0/STEPS.md)) |
| `Unable to locate credentials` | Re-run [Lab 0 Step 17](../lab0/STEPS.md) `aws configure` on EC2 |
| `No such file: kms_keys.json` | Run Step 4 before Step 5 |
| `No such file: buckets.json` | Run Step 5 before Steps 6 and 8 |
| `No such file: iam_roles.json` | Run Step 6 before Step 7 |
| `AccessDenied` on KMS / IAM / SageMaker | Confirm IAM user has lab admin rights; ask instructor |
| KMS `LimitExceededException` | Too many keys in account — wait for teardown pending deletion or ask instructor |
| SageMaker domain `Failed` or timeout | Wait 5 min, re-run Step 7; check VPC/subnets exist (default VPC) |
| SageMaker validation `Status: Pending` | Domain still creating — re-run Step 7 or wait and re-run Step 9 |
| `PythonDeprecationWarning` (Boto3 / Python 3.9) | [Lab 0 Step 17a](../lab0/STEPS.md) — upgrade to Python 3.11, re-run Step 18, then continue Lab 1 |
| CloudTrail `InvalidCloudWatchLogsRoleArnException` | IAM propagation — wait **60s**, re-run Step 8 (script auto-retries) |
| CloudTrail `InvalidCloudWatchLogsLogGroupArnException` | `git pull` then re-run Step 8 (log group ARN format fix) |
| CloudTrail `TrailAlreadyExists` | Warning only — script updates trail and starts logging |
| Step 9 partial failures | Re-run the failed step (4–8), then Step 9 |
| Re-running Step 4 creates extra keys | Use [Fresh start](#fresh-start-after-teardown-or-failed-partial-run) instead of repeating Step 4 |

---

## Lab 1 complete → [Lab 2](../lab2/STEPS.md)
