# Lab 4: CI/CD Pipeline with Compliance Gates

## Class · `ai-mlops-2026-jun30` · **30 min** · **us-west-2**
## Platform · **EC2** + [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) + **bash**
## Prerequisite · [Lab 3](../lab3/STEPS.md) complete
## Working directory · `~/ai-infra-mlops/lab4`
## Outputs · `~/ai-infra-mlops/workspace/lab4/`

> **Scripts:** `lab4/scripts/` · Run all: `python3 scripts/run_lab4.py`

---

# Step 1 — Confirm lab4 folder

```bash
clear
cd ~/ai-infra-mlops && ls -1 lab4
```

**Expected output:** `Validate Lab 4`, `config`, `images`, `requirements.txt`, `scripts`, `src`, `tests`, `buildspecs`

**Optional screenshot:** `images/step-01-lab4-folder.png`

---

# Step 2 — Copy prior lab artifacts

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

**Expected output:**

```text
best_model.pkl
```

**Optional screenshot:** `images/step-02-artifacts.png`

---

# Step 3 — Install dependencies

```bash
clear
pip install -r requirements.txt
python3 -c "import boto3, pytest; print('Lab 4 imports OK')"
```

**Expected output:** `Lab 4 imports OK`

**Optional screenshot:** `images/step-03-pip.png`

---

# Step 4 — Set up project structure

```bash
clear
python3 scripts/setup_project_structure.py
```

**Expected output:**

```text
   ✅ Created: src/
   ✅ Created: tests/unit/
   ✅ Created: buildspecs/
✅ Banking ML CI/CD project structure ready
```

**Optional screenshot:** `images/step-04-structure.png`

---

# Step 5 — Run unit tests

```bash
clear
python3 -m pytest tests/unit -q
```

**Expected output:**

```text
🔒 Compliance Gates
============================================================
   ✅ PII scan: PASS
   ✅ Fairness threshold: PASS
   ✅ Security lint: PASS
✅ All compliance gates passed
```

**Optional screenshot:** `images/step-05-unit-tests.png`

---

# Step 6 — Compliance gate checks

```bash
clear
python3 scripts/run_compliance_checks.py
```

**Expected output:**

```text
🔄 CodePipeline Setup
============================================================
   ✅ Pipeline: banking-ml-cicd-028417007274
   ✅ Stages: Source → Build → Test → Compliance → Deploy
   ✅ Manual approval gate: enabled
✅ Pipeline configuration saved
```

**Optional screenshot:** `images/step-06-compliance.png`

---

# Step 7 — Configure CodePipeline (classroom mode)

```bash
clear
python3 scripts/setup_codepipeline.py
```

**Expected output:**

```text
   ✅ Source: PASS
   ✅ Build: PASS
   ✅ Test: PASS
   ✅ Compliance: PASS
   ⏸ Manual approval: simulated APPROVED
   ✅ Deploy: PASS (simulation)
✅ Pipeline run complete (simulation)
```

**Optional screenshot:** `images/step-07-pipeline.png`

---

# Step 8 — Simulate pipeline run

```bash
clear
python3 scripts/simulate_pipeline_run.py
```

**Expected output:**

```text
   ✅ Source: PASS
   ✅ Build: PASS
   ✅ Test: PASS
   ✅ Compliance: PASS
   ⏸ Manual approval: simulated APPROVED
✅ Pipeline run complete (simulation)
```

**Optional screenshot:** `images/step-08-simulate.png`

---

# Step 9 — Generate CI/CD compliance report

```bash
clear
python3 scripts/generate_cicd_report.py
cat ../workspace/lab4/artifacts/cicd_compliance_report_final.json | head -20
```

**Expected output:**

```text
✅ CI/CD compliance report generated
{
  "pipeline": "banking-ml-cicd",
  "compliance_gates": "PASS",
  ...
}
```

**Optional screenshot:** `images/step-09-report.png`

---

# Step 10 — Validate lab4

```bash
clear
python3 scripts/validate_lab4.py
```

**Expected output:**

```text
Validate Lab 4
============================================================
   ✅ Lab 1 buckets.json
   ✅ Lab 3 best_model.pkl
   ✅ cicd_compliance_report_final.json
Prerequisites OK — proceed to Lab 5
```

**Optional screenshot:** `images/step-10-validate.png`

---

## Lab 4 complete → [Lab 5](../lab5/STEPS.md)
