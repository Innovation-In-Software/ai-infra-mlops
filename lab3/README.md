# Lab 3: Model Training & Fairness Testing

**Class:** `ai-mlops-2026-jun30` · **Module 4:** Model Development and Experiment Tracking · **Duration:** ~30 min (+ optional ~45 min SageMaker)

Hands-on steps: [STEPS.md](STEPS.md)

---

## Terms & acronyms (beginners)

| Term | Full form / meaning |
|------|---------------------|
| **ML** | **Machine Learning** |
| **CI/CD** | **Continuous Integration / Continuous Delivery** — automate build, test, and release |
| **LR** | **Logistic Regression** — simple, interpretable classification model |
| **RF** | **Random Forest** — ensemble of decision trees |
| **XGBoost** | **Extreme Gradient Boosting** — popular high-performance ML algorithm |
| **AUC** | **Area Under the Curve** — classification performance metric (higher is better) |
| **SageMaker** | AWS **managed machine learning** service |
| **S3** | **Simple Storage Service** — where training data is uploaded (optional lab3b) |
| **IAM** | **Identity and Access Management** — permissions for SageMaker jobs |
| **API** | **Application Programming Interface** |
| **Fairness / disparate impact** | Whether model outcomes are **similar across groups** (e.g. age groups) |

---

## Overview

Lab 3 trains **baseline risk models** on Lab 2 engineered data, logs experiments to SageMaker Experiments, runs **fairness testing** across protected groups, and selects the best model for downstream CI/CD and deployment.

The primary path runs on EC2 with scikit-learn/XGBoost. Optional Steps 10–12 use `optional/lab3b/` for a managed SageMaker Processing training job.

---

## Prerequisites

- Lab 2 complete — `validate_lab2.py` passed
- `workspace/lab2/data/engineered_banking_data.csv` and `preprocessor.pkl`

---

## Lab flow

```
pip install → load_training_data.py (train/test splits)
    → train_models.py (LR, RF, XGBoost)
    → sagemaker_experiments.py (experiment tracking)
    → fairness_testing.py (disparate impact)
    → select_best_model.py
    → validate_lab3.py

Optional (lab3b):
    → upload_training_data.py → run_training_job.py → validate_lab3b.py
```

| Step | Script | Output |
|------|--------|--------|
| 4 | `load_training_data.py` | `X_train/test`, `y_train/test`, copies Lab 2 artifacts |
| 5 | `train_models.py` | Three `.pkl` models + `training_results.json` |
| 6 | `sagemaker_experiments.py` | `experiment_tracking.json` (SageMaker Experiments API) |
| 7 | `fairness_testing.py` | `fairness_report.json` (age_group disparate impact) |
| 8 | `select_best_model.py` | `best_model.pkl`, `selection_results.json` |
| 9 | `validate_lab3.py` | Gate to Lab 4 |

**Quick run:** `python3 scripts/run_lab3.py` (Steps 4–8; run Step 9 separately).

---

## Scripts reference

### `load_training_data.py`

Copies engineered data and preprocessor from Lab 2. Performs stratified train/test split. Writes feature name list and split metadata to `config/`.

### `train_models.py`

Trains three classifiers:

- Logistic Regression (interpretable baseline)
- Random Forest (ensemble)
- XGBoost (gradient boosting — typically best performance)

Saves metrics (accuracy, AUC) to `training_results.json` and model files to `models/`.

### `sagemaker_experiments.py`

Creates or reuses experiment `banking-risk-experiments`. Logs parameters and metrics per model run — classroom-safe API usage without full training job cost.

### `fairness_testing.py`

Evaluates predictions across `age_group` buckets. Computes disparate impact ratio; flags if below 0.80 threshold. Output used as a **compliance gate** in Lab 4.

### `select_best_model.py`

Combines performance and fairness scores. Copies winning model to `best_model.pkl` for Labs 4–9.

### `validate_lab3.py`

Verifies splits, models, fairness report, and experiment tracking files exist.

### `lab_paths.py`

Paths under `workspace/lab3/`.

### Optional: `optional/lab3b/scripts/`

| Script | Purpose |
|--------|---------|
| `upload_training_data.py` | Upload train/test CSV to S3 processed bucket |
| `run_training_job.py` | SageMaker Processing job trains `model.joblib` in cloud |
| `patch_iam_for_sagemaker.py` | IAM helper for processing job role |
| `validate_lab3b.py` | Confirms S3 output artifact exists |

---

## Configuration & outputs

**Workspace (`workspace/lab3/`):**

| Path | Purpose |
|------|---------|
| `data/X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv` | Training splits |
| `models/*.pkl` | Trained models |
| `models/best_model.pkl` | Selected model for deployment |
| `config/training_results.json` | Metrics per algorithm |
| `config/experiment_tracking.json` | SageMaker experiment run IDs |
| `results/fairness_report.json` | Fairness audit |
| `results/training_report_final.json` | Final selection summary |

---

## Architecture role

Lab 3 is the **training layer** (Lab 10). Evidence: `training_results.json`.

---

## Next lab

[Lab 4: CI/CD Pipeline with Compliance Gates](../lab4/README.md)
