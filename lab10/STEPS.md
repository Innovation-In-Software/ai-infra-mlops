# Lab 10: Enterprise MLOps Architecture

## Class · `ai-mlops-2026-jun30` · **30 min** · **us-west-2**
## Platform · **EC2** + [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) + **bash**
## Prerequisite · [Lab 9](../lab9/STEPS.md) complete
## Working directory · `~/ai-infra-mlops/lab10`
## Outputs · `~/ai-infra-mlops/workspace/lab10/`

## Run all · `python3 scripts/run_lab10.py`

---

# Step 1 — Confirm lab10 folder

```bash
clear
cd ~/ai-infra-mlops && ls -1 lab10
```

**Expected output:** `Validate Lab 10 — Course Completion`, `config`, `images`, `requirements.txt`, `scripts`

**Optional screenshot:** `images/step-01-lab10-folder.png`

---

# Step 2 — Collect course artifacts

```bash
clear
cd ~/ai-infra-mlops/lab10
pip install -r requirements.txt
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

**Optional screenshot:** `images/step-02-collect.png`

---

# Step 3 — Architecture assessment

```bash
clear
python3 scripts/architecture_assessment.py
```

**Expected output:**

```text
🏗️ Enterprise Architecture Assessment
============================================================
   Security layer:     ✅ COMPLETE
   Data layer:         ✅ COMPLETE
   Training layer:     ✅ COMPLETE
   Deployment layer:   ✅ COMPLETE
   Monitoring layer:   ✅ COMPLETE
   Governance layer:   ✅ COMPLETE
   Score: 94/100
```

**Optional screenshot:** `images/step-03-assessment.png`

---

# Step 4 — Gap analysis

```bash
clear
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

**Optional screenshot:** `images/step-04-gaps.png`

---

# Step 5 — Implementation roadmap

```bash
clear
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

**Optional screenshot:** `images/step-05-roadmap.png`

---

# Step 6 — Implementation checklist

```bash
clear
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

**Optional screenshot:** `images/step-06-checklist.png`

---

# Step 7 — Executive summary

```bash
clear
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

**Optional screenshot:** `images/step-07-summary.png`

---

# Step 8 — Final compliance bundle

```bash
clear
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

**Optional screenshot:** `images/step-08-bundle.png`

---

# Step 9 — Course completion validation

```bash
clear
python3 scripts/validate_lab10.py
```

**Expected output:**

```text
Validate Lab 10 — Course Completion
============================================================
🎉 COURSE COMPLETE — ai-mlops-2026-jun30
```

**Optional screenshot:** `images/step-09-complete.png`

---

# Step 10 — Reset workspace (optional, next cohort)

```bash
clear
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

# Step 11 — Delete all AWS resources (instructor)

After completing the course, tear down AWS resources so the account is clean for the next cohort.

```bash
clear
cd ~/ai-infra-mlops
python3 scripts/teardown_course.py --yes
```

This runs in order:

1. Reset all `workspace/lab1`–`lab10` folders  
2. Delete Lab 2 SageMaker Feature Groups (`banking-transaction-features`, `banking-customer-features`)  
3. Delete Lab 1 CloudTrail + dashboard (`delete_audit_logging.py`)  
4. Delete SageMaker Studio domain (`delete_sagemaker_studio.py`)  
5. Empty and delete Lab 1 S3 buckets (`delete_banking_buckets.py`)  
6. Delete Lab 5 ECR repository `banking-ml-inference` (if created)

**Expected output:**

```text
🧹 Full course teardown
============================================================
   ✅ Cleared workspace/lab1/ … lab10/
   ✅ Deleted: banking-transaction-features
   ✅ Deleted: banking-customer-features
   ✅ CloudTrail / SageMaker / S3 cleanup complete
   ✅ Deleted ECR repository: banking-ml-inference

✅ Teardown complete.
   Manual (if re-running Lab 1 from scratch):
   - IAM Console: delete BankingDataScientistRole, BankingMLEngineerRole, BankingComplianceOfficerRole
   - KMS Console: disable/delete keys from workspace/lab1/config/kms_keys.json (after Lab 1 re-run saves new IDs)
   - CloudWatch: delete BankingDataDriftAlarm if desired
```

**Optional screenshot:** `images/step-11-teardown.png`

---

## Course complete

You have finished Labs 0–10 on EC2. Run **Step 11** to delete AWS resources when the class is done.
