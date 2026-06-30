# Lab 10: Enterprise MLOps Architecture

## Class · `ai-mlops-2026-jun30` · **30 min** · **us-west-2**
## Platform · **EC2** + [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) + **bash**
## Prerequisite · [Lab 9](../lab9/STEPS.md) complete
## Working directory · `~/ai-infra-mlops/lab10`
## Outputs · `~/ai-infra-mlops/workspace/lab10/`

## Run all · `python3 scripts/run_lab10.py`

> All commands run in the **VS Code integrated terminal** on EC2. Do not use local Windows PowerShell for lab steps.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
whoami   # must be ec2-user
cd ~/ai-infra-mlops/lab9 && python3 scripts/validate_lab9.py
cd ~/ai-infra-mlops/lab10
```

**Expected:** `Prerequisites OK — proceed to Lab 10` from Lab 9 validation.

![Lab 9 validation — `python3 scripts/validate_lab9.py`](images/step-00b-lab9-validate.png)

> **Note:** Participant repo ends at **Lab 10** (Enterprise MLOps Architecture). There is no separate `lab11` folder — Module 11 content maps to Lab 10.

---

# Step 1 — Confirm lab10 folder

```bash
cd ~/ai-infra-mlops && ls -1 lab10
```

**Expected output:** `STEPS.md`, `config`, `images`, `requirements.txt`, `scripts`

![Step 1 — `ls -1 lab10`](images/step-01-lab10-folder.png)

---

# Step 2 — Collect course artifacts

```bash
cd ~/ai-infra-mlops/lab10
python3 -m pip install -r requirements.txt
python3 scripts/collect_course_artifacts.py
```

**Expected output:**

```text
📦 Course Artifact Collection
============================================================
   ✅ Lab 1: infrastructure configs
   ✅ Lab 2: data & feature store
   ✅ Lab 3: model & fairness
   ✅ Lab 4–9: CI/CD, deploy, monitor, pipeline, governance
✅ Artifact manifest saved
```

![Step 2 — `collect_course_artifacts.py`](images/step-02-collect.png)

---

# Step 3 — Architecture assessment

```bash
python3 scripts/architecture_assessment.py
```

**Expected output:**

```text
🏗️ Enterprise Architecture Assessment
============================================================
   Security layer:     ✅ COMPLETE
   Data layer:         ✅ COMPLETE
   Training layer:     ✅ COMPLETE
   Pipeline layer:     ✅ COMPLETE
   Deployment layer:   ✅ COMPLETE
   Monitoring layer:   ✅ COMPLETE
   Governance layer:   ✅ COMPLETE
   Score: 100/100
```

![Step 3 — `architecture_assessment.py`](images/step-03-assessment.png)

---

# Step 4 — Gap analysis

```bash
python3 scripts/gap_analysis.py
```

**Expected output:**

```text
📋 Gap Analysis
============================================================
   Gaps identified: 2 (documentation, multi-region DR)
   Priority: MEDIUM
✅ Gap report saved
```

![Step 4 — `gap_analysis.py`](images/step-04-gaps.png)

---

# Step 5 — Implementation roadmap

```bash
python3 scripts/implementation_roadmap.py
```

**Expected output:**

```text
🗺️ Implementation Roadmap
============================================================
   Phase 1 (0–3 mo): Production hardening
   Phase 2 (3–6 mo): Multi-account landing zone
   Phase 3 (6–12 mo): Federated feature store
✅ Roadmap saved: results/implementation_roadmap.json
```

![Step 5 — `implementation_roadmap.py`](images/step-05-roadmap.png)

---

# Step 6 — Implementation checklist

```bash
python3 scripts/implementation_checklist.py
```

**Expected output:**

```text
☑️ Implementation Checklist
============================================================
   [x] Secure environment (Lab 1)
   [x] Data & PII (Lab 2)
   [x] Model training & fairness (Lab 3)
   ...
   [ ] Multi-region DR (future)
   Completed: 18/20 items
```

![Step 6 — `implementation_checklist.py`](images/step-06-checklist.png)

---

# Step 7 — Executive summary

```bash
python3 scripts/generate_executive_summary.py
cat ../workspace/lab10/results/executive_summary.md | head -20
```

**Expected output:**

```text
✅ Executive summary generated
# Banking MLOps — Executive Summary
## Course: ai-mlops-2026-jun30
...
```

![Step 7 — `generate_executive_summary.py`](images/step-07-summary.png)

---

# Step 8 — Final compliance bundle

```bash
python3 scripts/build_compliance_bundle.py
ls -1 ../workspace/lab10/results
```

**Expected output:**

```text
✅ Compliance bundle created: results/course_compliance_bundle.zip
architecture_assessment.json
course_compliance_bundle.zip
executive_summary.md
implementation_roadmap.json
```

![Step 8 — `build_compliance_bundle.py`](images/step-08-bundle.png)

---

# Step 9 — Course completion validation

```bash
python3 scripts/validate_lab10.py
```

**Expected output:**

```text
Validate Lab 10 — Course Completion
============================================================
🎉 COURSE COMPLETE — ai-mlops-2026-jun30
```

![Step 9 — `validate_lab10.py`](images/step-09-complete.png)

---

# Step 10 — Reset workspace (optional, next cohort)

```bash
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab1,lab2,lab3,lab4,lab5,lab6,lab7,lab8,lab9,lab10
```

**Expected output:**

```text
🧹 Reset course workspace
============================================================
   Repo: /home/ec2-user/ai-infra-mlops
   ✅ Cleared workspace/lab1/
   ✅ Cleared workspace/lab2/
   ...
   ✅ Cleared workspace/lab10/

✅ Done. Re-run labs from STEPS.md (Lab 0 verify → Labs 1–10).
```

**Optional screenshot:** `images/step-10-reset.png`

---

# Step 11 — Delete AWS resources (optional — after all labs)

> **Only run this when the course is fully complete.** Do **not** run teardown scripts during Labs 1–9 — you will delete resources still needed for later labs.

After finishing Labs 0–10, tear down AWS resources so the account is clean for the next cohort.

```bash
cd ~/ai-infra-mlops
python3 scripts/teardown_course.py --yes
```

This also removes the Lab 4 CodePipeline (`banking-ml-cicd-lab4b-*`), CodeBuild project, and related IAM roles.

To also terminate lab EC2 instances (name contains `mlops`):

```bash
python3 scripts/teardown_course.py --yes --terminate-ec2
```

Preview without deleting:

```bash
python3 scripts/teardown_course.py --dry-run
```

This runs in order:

1. Reset all `workspace/lab1`–`lab10` folders  
2. Delete Lab 4 CodePipeline + CodeBuild (`optional/lab4b/scripts/teardown_lab4b.py`)  
3. Delete Lab 2 SageMaker Feature Groups (`banking-transaction-features`, `banking-customer-features`)  
4. Delete Lab 1 CloudTrail + dashboard (`delete_audit_logging.py`)  
5. Delete SageMaker Studio domain (`delete_sagemaker_studio.py`)  
6. Empty and delete Lab 1 S3 buckets (`delete_banking_buckets.py`)  
7. **Extended cleanup** (`teardown_aws_extras.py`):
   - CloudWatch alarms and dashboards (`BankingDataDriftAlarm`, `banking-ml-*`, …)
   - SageMaker experiments (`banking-risk-experiments` + trials)
   - SageMaker endpoints (`banking-*`) and pipeline (`banking-ml-pipeline`)
   - ECR repository `banking-ml-inference`
   - SNS topics (`banking-drift-alerts`, …)
   - IAM roles (`Banking*`, `EC2MLOpsLabRole`) and instance profile `EC2MLOpsLabProfile`
   - KMS keys (from `workspace/lab1/config/kms_keys.json` or description contains `Banking`) — **scheduled deletion in 7 days**
   - EC2 key pairs (`ai-mlops-instructor`, `mlops-lab-key`, …) and security group `mlops-lab-sg`
8. Optional `--terminate-ec2`: terminate running/stopped instances with `mlops` in the Name tag

**Expected output:**

```text
🧹 Full course teardown
============================================================
   ✅ Cleared workspace/lab1/ … lab10/
   ✅ Deleted: banking-transaction-features
   ✅ Deleted: banking-customer-features
   ✅ CloudTrail / SageMaker Studio / S3 cleanup complete

📋 Extended AWS cleanup (IAM, KMS, alarms, SageMaker, EC2, …)
============================================================
   ✅ Deleted CloudWatch alarms: BankingDataDriftAlarm
   ✅ Deleted experiment: banking-risk-experiments
   ✅ Deleted IAM role: BankingDataScientistRole
   ✅ Scheduled KMS key deletion (7d): ...
   ✅ Deleted security group: mlops-lab-sg

✅ Teardown complete.
   Re-run Lab 0 → Lab 1 to provision a fresh environment.
```

**Note:** KMS keys enter **PendingDeletion** for 7 days (AWS minimum). New Lab 1 runs create fresh keys.

**Optional screenshot:** `images/step-11-teardown.png`

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Architecture score below 90 | Complete missing lab workspaces (see layer → lab mapping in `architecture_assessment.py`) |
| Pipeline layer MISSING | Finish [Lab 8](../lab8/STEPS.md) through `validate_lab8.py` |
| `course_compliance_bundle.zip` missing | Run Step 9 (`build_compliance_bundle.py`) |
| ECR/pipeline checks warn in Step 2 | Normal if Lab 5/8 not finished; complete those labs first |

---

## Course complete

You have finished Labs 0–10 on EC2. When the class is done, run **Step 11** (optional) to delete AWS resources — not before.
