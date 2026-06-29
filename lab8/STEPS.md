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
whoami   # must be ec2-user
cd ~/ai-infra-mlops/lab7 && python3 scripts/validate_lab7.py
cd ~/ai-infra-mlops/lab1 && python3 scripts/create_banking_iam_roles.py
cd ~/ai-infra-mlops/lab8
```

> **Always run** `create_banking_iam_roles.py` before Lab 8 — SageMaker pipelines need current S3, KMS, PassRole, and tag permissions on `BankingMLEngineerRole`.

**Expected:** `Prerequisites OK — proceed to Lab 8` from Lab 7 validation.

![Lab 7 validation — `python3 scripts/validate_lab7.py`](images/step-00b-lab7-validate.png)

---

## Step 1 — Confirm lab8 folder

**Do this:**

```bash
cd ~/ai-infra-mlops && ls -1 lab8
```

**Expected result:**

```text
STEPS.md
config
images
pipeline
requirements.txt
scripts
```

![Step 1 — `ls -1 lab8`](images/step-01-lab8-folder.png)

---

## Step 2 — Install pipeline dependencies

**Do this:**

```bash
cd ~/ai-infra-mlops/lab8
pip install -r requirements.txt
python3 -c "import sagemaker; print('SageMaker SDK', sagemaker.__version__)"
```

**Expected result:** `SageMaker SDK 2.x.x`

![Step 2 — `pip install` + SageMaker SDK](images/step-02-pip.png)

---

## Step 3 — Define pipeline parameters

**Do this:**

```bash
python3 scripts/define_pipeline_params.py
cat ../workspace/lab8/config/pipeline_params.json | head -12
```

**Expected result:**

```text
   ✅ Input data from Lab 2
   ✅ Uploaded input to s3://banking-mlops-processed-.../lab8-pipeline/input/banking_data.csv
✅ Pipeline parameters defined
```

![Step 3 — `define_pipeline_params.py`](images/step-03-params.png)

---

## Step 4 — Build pipeline definition

**Do this:**

```bash
python3 scripts/build_pipeline.py
```

**Expected result:**

```text
🔧 SageMaker Pipeline
============================================================
   ✅ ProcessingStep: DataValidation
✅ Pipeline definition saved
```

![Step 4 — `build_pipeline.py`](images/step-04-build.png)

---

## Step 5 — Upsert pipeline to SageMaker

**Do this:**

```bash
python3 scripts/upsert_pipeline.py
```

**Expected result:**

```text
   ✅ Pipeline name: banking-ml-pipeline
   ✅ Pipeline ARN: arn:aws:sagemaker:us-west-2:...
✅ Pipeline registered
```

![Step 5 — `upsert_pipeline.py`](images/step-05-upsert.png)

---

## Step 6 — Start pipeline execution

**Do this:**

```bash
python3 scripts/start_pipeline.py
```

**Expected result:**

```text
▶️ Pipeline Execution
============================================================
   Execution ARN: arn:aws:sagemaker:us-west-2:...:pipeline/banking-ml-pipeline/execution/...
✅ Pipeline started and completed successfully
```

**Note:** Processing on `ml.t3.medium` typically takes 5–15 minutes.

![Step 6 — `start_pipeline.py`](images/step-06-execute.png)

---

## Step 7 — Monitor pipeline steps

**Do this:**

```bash
python3 scripts/monitor_pipeline.py
```

**Expected result:**

```text
   DataValidation         ✅ Succeeded
✅ All pipeline steps succeeded
```

![Step 7 — `monitor_pipeline.py`](images/step-07-monitor.png)

---

## Step 8 — Register model in Model Registry

**Do this:**

```bash
python3 scripts/register_model.py
```

**Expected result:**

```text
📋 Model Registry
============================================================
   ✅ Model package group: banking-risk-models
   ✅ Model package ARN: arn:aws:sagemaker:us-west-2:...
✅ Model registered
```

![Step 8 — `register_model.py`](images/step-08-registry.png)

---

## Step 9 — Pipeline compliance report

**Do this:**

```bash
python3 scripts/generate_pipeline_report.py
```

**Expected result:**

```text
✅ Pipeline compliance report generated
```

![Step 9 — `generate_pipeline_report.py`](images/step-09-report.png)

---

## Step 10 — Validate lab8

**Do this:**

```bash
python3 scripts/validate_lab8.py
```

**Expected result:**

```text
Validate Lab 8
============================================================
   ✅ config: pipeline_params.json
   ✅ config: pipeline_registration.json
   ✅ config: pipeline_execution.json
   ✅ config: pipeline_monitor.json
   ✅ config: model_registry.json

============================================================
Prerequisites OK — proceed to Lab 9
```

![Step 10 — `validate_lab8.py`](images/step-10-validate.png)

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Lab 7 validation fails | Complete [Lab 7](../lab7/STEPS.md) Steps 1–10 first |
| `Missing Lab 2 engineered_banking_data.csv` | Run Lab 2 data engineering steps |
| `AccessDenied` on `CreatePipeline` | Re-run `lab1/scripts/create_banking_iam_roles.py` |
| Pipeline execution `Failed` | Run `python3 scripts/start_pipeline.py` again and read the **Step / FailureReason** line. Then `git pull` and re-run `lab1/scripts/create_banking_iam_roles.py` |
| `not authorized to perform: iam:PassRole` | Re-run `lab1/scripts/create_banking_iam_roles.py` |
| `sagemaker:AddTags` denied | Re-run `lab1/scripts/create_banking_iam_roles.py` |
| `ImportError: cannot import name 'LAB5' from 'lab_paths'` | `git pull` — `lab8/scripts/lab_paths.py` must export `LAB5` and `LAB6` workspace paths |
| `Model package not registered` | Run Step 8 after pipeline succeeds; confirm Lab 5 ECR image exists |

---

## Lab 8 complete → [Lab 9](../lab9/STEPS.md)
