# Lab 9: Banking Security & Governance Framework

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30 minutes |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | [Lab 8](../lab8/STEPS.md) |
| **Working directory** | `~/ai-infra-mlops/lab9` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab9/` |

> All commands run in the **VS Code integrated terminal** on EC2. Do not use local Windows PowerShell for lab steps.

> **Quick run:** `python3 scripts/run_lab9.py` runs all script steps in order.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
cd lab9
```

Run `clear` before each step for clean terminal screenshots.

---

## Step 1 — Confirm lab9 folder

**Do this:**

```bash
clear
cd ~/ai-infra-mlops && ls -1 lab9
```

**Expected result:** `Validate Lab 9`


**Screenshot (optional):** `images/step-01-lab9-folder.png`

---

## Step 2 — Load governance baseline

**Do this:**

```bash
clear
cd ~/ai-infra-mlops/lab9
pip install -r requirements.txt
python3 scripts/load_governance_baseline.py
```

**Expected result:**

```text
🛡️ Governance Baseline
============================================================
   ✅ Lab 1 IAM roles loaded
   ✅ Lab 8 model registry reference loaded
   ✅ Audit trail from Lab 1 CloudTrail linked
✅ Baseline ready
```


**Screenshot (optional):** `images/step-02-baseline.png`

---

## Step 3 — IAM least-privilege review

**Do this:**

```bash
clear
python3 scripts/review_iam_policies.py
```

**Expected result:**

```text
🔑 IAM Review
============================================================
   Roles reviewed: 3
   Over-privileged actions: 0
   Status: COMPLIANT
✅ IAM review report saved
```


**Screenshot (optional):** `images/step-03-iam.png`

---

## Step 4 — Encryption audit

**Do this:**

```bash
clear
python3 scripts/audit_encryption.py
```

**Expected result:**

```text
🔐 Encryption Audit
============================================================
   S3 buckets: KMS encrypted ✅
   SageMaker: KMS encrypted ✅
   ECR: KMS encrypted ✅
✅ Encryption audit PASS
```


**Screenshot (optional):** `images/step-04-encryption.png`

---

## Step 5 — Model approval workflow

**Do this:**

```bash
clear
python3 scripts/model_approval_workflow.py
```

**Expected result:**

```text
📋 Model Approval
============================================================
   Model: banking-risk-xgboost-v1
   Fairness: APPROVED
   Security scan: APPROVED
   Status: PendingComplianceOfficer
✅ Workflow state saved
```


**Screenshot (optional):** `images/step-05-approval.png`

---

## Step 6 — Explainability report

**Do this:**

```bash
clear
python3 scripts/generate_explainability.py
```

**Expected result:**

```text
🔍 Explainability (SHAP)
============================================================
   Top features: transaction_amount, merchant_category, ...
   Report: results/explainability_report.json
✅ Explainability complete
```


**Screenshot (optional):** `images/step-06-explainability.png`

---

## Step 7 — Fairness governance check

**Do this:**

```bash
clear
python3 scripts/governance_fairness_check.py
```

**Expected result:**

```text
⚖️ Governance Fairness
============================================================
   Disparate impact: 0.91
   Threshold: 0.80
   Status: APPROVED
✅ Fairness governance PASS
```


**Screenshot (optional):** `images/step-07-fairness.png`

---

## Step 8 — Audit trail export

**Do this:**

```bash
clear
python3 scripts/export_audit_trail.py
```

**Expected result:**

```text
📝 Audit Trail Export
============================================================
   CloudTrail events: 150+ (sampled)
   Pipeline executions: linked
   Export: logs/governance_audit_export.json
✅ Audit export complete
```


**Screenshot (optional):** `images/step-08-audit.png`

---

## Step 9 — Governance compliance report

**Do this:**

```bash
clear
python3 scripts/generate_governance_report.py
```

**Expected result:**

```text
✅ Governance report: results/governance_report_final.json
   Overall status: COMPLIANT
```


**Screenshot (optional):** `images/step-09-report.png`

---

## Step 10 — Validate lab9

**Do this:**

```bash
clear
python3 scripts/validate_lab9.py
```

**Expected result:**

```text
Validate Lab 9
   ✅ governance_report_final.json
   ✅ governance_state.json
Prerequisites OK — proceed to Lab 10
```


**Screenshot (optional):** `images/step-10-validate.png`

---

## Lab 9 complete → [Lab 10](../lab10/STEPS.md)
