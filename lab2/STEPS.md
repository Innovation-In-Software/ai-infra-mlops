# Lab 2: Banking Data Management & PII Protection

## Class · `ai-mlops-2026-jun30` · **30 min** · **us-west-2**
## Platform · **EC2** + [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) + **bash**
## Prerequisite · [Lab 1](../lab1/STEPS.md) — `Compliance Score: 100%`
## Working directory · `~/ai-infra-mlops/lab2`
## Outputs · `~/ai-infra-mlops/workspace/lab2/`

---

## Classroom env (run once per session)

```bash
export LAB_NUM_RECORDS=1000
export LAB_USE_COMPREHEND=0
```

---

## Fresh start

```bash
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab2
cd lab2 && python3 scripts/cleanup_lab2.py --aws   # if re-running Feature Store
```

---

# Step 1 — Confirm lab2 in repo

```bash
clear
cd ~/ai-infra-mlops
ls -1 lab2
```

**Expected output:** `Validate Lab 2`, `config`, `images`, `requirements.txt`, `scripts`

**Optional screenshot:** `images/step-01-lab2-folder.png`

---

# Step 2 — Confirm workspace

```bash
clear
cd ~/ai-infra-mlops/lab2
ls -1 ../workspace/lab2
```

**Expected output:** `config`, `data`, `logs`, `results`, `validation`

**Optional screenshot:** `images/step-02-workspace-lab2.png`

---

# Step 3 — Verify Lab 1 prerequisites

```bash
clear
python3 scripts/validate_lab2.py
cd ../lab1 && python3 scripts/validate_environment.py && cd ../lab2
```

**Expected output:**

```text
Validate Lab 2
============================================================
   ✅ Lab 1 config: buckets.json
   ✅ Lab 1 config: iam_roles.json
   ⚠️ not yet created: customers.csv
   ...
Prerequisites OK — run lab2 scripts in STEPS.md order.

Compliance Score: 100.0%
Status: COMPLIANT
✅ ALL CHECKS PASSED! Environment is compliant.
```

**Optional screenshot:** `images/step-03-prerequisites.png`

---

# Step 4 — Generate banking dataset

```bash
clear
python3 scripts/download_banking_data.py
```

**Expected output:**

```text
🏦 Generating Banking Transaction Dataset
   Records: 1000 (set LAB_NUM_RECORDS to change)
✅ Generated 100 customer records
✅ Generated 1000 transaction records
✅ Dataset metadata saved
```

Files: `workspace/lab2/data/customers.csv`, `transactions.csv`

**Optional screenshot:** `images/step-04-dataset.png`

---

# Step 5 — PII detection & anonymization

```bash
clear
python3 scripts/pii_detection_anonymization.py
```

**Expected output:**

```text
🏦 Processing Banking Data with PII Protection
   Detection mode: patterns only (classroom mode)
...
✅ PII Detection and Anonymization Complete!
   Total PII Instances Anonymized: 3700
✅ Banking Data Processing Complete!
```

Files: `anonymized_customers.csv`, `anonymized_transactions.csv`, `config/pii_*.json`

**Optional screenshot:** `images/step-05-pii.png`

---

# Step 6 — Data validation

```bash
clear
python3 scripts/data_validation.py
```

**Expected output:**

```text
✅ Data Validation Complete!
   Customer Quality Score: 57.1%
   Transaction Quality Score: 70.0%
```

Reports: `config/data_quality_report_*.json`

**Optional screenshot:** `images/step-06-validation.png`

---

# Step 7 — Feature engineering

```bash
clear
python3 scripts/feature_engineering.py
```

**Expected output:**

```text
✅ Feature Engineering Complete!
   Training Data: .../data/engineered_banking_data.csv
   Feature Pipeline: .../config/preprocessor.pkl
   Feature Metadata: .../config/feature_metadata.json
```

**Optional screenshot:** `images/step-07-features.png`

---

# Step 8 — SageMaker Feature Store

```bash
clear
python3 scripts/feature_store_setup.py
```

**Expected output:**

```text
🏦 Setting Up Banking Feature Store
   ✅ Feature group created: banking-transaction-features
   ⏳ Waiting for banking-transaction-features to become active...
   ✅ Feature group active: banking-transaction-features
   ...
   ✅ Ingested 1000 records into banking-transaction-features
   ✅ Ingested 100 records into banking-customer-features
✅ Feature Store Setup Complete!
```

Config: `config/feature_store_config.json` · **~5–15 min**

**Optional screenshot:** `images/step-08-feature-store.png`

---

# Step 9 — Drift detection

```bash
clear
python3 scripts/data_drift_detection.py
```

**Expected output:**

```text
📊 Drift Detection Summary:
   Total Features: 50
   Features with Drift: 0
   Drift Percentage: 0.0%
   Status: NORMAL
✅ Drift Detection Complete!
```

**Optional screenshot:** `images/step-09-drift.png`

---

# Step 10 — Compliance report

```bash
clear
python3 scripts/generate_compliance_doc.py
```

**Expected output:**

```text
📋 COMPLIANCE REPORT SUMMARY
============================================================
✅ PII Protection: 3700 instances anonymized
✅ Features Managed: 52
✅ Drift Monitoring: NORMAL
```

File: `data/compliance_report_final.json`

Or all steps: `python3 scripts/run_lab2.py`

**Optional screenshot:** `images/step-10-compliance.png`

---

# Step 11 — Final validation

```bash
clear
python3 scripts/validate_lab2.py
ls -1 ../workspace/lab2/data
ls -1 ../workspace/lab2/config
```

**Expected output:**

```text
Validate Lab 2
============================================================
   ✅ Lab 1 config: buckets.json
   ✅ Lab 1 config: iam_roles.json
   ✅ data: customers.csv
   ✅ data: transactions.csv
   ✅ data: anonymized_customers.csv
   ✅ data: anonymized_transactions.csv
   ✅ data: engineered_banking_data.csv
   ✅ data: compliance_report_final.json
   ✅ config: dataset_metadata.json
   ✅ config: pii_report.json
   ✅ config: pii_compliance_report.json
   ✅ config: feature_metadata.json
   ✅ config: feature_store_config.json
   ✅ config: drift_report.json
   ✅ config: data_quality_report_customers.json
   ✅ config: data_quality_report_transactions.json

============================================================
Prerequisites OK — run lab2 scripts in STEPS.md order.
```

**Optional screenshot:** `images/step-11-validate.png`

---

## Lab 2 complete → [Lab 3](../lab3/STEPS.md)
