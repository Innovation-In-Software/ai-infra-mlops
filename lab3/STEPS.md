# Lab 3: Model Training & Fairness Testing

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30 minutes |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | [Lab 2](../lab2/STEPS.md) |
| **Working directory** | `~/ai-infra-mlops/lab3` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab3/` |

> All commands run in the **VS Code integrated terminal** on EC2. Do not use local Windows PowerShell for lab steps.

> **Quick run:** `python3 scripts/run_lab3.py` runs all script steps in order.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
cd lab3
```

Run `clear` before each step for clean terminal screenshots.

---

## Step 1 — Confirm lab3 in repo

**Do this:**

```bash
clear
cd ~/ai-infra-mlops
ls -1 lab3
```

**Expected result:**

```text
STEPS.md
config
images
requirements.txt
scripts
```


**Screenshot (optional):** `images/step-01-lab3-folder.png`

---

## Step 2 — Confirm workspace

**Do this:**

```bash
clear
cd ~/ai-infra-mlops/lab3
ls -1 ../workspace/lab3 2>/dev/null || echo "Run Lab 0 Step 21 if missing"
```

**Expected result:**

```text
config
data
logs
models
results
validation
```


**Screenshot (optional):** `images/step-02-workspace-lab3.png`

---

## Step 3 — Install lab3 packages

**Do this:**

```bash
clear
cd ~/ai-infra-mlops/lab3
pip install -r requirements.txt
python3 -c "import sklearn, xgboost, sagemaker; print('Lab 3 imports OK')"
```

**Expected result:** `Lab 3 imports OK`


**Screenshot (optional):** `images/step-03-pip.png`

---

## Step 4 — Load training data (copies Lab 2 artifacts)

**Do this:**

```bash
clear
python3 scripts/load_training_data.py
```

**Expected result:**

```text
📂 Loading Lab 2 Training Data
============================================================
   ✅ Copied: engineered_banking_data.csv
   ✅ Copied: anonymized_customers.csv
   ✅ Copied: anonymized_transactions.csv
   ✅ Copied: feature_metadata.json
   ✅ Copied: preprocessor.pkl

   Records: 1000
   Features: 30
   Train: 800 / Test: 200
✅ Training data prepared
```


**Screenshot (optional):** `images/step-04-load-data.png`

---

## Step 5 — Train baseline models

**Do this:**

```bash
clear
python3 scripts/train_models.py
```

**Expected result:**

```text
🏦 Training Banking Risk Models
============================================================
   ✅ LogisticRegression — AUC: 0.83
   ✅ RandomForest — AUC: 1.00
   ✅ XGBoost — AUC: 1.00
✅ Model training complete
```


**Screenshot (optional):** `images/step-05-train.png`

---

## Step 6 — SageMaker Experiments tracking

**Do this:**

```bash
clear
python3 scripts/sagemaker_experiments.py
```

**Expected result:**

```text
📊 SageMaker Experiments
============================================================
   ✅ Experiment: banking-risk-experiments
   ✅ Trial: trial-randomforest-20260628003742
   ✅ Metrics recorded locally: 3 models
   ✅ Metrics logged: auc, accuracy, f1
✅ Experiment tracking complete
```


**Screenshot (optional):** `images/step-06-experiments.png`

---

## Step 7 — Fairness testing

**Do this:**

```bash
clear
python3 scripts/fairness_testing.py
```

**Expected result:**

```text
⚖️ Fairness Testing
============================================================
   Protected attribute: age_group
   Disparate impact ratio: 0.84
   Status: PASS (within banking threshold)
✅ Fairness report saved: results/fairness_report.json
```


**Screenshot (optional):** `images/step-07-fairness.png`

---

## Step 8 — Select best model

**Do this:**

```bash
clear
python3 scripts/select_best_model.py
ls -1 ../workspace/lab3/models
```

**Expected result:**

```text
📋 Banking Model Selection
============================================================
   LogisticRegression: combined=0.895 AUC=0.83
   RandomForest: combined=1.000 AUC=1.00
   XGBoost: combined=1.000 AUC=1.00

✅ Best model: RandomForest (AUC 1.00, fairness PASS)
   Saved: models/best_model.pkl

============================================================
Lab 3 complete.
```


**Screenshot (optional):** `images/step-08-model-select.png`

---

## Step 9 — Validate lab3

**Do this:**

```bash
clear
python3 scripts/validate_lab3.py
```

**Expected result:**

```text
Validate Lab 3
============================================================
   ✅ Lab 2: engineered_banking_data.csv
   ✅ Lab 2: feature_metadata.json
   ✅ data: X_train.csv
   ✅ models: best_model.pkl
   ✅ results: fairness_report.json
   ✅ results: training_report_final.json
   ✅ config: training_results.json

============================================================
Prerequisites OK — proceed to Lab 4
```


**Screenshot (optional):** `images/step-09-validate.png`

---

## Lab 3 complete → [Lab 4](../lab4/STEPS.md)
