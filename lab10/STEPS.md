# Lab 10: Enterprise MLOps Architecture

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30 minutes |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | [Lab 9](../lab9/STEPS.md) |
| **Working directory** | `~/ai-infra-mlops/lab10` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab10/` |

> All commands run in the **VS Code integrated terminal** on EC2. Do not use local Windows PowerShell for lab steps.

> **Quick run:** `python3 scripts/run_lab10.py` runs all script steps in order.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
cd lab10
```

Run `clear` before each step for clean terminal screenshots.

---

## Step 1 — Confirm lab10 folder

**Do this:**

```bash
clear
cd ~/ai-infra-mlops && ls -1 lab10
```

**Expected result:** `Validate Lab 10 — Course Completion`


**Screenshot (optional):** `images/step-01-lab10-folder.png`

---

## Step 2 — Collect course artifacts

**Do this:**

```bash
clear
cd ~/ai-infra-mlops/lab10
pip install -r requirements.txt
python3 scripts/collect_course_artifacts.py
```

**Expected result:**

```text
📦 Course Artifact Collection
============================================================
   ✅ Lab 1: infrastructure configs
   ✅ Lab 2: data & feature store
   ✅ Lab 3: model & fairness
   ✅ Lab 4–9: CI/CD, deploy, monitor, pipeline, governance
✅ Artifact manifest saved
```


**Screenshot (optional):** `images/step-02-collect.png`

---

## Step 3 — Architecture assessment

**Do this:**

```bash
clear
python3 scripts/architecture_assessment.py
```

**Expected result:**

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


**Screenshot (optional):** `images/step-03-assessment.png`

---

## Step 4 — Gap analysis

**Do this:**

```bash
clear
python3 scripts/gap_analysis.py
```

**Expected result:**

```text
📋 Gap Analysis
============================================================
   Gaps identified: 2 (documentation, multi-region DR)
   Priority: MEDIUM
✅ Gap report saved
```


**Screenshot (optional):** `images/step-04-gaps.png`

---

## Step 5 — Implementation roadmap

**Do this:**

```bash
clear
python3 scripts/implementation_roadmap.py
```

**Expected result:**

```text
🗺️ Implementation Roadmap
============================================================
   Phase 1 (0–3 mo): Production hardening
   Phase 2 (3–6 mo): Multi-account landing zone
   Phase 3 (6–12 mo): Federated feature store
✅ Roadmap saved: results/implementation_roadmap.json
```


**Screenshot (optional):** `images/step-05-roadmap.png`

---

## Step 6 — Implementation checklist

**Do this:**

```bash
clear
python3 scripts/implementation_checklist.py
```

**Expected result:**

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


**Screenshot (optional):** `images/step-06-checklist.png`

---

## Step 7 — Executive summary

**Do this:**

```bash
clear
python3 scripts/generate_executive_summary.py
cat ../workspace/lab10/results/executive_summary.md | head -20
```

**Expected result:**

```text
✅ Executive summary generated
# Banking MLOps — Executive Summary
## Course: ai-mlops-2026-jun30
...
```


**Screenshot (optional):** `images/step-07-summary.png`

---

## Step 8 — Final compliance bundle

**Do this:**

```bash
clear
python3 scripts/build_compliance_bundle.py
ls -1 ../workspace/lab10/results
```

**Expected result:**

```text
✅ Compliance bundle created: results/course_compliance_bundle.zip
architecture_assessment.json
course_compliance_bundle.zip
executive_summary.md
implementation_roadmap.json
```


**Screenshot (optional):** `images/step-08-bundle.png`

---

## Step 9 — Course completion validation

**Do this:**

```bash
clear
python3 scripts/validate_lab10.py
```

**Expected result:**

```text
Validate Lab 10 — Course Completion
============================================================
🎉 COURSE COMPLETE — ai-mlops-2026-jun30
```


**Screenshot (optional):** `images/step-09-complete.png`

---

## Step 10 — Reset workspace (optional, next cohort)

**Do this:**

```bash
clear
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab1,lab2,lab3,lab4,lab5,lab6,lab7,lab8,lab9,lab10
```

**Expected result:**

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


**Screenshot (optional):** `images/step-10-reset.png`

---

## Step 11 — Delete all AWS resources (instructor)

**Do this:**

```bash
clear
cd ~/ai-infra-mlops
python3 scripts/teardown_course.py --yes
```

**Expected result:**

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


**Screenshot (optional):** `images/step-11-teardown.png`

---
