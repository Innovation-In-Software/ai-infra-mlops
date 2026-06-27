# Lab 3: Model Training & Fairness Testing

## Class · `ai-mlops-2026-jun30` · **30 min** · **us-west-2**
## Platform · **EC2** + [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) + **bash**
## Prerequisite · [Lab 2](../lab2/STEPS.md) complete
## Working directory · `~/ai-infra-mlops/lab3`
## Outputs · `~/ai-infra-mlops/workspace/lab3/`

> **Scripts:** Runnable scripts will live under `lab3/scripts/`. Full reference content: `Labs_Banking_Edition/Lab_3_Model_Training_and_Fairness_Testing/` in the course repo.

---

# Step 1 — Confirm lab3 in repo

```bash
clear
cd ~/ai-infra-mlops
ls -1 lab3
```

**Expected output:**

```text
STEPS.md
config
images
requirements.txt
scripts
```

**Optional screenshot:** `images/step-01-lab3-folder.png`

---

# Step 2 — Confirm workspace

```bash
clear
cd ~/ai-infra-mlops/lab3
ls -1 ../workspace/lab3 2>/dev/null || echo "Run lab0 Step 10 if missing"
```

**Expected output:**

```text
config
data
logs
models
results
validation
```

**Optional screenshot:** `images/step-02-workspace-lab3.png`

---

# Step 3 — Copy Lab 2 artifacts into workspace

```bash
clear
cd ~/ai-infra-mlops/lab3
mkdir -p ../workspace/lab3/{data,config,models,results,logs,validation}
cp ../workspace/lab2/data/engineered_banking_data.csv ../workspace/lab3/data/
cp ../workspace/lab2/data/anonymized_customers.csv ../workspace/lab3/data/
cp ../workspace/lab2/data/anonymized_transactions.csv ../workspace/lab3/data/
cp ../workspace/lab2/config/feature_metadata.json ../workspace/lab3/config/
cp ../workspace/lab2/config/preprocessor.pkl ../workspace/lab3/config/
ls -1 ../workspace/lab3/data
```

**Expected output:**

```text
anonymized_customers.csv
anonymized_transactions.csv
engineered_banking_data.csv
```

**Optional screenshot:** `images/step-03-prerequisites.png`

---

# Step 4 — Install lab3 packages

```bash
clear
cd ~/ai-infra-mlops/lab3
pip install -r requirements.txt
python3 -c "import sklearn, xgboost, sagemaker; print('Lab 3 imports OK')"
```

**Expected output:**

```text
Lab 3 imports OK
```

**Optional screenshot:** `images/step-04-pip.png`

---

# Step 5 — Load training data

```bash
clear
cd ~/ai-infra-mlops/lab3
python3 scripts/load_training_data.py
```

**Expected output:**

```text
📂 Loading Lab 2 Training Data
============================================================
   ✅ Found: data/engineered_banking_data.csv
   ✅ Found: config/feature_metadata.json
   ✅ Found: config/preprocessor.pkl
   Records: 1000
   Features: 52
✅ Training data prepared
```

**Optional screenshot:** `images/step-05-load-data.png`

---

# Step 6 — Train baseline models

```bash
clear
python3 scripts/train_models.py
```

**Expected output:**

```text
🏦 Training Banking Risk Models
============================================================
   ✅ LogisticRegression — AUC: 0.82
   ✅ RandomForest — AUC: 0.85
   ✅ XGBoost — AUC: 0.87
✅ Model training complete
```

**Optional screenshot:** `images/step-06-train.png`

---

# Step 7 — SageMaker Experiments tracking

```bash
clear
python3 scripts/sagemaker_experiments.py
```

**Expected output:**

```text
📊 SageMaker Experiments
============================================================
   ✅ Experiment: banking-risk-experiments
   ✅ Trial: trial-baseline-xgboost
   ✅ Metrics logged: auc, accuracy, f1
✅ Experiment tracking complete
```

**Optional screenshot:** `images/step-07-experiments.png`

---

# Step 8 — Fairness testing

```bash
clear
python3 scripts/fairness_testing.py
```

**Expected output:**

```text
⚖️ Fairness Testing
============================================================
   Protected attribute: customer_segment
   Disparate impact ratio: 0.91
   Status: PASS (within banking threshold)
✅ Fairness report saved: results/fairness_report.json
```

**Optional screenshot:** `images/step-08-fairness.png`

---

# Step 9 — Select best model

```bash
clear
python3 scripts/select_best_model.py
ls -1 ../workspace/lab3/models
```

**Expected output:**

```text
✅ Best model: XGBoost (AUC 0.87, fairness PASS)
   Saved: models/best_model.pkl
best_model.pkl
```

**Optional screenshot:** `images/step-09-model-select.png`

---

# Step 10 — Validate lab3

```bash
clear
python3 scripts/validate_lab3.py
```

**Expected output:**

```text
Validate Lab 3
============================================================
   ✅ data: engineered_banking_data.csv
   ✅ models: best_model.pkl
   ✅ results: fairness_report.json
   ✅ results: training_report_final.json
Prerequisites OK — proceed to Lab 4
```

**Optional screenshot:** `images/step-10-validate.png`

---

## Lab 3 complete → [Lab 4](../lab4/STEPS.md)
