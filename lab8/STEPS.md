# Lab 8: End-to-End SageMaker Pipeline

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30 minutes |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | [Lab 7](../lab7/STEPS.md) |
| **Working directory** | `~/ai-infra-mlops/lab8` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab8/` |

> All commands run in the **VS Code integrated terminal** on EC2. Do not use local Windows PowerShell for lab steps.

> **Quick run:** `python3 scripts/run_lab8.py` runs all script steps in order.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
cd lab8
```

Run `clear` before each step for clean terminal screenshots.

---

## Step 1 — Confirm lab8 folder

**Do this:**

```bash
clear
cd ~/ai-infra-mlops && ls -1 lab8
```

**Expected result:** `Validate Lab 8`


**Screenshot (optional):** `images/step-01-lab8-folder.png`

---

## Step 2 — Install pipeline dependencies

**Do this:**

```bash
clear
cd ~/ai-infra-mlops/lab8
pip install -r requirements.txt
python3 -c "import sagemaker; print('SageMaker SDK', sagemaker.__version__)"
```

**Expected result:** `SageMaker SDK 2.x.x`


**Screenshot (optional):** `images/step-02-pip.png`

---

## Step 3 — Define pipeline parameters

**Do this:**

```bash
clear
python3 scripts/define_pipeline_params.py
cat ../workspace/lab8/config/pipeline_params.json | head -12
```

**Expected result:**

```text
✅ Pipeline parameters defined
{
  "region": "us-west-2",
  "instance_type": "ml.m5.large",
  ...
}
```


**Screenshot (optional):** `images/step-03-params.png`

---

## Step 4 — Build pipeline definition

**Do this:**

```bash
clear
python3 scripts/build_pipeline.py
```

**Expected result:**

```text
🔧 SageMaker Pipeline
============================================================
   ✅ ProcessingStep: data-validation
   ✅ TrainingStep: xgboost-training
   ✅ EvaluationStep: model-evaluation
   ✅ RegisterStep: model-registry
✅ Pipeline definition saved
```


**Screenshot (optional):** `images/step-04-build.png`

---

## Step 5 — Upsert pipeline to SageMaker

**Do this:**

```bash
clear
python3 scripts/upsert_pipeline.py --dry-run
```

**Expected result:**

```text
✅ Pipeline name: banking-ml-pipeline
   ✅ Upsert: simulated success
✅ Pipeline registered (dry-run)
```


**Screenshot (optional):** `images/step-05-upsert.png`

---

## Step 6 — Start pipeline execution

**Do this:**

```bash
clear
python3 scripts/start_pipeline.py --dry-run
```

**Expected result:**

```text
▶️ Pipeline Execution
============================================================
   Execution ARN: arn:aws:sagemaker:us-west-2:...:pipeline/banking-ml-pipeline/execution/...
   Status: Executing (simulated)
✅ Pipeline started (dry-run)
```


**Screenshot (optional):** `images/step-06-execute.png`

---

## Step 7 — Monitor pipeline steps

**Do this:**

```bash
clear
python3 scripts/monitor_pipeline.py --dry-run
```

**Expected result:**

```text
data-validation     ✅ Succeeded
   xgboost-training    ✅ Succeeded
   model-evaluation    ✅ Succeeded
   model-registry      ✅ Succeeded
✅ All steps succeeded (simulated)
```


**Screenshot (optional):** `images/step-07-monitor.png`

---

## Step 8 — Register model in Model Registry

**Do this:**

```bash
clear
python3 scripts/register_model.py --dry-run
```

**Expected result:**

```text
📋 Model Registry
============================================================
   ✅ Model package group: banking-risk-models
   ✅ Approval status: PendingManualApproval
✅ Model registered (dry-run)
```


**Screenshot (optional):** `images/step-08-registry.png`

---

## Step 9 — Pipeline compliance report

**Do this:**

```bash
clear
python3 scripts/generate_pipeline_report.py
```

**Expected result:**

```text
✅ Pipeline compliance report generated
   File: results/pipeline_compliance_report_final.json
```


**Screenshot (optional):** `images/step-09-report.png`

---

## Step 10 — Validate lab8

**Do this:**

```bash
clear
python3 scripts/validate_lab8.py
```

**Expected result:**

```text
Validate Lab 8
============================================================
   ✅ pipeline_params.json
   ✅ pipeline_compliance_report_final.json
Prerequisites OK — proceed to Lab 9
```


**Screenshot (optional):** `images/step-10-validate.png`

---

## Lab 8 complete → [Lab 9](../lab9/STEPS.md)
