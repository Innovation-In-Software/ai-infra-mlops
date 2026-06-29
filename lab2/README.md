# Lab 2: Banking Data Management & PII Protection

**Class:** `ai-mlops-2026-jun30` · **Region:** `us-west-2` · **Duration:** ~30 min

Hands-on steps: [STEPS.md](STEPS.md)

---

## Terms & acronyms (beginners)

| Term | Full form / meaning |
|------|---------------------|
| **PII** | **Personally Identifiable Information** — data that can identify a person (names, SSN, etc.) |
| **S3** | **Simple Storage Service** — AWS object storage (buckets and files) |
| **KMS** | **Key Management Service** — encryption keys for S3 and SageMaker |
| **IAM** | **Identity and Access Management** — roles that control who can access data |
| **SageMaker** | AWS **managed machine learning** platform |
| **Feature Store** | SageMaker service to store and serve **ML features** for training and inference |
| **CSV** | **Comma-Separated Values** — spreadsheet-style data files |
| **ML** | **Machine Learning** |
| **Drift** | When live data or model behavior **changes** from the original training baseline |

---

## Overview

Lab 2 builds the **data layer**: synthetic banking customers and transactions, PII detection and anonymization, quality validation, feature engineering, SageMaker Feature Store, and drift monitoring. Data flows from local CSV files to S3 and Feature Store while maintaining compliance documentation.

Depends on Lab 1 S3 buckets and IAM roles (`workspace/lab1/config/`).

---

## Prerequisites

- Lab 1 — **13/13 COMPLIANT**
- Classroom env: `LAB_NUM_RECORDS=1000`, `LAB_USE_COMPREHEND=0` (from Lab 0)

---

## Lab flow

```
validate_lab2.py (Lab 1 prereqs)
    → generate synthetic banking data
    → PII detection & anonymization
    → data quality validation
    → feature engineering + preprocessor
    → SageMaker Feature Store (2 feature groups)
    → drift baseline
    → compliance documentation
    → validate_lab2.py (final)
```

| Step | Script | Purpose |
|------|--------|---------|
| 4 | `download_banking_data.py` | Generate `customers.csv` and `transactions.csv` with PII fields |
| 5 | `pii_detection_anonymization.py` | Detect PII; write anonymized CSVs; upload PII report to governance bucket |
| 6 | `data_validation.py` | Schema, null, and range checks; quality JSON reports |
| 7 | `feature_engineering.py` | Build `engineered_banking_data.csv`, `preprocessor.pkl`, feature metadata |
| 8 | `feature_store_setup.py` | Create Feature Groups `banking-transaction-features`, `banking-customer-features` |
| 9 | `data_drift_detection.py` | Baseline snapshot for later monitoring |
| 10 | `generate_compliance_doc.py` | Consolidated compliance report |
| 11 | `validate_lab2.py` | Gate to Lab 3 |

**Quick run:** `python3 scripts/run_lab2.py`

---

## Scripts reference

### `download_banking_data.py`

Generates reproducible synthetic banking data (customer demographics, transaction amounts, merchant categories). Writes to `workspace/lab2/data/` and `dataset_metadata.json`.

### `pii_detection_anonymization.py`

Scans for PII columns (names, SSN patterns, account numbers). Applies masking/tokenization. Uploads `pii_report.json` to the Lab 1 governance S3 bucket.

### `data_validation.py`

Runs Great Expectations–style checks (via pandas rules) per dataset. Outputs `data_quality_report_*.json`.

### `feature_engineering.py`

Creates model-ready features: aggregates, encodings, risk indicators. Saves `engineered_banking_data.csv`, `feature_metadata.json`, and `preprocessor.pkl` (used in Labs 3–9).

### `feature_store_setup.py`

Ingests features into SageMaker Feature Store with KMS encryption. **Longest step** (~10 min wait for feature groups). Writes `feature_store_config.json`.

### `data_drift_detection.py`

Stores a baseline distribution file for drift comparison in Lab 7.

### `generate_compliance_doc.py`

Merges PII, quality, and feature metadata into `compliance_report_final.json` for auditors.

### `validate_lab2.py`

Checks Lab 1 configs exist, required data/config files present, Feature Store config valid.

### `lab_paths.py`

Paths helper for `workspace/lab2/`.

### `cleanup_lab2.py`

Instructor reset — clears workspace and optionally deletes Feature Groups (`--aws`).

---

## Configuration & outputs

**Workspace (`workspace/lab2/`):**

| Directory | Key files |
|-----------|-----------|
| `data/` | `customers.csv`, `transactions.csv`, anonymized copies, `engineered_banking_data.csv` |
| `config/` | `pii_report.json`, `feature_metadata.json`, `preprocessor.pkl`, `feature_store_config.json`, `drift_report.json` |
| `data/` | `compliance_report_final.json` |

**AWS:** Feature Groups, S3 uploads to processed/governance buckets.

---

## Architecture role

Lab 2 is the **data layer** (Lab 10). Evidence: `feature_store_config.json`.

---

## Next lab

[Lab 3: Model Training & Fairness Testing](../lab3/README.md)
