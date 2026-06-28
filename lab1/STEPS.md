# Lab 1: Secure MLOps Environment Setup

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30–45 minutes (SageMaker wait up to 15 min in Step 7) |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | [Lab 0](../lab0/STEPS.md) complete — verification **9/9 passed** |
| **Working directory** | `~/ai-infra-mlops/lab1` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab1/config/` and `results/` |

> **Run Steps 1–9 once, in order.** Each step writes config files the next step needs.  
> All commands run in the **VS Code terminal on EC2** (`whoami` = `ec2-user`). Do not use Windows PowerShell on the ProTech VM.

---

## Before you start

1. Connect VS Code to EC2 ([Lab 0 Step 13](../lab0/STEPS.md)).
2. Pull the latest course repo and confirm you are on EC2:

```bash
cd ~/ai-infra-mlops && git pull
whoami
hostname
```

**Expected:**

```text
ec2-user
ip-172-31-....us-west-2.compute.internal
```

If you see `Administrator` or `COMPUTER540`, reconnect Remote-SSH to EC2 first.

3. Confirm Lab 0 passed:

```bash
cd ~/ai-infra-mlops/lab0 && python3 scripts/verify_environment.py
```

**Expected:** `Passed: 9` / `Failed: 0`.

4. Go to Lab 1:

```bash
cd ~/ai-infra-mlops/lab1
```

![git pull on EC2 before Lab 1](images/step-01-git-pull.png)

---

## Lab 1 roadmap

| Step | What you create |
|------|-----------------|
| **1–3** | Confirm repo, workspace, and AWS credentials |
| **4** | KMS encryption keys |
| **5** | Six banking-compliant S3 buckets |
| **6** | Three IAM roles (least privilege) |
| **7** | SageMaker Studio domain (**longest — up to 15 min wait**) |
| **8** | CloudTrail audit logging + dashboard |
| **9** | Compliance validation (13 checks) |
| **10** | Optional AWS Console check |

---

# Step 1 — Confirm the lab1 folder

**What you do:** Verify the Lab 1 course files are in the repo.

```bash
cd ~/ai-infra-mlops
ls -1 lab1
```

**Expected:**

```text
STEPS.md
config
images
requirements.txt
scripts
```

![Lab 1 folder listing on EC2](images/step-01b-lab1-folder.png)

---

# Step 2 — Confirm the workspace

**What you do:** Verify your personal workspace exists (created in [Lab 0 Step 21](../lab0/STEPS.md)).

```bash
cd ~/ai-infra-mlops/lab1
ls -1 ../workspace/lab1
```

**Expected:**

```text
config
data
logs
results
scripts
```

If folders are missing, run once from Lab 0:

```bash
cd ~/ai-infra-mlops/lab0
python3 scripts/setup_lab_directories.py
cd ~/ai-infra-mlops/lab1
```

![Workspace lab1 folders on EC2](images/step-02-workspace-lab1.png)

---

# Step 3 — Verify AWS CLI

**What you do:** Confirm AWS credentials and region before creating resources.

```bash
aws sts get-caller-identity
aws configure get region
```

**Expected:**

```text
{
    "UserId": "AIDAXXXXXXXXXXXXXXXXX",
    "Account": "<your-account-id>",
    "Arn": "arn:aws:iam::<account-id>:user/StudentXX"
}
us-west-2
```

Account ID and ARN must match your handout. Region must be **`us-west-2`**.  
If you used an **instance profile** in Lab 0, the ARN may show `assumed-role/EC2MLOpsLabRole/...` — that is OK if your instructor confirmed lab permissions.

![AWS identity on EC2](images/step-03a-aws-identity.png)

![AWS region us-west-2](images/step-03b-aws-region.png)

---

# Step 4 — Create KMS keys

**Requires:** Step 3 (`aws` works).

**What you do:** Create two KMS keys for S3 and SageMaker encryption.

```bash
cd ~/ai-infra-mlops/lab1
python3 scripts/create_kms_keys.py
```

**Expected:**

```text
🔐 Creating KMS Keys for Banking Compliance
============================================================
✅ S3 KMS Key Created: <uuid>
✅ SageMaker KMS Key Created: <uuid>
✅ S3 Key Policy Applied
============================================================
✅ KMS Key Creation Complete!
```

Config file: `~/ai-infra-mlops/workspace/lab1/config/kms_keys.json`

![KMS keys being created](images/step-04a-kms-keys.png)

![KMS key creation complete](images/step-04b-kms-complete.png)

![kms_keys.json in workspace](images/step-04c-kms-config-file.png)

---

# Step 5 — Create S3 buckets

**Requires:** Step 4 (`kms_keys.json` exists).

**What you do:** Create six encrypted buckets (raw, processed, models, monitoring, governance, audit).

```bash
python3 scripts/create_banking_buckets.py
```

**Expected:**

```text
📦 Creating Banking-Compliant S3 Buckets
...
✅ All Banking-Compliant Buckets Created!

📋 Bucket Summary:
   RAW: bank-mlops-<account-id>-raw
   PROCESSED: bank-mlops-<account-id>-processed
   MODELS: bank-mlops-<account-id>-models
   MONITORING: bank-mlops-<account-id>-monitoring
   GOVERNANCE: bank-mlops-<account-id>-governance
   AUDIT: bank-mlops-<account-id>-audit
```

Config file: `~/ai-infra-mlops/workspace/lab1/config/buckets.json`

![S3 buckets created — summary](images/step-05b-s3-buckets-complete.png)

---

# Step 6 — Create IAM roles

**Requires:** Step 5 (`buckets.json` exists).

**What you do:** Create three banking IAM roles with least-privilege policies.

```bash
python3 scripts/create_banking_iam_roles.py
```

**Expected:**

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

Config file: `~/ai-infra-mlops/workspace/lab1/config/iam_roles.json`

![IAM roles created](images/step-06-iam-roles.png)

---

# Step 7 — SageMaker Studio

**Requires:** Step 6 (`iam_roles.json` exists).

**What you do:** Create a SageMaker Studio domain and user profiles. **This step can take up to 15 minutes** while the domain becomes `InService`.

```bash
python3 scripts/create_sagemaker_studio.py
```

**Expected:**

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

Config file: `~/ai-infra-mlops/workspace/lab1/config/sagemaker_studio.json`

**Wait for** `✅ Domain is ready!` before continuing to Step 8.  
If the script times out, wait 5 minutes and run the **same command once more**.

![SageMaker domain waiting](images/step-07a-sagemaker-waiting.png)

![SageMaker Studio configuration complete](images/step-07c-sagemaker-complete.png)

---

# Step 8 — CloudTrail audit logging

**Requires:** Step 5 (`buckets.json` — audit bucket).

**What you do:** Enable CloudTrail, S3 access logging, object-level logging, and an audit dashboard.

```bash
cd ~/ai-infra-mlops/lab1
python3 scripts/enable_audit_logging.py
```

**Expected:**

```text
📝 Enabling Audit Logging for Banking Compliance
...
   ✅ CloudTrail trail created: BankingMLOpsAuditTrail-<account-id>
   ✅ Logging started
   ✅ S3 object-level logging enabled for data buckets
...
✅ Audit Logging Enabled!
   CloudTrail Trail: BankingMLOpsAuditTrail-<account-id>
📋 Audit Dashboard URL:
   https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#dashboards:name=Banking-MLOps-Audit-Dashboard
```

**Copy the dashboard URL** from the terminal before you close it.

![CloudTrail and logging enabled](images/step-08a-audit-logging.png)

![Audit logging complete summary](images/step-08b-audit-complete.png)

![Audit dashboard in CloudWatch](images/step-08c-audit-dashboard.png)

---

# Step 9 — Validate environment

**What you do:** Run the compliance checker (13 checks).

```bash
python3 scripts/validate_environment.py
```

**Expected:**

```text
🔍 Validating Banking MLOps Environment
...
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

Report saved to: `~/ai-infra-mlops/workspace/lab1/results/compliance_report.json`

![Validation output](images/step-09a-validation.png)

![Validation 13/13 COMPLIANT](images/step-09b-validation-pass.png)

---

# Step 10 — Console check (optional)

**What you do:** In the **ProTech VM browser** (not the EC2 terminal), open the AWS Console in region **`us-west-2`** and confirm resources exist.

| Service | Confirm |
|---------|---------|
| **S3** | Six buckets named `bank-mlops-<account-id>-*` |
| **IAM** | Roles `BankingDataScientistRole`, `BankingMLEngineerRole`, `BankingComplianceOfficerRole` |
| **KMS** | Two customer managed keys for S3 and SageMaker |
| **SageMaker** | Domain `banking-mlops-domain-<account-id>` — status **InService** |
| **CloudTrail** | Trail `BankingMLOpsAuditTrail-<account-id>` — **Logging** |

![S3 console — six buckets](images/step-10a-s3-console.png)

![IAM console — banking roles](images/step-10b-iam-console.png)

![KMS console — encryption keys](images/step-10c-kms-console.png)

![CloudTrail search](images/step-10d-cloudtrail-search.png)

![CloudTrail dashboard](images/step-10e-cloudtrail-dashboard.png)

![CloudTrail events](images/step-10f-cloudtrail-events.png)

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `whoami` = `Administrator` | Reconnect VS Code Remote-SSH to EC2 ([Lab 0 Step 13](../lab0/STEPS.md)) |
| `Unable to locate credentials` | Re-run [Lab 0 Step 17](../lab0/STEPS.md) `aws configure` on EC2 |
| `No such file: kms_keys.json` | Run Step 4 before Step 5 |
| `No such file: buckets.json` | Run Step 5 before Steps 6 and 8 |
| `No such file: iam_roles.json` | Run Step 6 before Step 7 |
| `PythonDeprecationWarning` (Boto3 / Python 3.9) | [Lab 0 Step 17a](../lab0/STEPS.md) — upgrade to Python 3.11, re-run Step 18 |
| SageMaker `Timed out` | Wait 5 min, run Step 7 **once more** (same command) |
| CloudTrail role error | Wait 60s, run Step 8 **once more** (script auto-retries) |
| Step 9 shows failures | Re-run only the failed step (4–8), then Step 9 |

---

## Appendix — Instructor reset (optional)

Participants normally **do not** reset Lab 1. Use this only after a failed run or before re-testing.

**Clear local workspace only** (AWS resources remain):

```bash
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab1
cd lab1
```

Then re-run **Steps 4–9**. Scripts may print `already exists` for resources still in AWS — that is OK.

**Full AWS teardown:** [Lab 10 Step 11](../lab10/STEPS.md) → `python3 scripts/teardown_course.py --yes`

---

## Lab 1 complete → [Lab 2](../lab2/STEPS.md)
