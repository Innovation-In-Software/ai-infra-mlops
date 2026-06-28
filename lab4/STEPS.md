# Lab 4: CI/CD Pipeline with Compliance Gates

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30 minutes |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | [Lab 3](../lab3/STEPS.md) |
| **Working directory** | `~/ai-infra-mlops/lab4` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab4/` |

> All commands run in the **VS Code integrated terminal** on EC2. Do not use local Windows PowerShell for lab steps.

> **Quick run:** `python3 scripts/run_lab4.py` runs all script steps in order.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
cd lab4
```

Run `clear` before each step for clean terminal screenshots.

---

## Step 1 — Confirm lab4 folder

**Do this:**

```bash
clear
cd ~/ai-infra-mlops && ls -1 lab4
```

**Expected result:** `Validate Lab 4`


**Screenshot (optional):** `images/step-01-lab4-folder.png`

---

## Step 2 — Copy prior lab artifacts

**Do this:**

```bash
clear
cd ~/ai-infra-mlops/lab4
mkdir -p ../workspace/lab4/{config,models,results,artifacts,logs}
cp ../workspace/lab1/config/buckets.json ../workspace/lab4/config/
cp ../workspace/lab1/config/iam_roles.json ../workspace/lab4/config/
cp ../workspace/lab3/models/best_model.pkl ../workspace/lab4/models/
cp ../workspace/lab3/results/fairness_report.json ../workspace/lab4/results/
ls -1 ../workspace/lab4/models
```

**Expected result:** `best_model.pkl`


**Screenshot (optional):** `images/step-02-artifacts.png`

---

## Step 3 — Install dependencies

**Do this:**

```bash
clear
pip install -r requirements.txt
python3 -c "import boto3, pytest; print('Lab 4 imports OK')"
```

**Expected result:** `Lab 4 imports OK`


**Screenshot (optional):** `images/step-03-pip.png`

---

## Step 4 — Set up project structure

**Do this:**

```bash
clear
python3 scripts/setup_project_structure.py
```

**Expected result:**

```text
✅ Created: src/
   ✅ Created: tests/unit/
   ✅ Created: buildspecs/
✅ Banking ML CI/CD project structure ready
```


**Screenshot (optional):** `images/step-04-structure.png`

---

## Step 5 — Run unit tests

**Do this:**

```bash
clear
python3 -m pytest tests/unit -q
```

**Expected result:**

```text
🔒 Compliance Gates
============================================================
   ✅ PII scan: PASS
   ✅ Fairness threshold: PASS
   ✅ Security lint: PASS
✅ All compliance gates passed
```


**Screenshot (optional):** `images/step-05-unit-tests.png`

---

## Step 6 — Compliance gate checks

**Do this:**

```bash
clear
python3 scripts/run_compliance_checks.py
```

**Expected result:**

```text
🔄 CodePipeline Setup
============================================================
   ✅ Pipeline: banking-ml-cicd-028417007274
   ✅ Stages: Source → Build → Test → Compliance → Deploy
   ✅ Manual approval gate: enabled
✅ Pipeline configuration saved
```


**Screenshot (optional):** `images/step-06-compliance.png`

---

## Step 7 — Configure CodePipeline (classroom mode)

**Do this:**

```bash
clear
python3 scripts/setup_codepipeline.py
```

**Expected result:**

```text
✅ Source: PASS
   ✅ Build: PASS
   ✅ Test: PASS
   ✅ Compliance: PASS
   ⏸ Manual approval: simulated APPROVED
   ✅ Deploy: PASS (simulation)
✅ Pipeline run complete (simulation)
```


**Screenshot (optional):** `images/step-07-pipeline.png`

---

## Step 8 — Simulate pipeline run

**Do this:**

```bash
clear
python3 scripts/simulate_pipeline_run.py
```

**Expected result:**

```text
✅ Source: PASS
   ✅ Build: PASS
   ✅ Test: PASS
   ✅ Compliance: PASS
   ⏸ Manual approval: simulated APPROVED
✅ Pipeline run complete (simulation)
```


**Screenshot (optional):** `images/step-08-simulate.png`

---

## Step 9 — Generate CI/CD compliance report

**Do this:**

```bash
clear
python3 scripts/generate_cicd_report.py
cat ../workspace/lab4/artifacts/cicd_compliance_report_final.json | head -20
```

**Expected result:**

```text
✅ CI/CD compliance report generated
{
  "pipeline": "banking-ml-cicd",
  "compliance_gates": "PASS",
  ...
}
```


**Screenshot (optional):** `images/step-09-report.png`

---

## Step 10 — Validate lab4

**Do this:**

```bash
clear
python3 scripts/validate_lab4.py
```

**Expected result:**

```text
Validate Lab 4
============================================================
   ✅ Lab 1 buckets.json
   ✅ Lab 3 best_model.pkl
   ✅ cicd_compliance_report_final.json
Prerequisites OK — proceed to Lab 5
```


**Screenshot (optional):** `images/step-10-validate.png`

---

## Lab 4 complete → [Lab 5](../lab5/STEPS.md)
