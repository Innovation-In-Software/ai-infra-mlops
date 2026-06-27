# Lab 8: End-to-End SageMaker Pipeline

## Class · `ai-mlops-2026-jun30` · **30 min** · **us-west-2**
## Platform · **EC2** + [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) + **bash**
## Prerequisite · [Lab 7](../lab7/STEPS.md) complete
## Working directory · `~/ai-infra-mlops/lab8`
## Outputs · `~/ai-infra-mlops/workspace/lab8/`

---

# Step 1 — Confirm lab8 folder

```bash
clear
cd ~/ai-infra-mlops && ls -1 lab8
```

**Expected output:** `STEPS.md`, `config`, `images`, `pipeline`, `requirements.txt`, `scripts`

**Optional screenshot:** `images/step-01-lab8-folder.png`

---

# Step 2 — Install pipeline dependencies

```bash
clear
cd ~/ai-infra-mlops/lab8
pip install -r requirements.txt
python3 -c "import sagemaker; print('SageMaker SDK', sagemaker.__version__)"
```

**Expected output:**

```text
SageMaker SDK 2.x.x
```

**Optional screenshot:** `images/step-02-pip.png`

---

# Step 3 — Define pipeline parameters

```bash
clear
python3 scripts/define_pipeline_params.py
cat ../workspace/lab8/config/pipeline_params.json | head -12
```

**Expected output:**

```text
✅ Pipeline parameters defined
{
  "region": "us-west-2",
  "instance_type": "ml.m5.large",
  ...
}
```

**Optional screenshot:** `images/step-03-params.png`

---

# Step 4 — Build pipeline definition

```bash
clear
python3 scripts/build_pipeline.py
```

**Expected output:**

```text
🔧 SageMaker Pipeline
============================================================
   ✅ ProcessingStep: data-validation
   ✅ TrainingStep: xgboost-training
   ✅ EvaluationStep: model-evaluation
   ✅ RegisterStep: model-registry
✅ Pipeline definition saved
```

**Optional screenshot:** `images/step-04-build.png`

---

# Step 5 — Upsert pipeline to SageMaker

```bash
clear
python3 scripts/upsert_pipeline.py --dry-run
```

**Expected output:**

```text
   ✅ Pipeline name: banking-ml-pipeline
   ✅ Upsert: simulated success
✅ Pipeline registered (dry-run)
```

**Optional screenshot:** `images/step-05-upsert.png`

---

# Step 6 — Start pipeline execution

```bash
clear
python3 scripts/start_pipeline.py --dry-run
```

**Expected output:**

```text
▶️ Pipeline Execution
============================================================
   Execution ARN: arn:aws:sagemaker:us-west-2:...:pipeline/banking-ml-pipeline/execution/...
   Status: Executing (simulated)
✅ Pipeline started (dry-run)
```

**Optional screenshot:** `images/step-06-execute.png`

---

# Step 7 — Monitor pipeline steps

```bash
clear
python3 scripts/monitor_pipeline.py --dry-run
```

**Expected output:**

```text
   data-validation     ✅ Succeeded
   xgboost-training    ✅ Succeeded
   model-evaluation    ✅ Succeeded
   model-registry      ✅ Succeeded
✅ All steps succeeded (simulated)
```

**Optional screenshot:** `images/step-07-monitor.png`

---

# Step 8 — Register model in Model Registry

```bash
clear
python3 scripts/register_model.py --dry-run
```

**Expected output:**

```text
📋 Model Registry
============================================================
   ✅ Model package group: banking-risk-models
   ✅ Approval status: PendingManualApproval
✅ Model registered (dry-run)
```

**Optional screenshot:** `images/step-08-registry.png`

---

# Step 9 — Pipeline compliance report

```bash
clear
python3 scripts/generate_pipeline_report.py
```

**Expected output:**

```text
✅ Pipeline compliance report generated
   File: results/pipeline_compliance_report_final.json
```

**Optional screenshot:** `images/step-09-report.png`

---

# Step 10 — Validate lab8

```bash
clear
python3 scripts/validate_lab8.py
```

**Expected output:**

```text
Validate Lab 8
============================================================
   ✅ config: pipeline_params.json
   ✅ results: pipeline_compliance_report_final.json
Prerequisites OK — proceed to Lab 9
```

**Optional screenshot:** `images/step-10-validate.png`

---

## Lab 8 complete → [Lab 9](../lab9/STEPS.md)
