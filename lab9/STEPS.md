# Lab 9: Banking Security & Governance Framework

## Class · `ai-mlops-2026-jun30` · **30 min** · **us-west-2**
## Platform · **EC2** + [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) + **bash**
## Prerequisite · [Lab 8](../lab8/STEPS.md) complete
## Working directory · `~/ai-infra-mlops/lab9`
## Outputs · `~/ai-infra-mlops/workspace/lab9/`
## Run all · `python3 scripts/run_lab9.py`

> All commands run in the **VS Code integrated terminal** on EC2. Do not use local Windows PowerShell for lab steps.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
whoami   # must be ec2-user
cd ~/ai-infra-mlops/lab8 && python3 scripts/validate_lab8.py
cd ~/ai-infra-mlops/lab1 && python3 scripts/create_banking_iam_roles.py
cd ~/ai-infra-mlops/lab9
```

**Expected:** `Prerequisites OK — proceed to Lab 9` from Lab 8 validation.

![Lab 8 validation — `python3 scripts/validate_lab8.py`](images/step-00b-lab8-validate.png)

---

# Step 1 — Confirm lab9 folder

```bash
cd ~/ai-infra-mlops && ls -1 lab9
```

**Expected output:** `STEPS.md`, `config`, `images`, `requirements.txt`, `scripts`

**Optional screenshot:** `images/step-01-lab9-folder.png`

---

# Step 2 — Load governance baseline

```bash
cd ~/ai-infra-mlops/lab9
pip install -r requirements.txt
python3 scripts/load_governance_baseline.py
```

**Expected output:**

```text
🛡️ Governance Baseline
============================================================
   ✅ Lab 1 IAM roles loaded
   ✅ Lab 8 model registry reference loaded
   ✅ Audit trail from Lab 1 CloudTrail linked
✅ Baseline ready
```

**Optional screenshot:** `images/step-02-baseline.png`

---

# Step 3 — IAM least-privilege review

```bash
python3 scripts/review_iam_policies.py
```

**Expected output:**

```text
🔑 IAM Review
============================================================
   Roles reviewed: 3
   Over-privileged actions: 0
   Status: COMPLIANT
✅ IAM review report saved
```

**Optional screenshot:** `images/step-03-iam.png`

---

# Step 4 — Encryption audit

```bash
python3 scripts/audit_encryption.py
```

**Expected output:**

```text
🔐 Encryption Audit
============================================================
   S3 buckets: KMS encrypted ✅
   SageMaker: KMS encrypted ✅
   ECR: KMS encrypted ✅
✅ Encryption audit PASS
```

**Optional screenshot:** `images/step-04-encryption.png`

---

# Step 5 — Model approval workflow

```bash
python3 scripts/model_approval_workflow.py
```

**Expected output:**

```text
📋 Model Approval
============================================================
   Model: banking-risk-xgboost-v1
   Fairness: APPROVED
   Security scan: APPROVED
   Status: PendingComplianceOfficer
✅ Workflow state saved
```

**Optional screenshot:** `images/step-05-approval.png`

---

# Step 6 — Explainability report

```bash
python3 scripts/generate_explainability.py
```

**Expected output:**

```text
🔍 Explainability (SHAP)
============================================================
   Top features: transaction_amount, merchant_category, ...
   Report: results/explainability_report.json
✅ Explainability complete
```

**Optional screenshot:** `images/step-06-explainability.png`

---

# Step 7 — Fairness governance check

```bash
python3 scripts/governance_fairness_check.py
```

**Expected output:**

```text
⚖️ Governance Fairness
============================================================
   Disparate impact: 0.91
   Threshold: 0.80
   Status: APPROVED
✅ Fairness governance PASS
```

**Optional screenshot:** `images/step-07-fairness.png`

---

# Step 8 — Audit trail export

```bash
python3 scripts/export_audit_trail.py
```

**Expected output:**

```text
📝 Audit Trail Export
============================================================
   CloudTrail events: 150+ (sampled)
   Pipeline executions: linked
   Export: logs/governance_audit_export.json
✅ Audit export complete
```

**Optional screenshot:** `images/step-08-audit.png`

---

# Step 9 — Governance compliance report

```bash
python3 scripts/generate_governance_report.py
```

**Expected output:**

```text
✅ Governance report: results/governance_report_final.json
   Overall status: COMPLIANT
```

**Optional screenshot:** `images/step-09-report.png`

---

# Step 10 — Validate lab9

```bash
python3 scripts/validate_lab9.py
```

**Expected output:**

```text
Validate Lab 9
============================================================
   ✅ governance_report_final.json
   ✅ governance_state.json
Prerequisites OK — proceed to Lab 10
```

**Optional screenshot:** `images/step-10-validate.png`

---

## Lab 9 complete → [Lab 10](../lab10/STEPS.md)

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Lab 8 validation fails | Complete [Lab 8](../lab8/STEPS.md) Steps 1–10 first |
| `AccessDenied` on IAM review | Confirm `iam:GetRole` / `iam:GetRolePolicy` for your EC2 user (PowerUser) |
| CloudTrail export shows 0 events | Normal if no recent SageMaker API calls; file still validates if `source` is `cloudtrail` |
| Encryption audit `REVIEW` | Confirm Lab 1 buckets use KMS and Lab 5 ECR repo exists |
