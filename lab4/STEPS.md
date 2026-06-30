# Lab 4: CI/CD Pipeline with Compliance Gates

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30 minutes (Steps 1–10) · ~45 minutes (Steps 11–15, CodePipeline on AWS) |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | [Lab 3](../lab3/STEPS.md) complete — Steps 1–12 (Step 9 minimum for local model; Step 12 for SageMaker) |
| **Working directory** | `~/ai-infra-mlops/lab4` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab4/` |

> **Run Steps 1–10 once, in order.** Run each command block below, then compare your terminal to the screenshot under that step.  
> All commands run in the **VS Code terminal on EC2** (`whoami` = `ec2-user`). Do not use Windows PowerShell on the ProTech VM.

> **Quick run (scripts only):** `python3 scripts/run_lab4.py` runs Steps 4–9 logic but **not** Step 2 (artifact copy) or Step 5 (pytest). Always finish with Step 10.

---

## Before you start

1. Connect VS Code to EC2 ([Lab 0 Step 13](../lab0/STEPS.md)).
2. Pull the latest course repo:

```bash
cd ~/ai-infra-mlops && git pull
whoami
```

**Expected:** `ec2-user`

![git pull — `cd ~/ai-infra-mlops && git pull`](images/step-00a-git-pull.png)

3. Confirm Lab 3 outputs exist:

```bash
cd ~/ai-infra-mlops/lab3 && python3 scripts/validate_lab3.py
```

**Expected:** All prerequisites show ✅ and `Prerequisites OK — proceed to Lab 4`.

![Lab 3 validation — `python3 scripts/validate_lab3.py`](images/step-00b-lab3-validate.png)

4. Go to Lab 4:

```bash
cd ~/ai-infra-mlops/lab4
```

---

## Lab 4 roadmap

| Step | What you create |
|------|-----------------|
| **1–3** | Confirm repo, copy prior lab artifacts, install packages |
| **4** | CI/CD project folders (`src/`, `tests/`, `buildspecs/`) |
| **5** | Unit tests — verify Labs 1–3 prerequisites |
| **6** | Compliance gates (PII, fairness, security lint) |
| **7** | CodePipeline config (classroom simulation with your account ID) |
| **8** | Simulated pipeline run through deploy |
| **9** | CI/CD compliance report JSON |
| **10** | Lab 4 validation (local CI/CD simulation) |
| **11–15** | **Real CodePipeline on AWS** (S3 → CodeBuild → validate) |

---

# Step 1 — Confirm lab4 folder

**What you do:** Verify the Lab 4 course files are in the repo.

```bash
cd ~/ai-infra-mlops
ls -1 lab4
```

**Expected:**

```text
STEPS.md
buildspecs
config
images
requirements.txt
scripts
src
tests
```

![Step 1 — `ls -1 lab4` (Step 2 copy commands are below in the same capture)](images/step-01-lab4-folder.png)

---

# Step 2 — Copy prior lab artifacts

**What you do:** Create Lab 4 workspace folders and copy config/model/fairness files from Labs 1 and 3.

```bash
cd ~/ai-infra-mlops/lab4
mkdir -p ../workspace/lab4/{config,models,results,artifacts,logs}
cp ../workspace/lab1/config/buckets.json ../workspace/lab4/config/
cp ../workspace/lab1/config/iam_roles.json ../workspace/lab4/config/
cp ../workspace/lab3/models/best_model.pkl ../workspace/lab4/models/
cp ../workspace/lab3/results/fairness_report.json ../workspace/lab4/results/
ls -1 ../workspace/lab4/models
```

**Expected:**

```text
best_model.pkl
```

> Step 5 unit tests also read **Lab 2** `pii_report.json` directly from `workspace/lab2/config/` (not copied here). Complete [Lab 2](../lab2/STEPS.md) if that file is missing.

![Step 2 — artifact copy and `ls -1 ../workspace/lab4/models` (same screenshot as Step 1 — scroll down)](images/step-02-artifacts.png)

---

# Step 3 — Install lab4 packages

**What you do:** Install CI/CD and testing dependencies.

```bash
cd ~/ai-infra-mlops/lab4
python3 -m pip install -r requirements.txt
python3 -c "import boto3, pytest; print('Lab 4 imports OK')"
```

**Expected:** `Lab 4 imports OK`

> If you completed [Lab 0 Step 17.5](../lab0/STEPS.md), packages may already be installed — re-running `python3 -m pip install` is safe.

![Step 3 — `python3 -m pip install -r requirements.txt` and `Lab 4 imports OK`](images/step-03-pip.png)

---

# Step 4 — Set up project structure

**What you do:** Ensure CI/CD directories exist under `lab4/`.

```bash
python3 scripts/setup_project_structure.py
```

**Expected:**

```text
   ✅ Created: src/
   ✅ Created: tests/unit/
   ✅ Created: buildspecs/
✅ Banking ML CI/CD project structure ready
```

![Step 4 — `python3 scripts/setup_project_structure.py` (same capture as Step 5 — scroll up)](images/step-04-structure.png)

---

# Step 5 — Run unit tests

**What you do:** Run pytest checks that Labs 1–3 artifacts are in place before the pipeline runs.

```bash
python3 -m pytest tests/unit -q
```

**Expected:**

```text
.....
5 passed in 0.02s
```

The five tests verify: Lab 1 `buckets.json` and `iam_roles.json`, Lab 2 `pii_report.json`, Lab 3 `best_model.pkl`, and fairness status `PASS`.

> If you see **`1 passed`** instead of five, run `cd ~/ai-infra-mlops && git pull` and re-run pytest — you need the updated `test_compliance.py` from the course repo.

![Step 5 — `python3 -m pytest tests/unit -q` showing `5 passed` (after `git pull`; ignore `1 passed` from the earlier run in the same capture)](images/step-05-unit-tests.png)

---

# Step 6 — Compliance gate checks

**What you do:** Run PII, fairness, and security lint gates (classroom simulation).

```bash
python3 scripts/run_compliance_checks.py
```

**Expected:**

```text
🔒 Compliance Gates
============================================================
   ✅ PII scan: PASS
   ✅ Fairness threshold: PASS
   ✅ Security lint: PASS
✅ All compliance gates passed
```

If Lab 2 is incomplete, PII may show `⚠️ WARN` — finish Lab 2 first for a full PASS.

![Step 6 — `python3 scripts/run_compliance_checks.py` (scroll down in the same capture for Step 7 CodePipeline)](images/step-06-compliance.png)

---

# Step 7 — Configure CodePipeline (classroom mode)

**What you do:** Save a CodePipeline config JSON using your AWS account ID (no pipeline created in the console).

```bash
python3 scripts/setup_codepipeline.py
```

**Expected:**

```text
🔄 CodePipeline Setup
============================================================
   ✅ Pipeline: banking-ml-cicd-<your-account-id>
   ✅ Stages: Source → Build → Test → Compliance → Deploy
   ✅ Manual approval gate: enabled
✅ Pipeline configuration saved
```

`<your-account-id>` is a 12-digit number from STS — unique to your EC2 role.

![Step 7 — `python3 scripts/setup_codepipeline.py` (same screenshot as Step 6 — scroll down)](images/step-07-pipeline.png)

---

# Step 8 — Simulate pipeline run

**What you do:** Walk through Source → Deploy stages and record a simulation JSON.

```bash
python3 scripts/simulate_pipeline_run.py
```

**Expected:**

```text
🔄 Pipeline Run Simulation
============================================================
   ✅ Source: PASS
   ✅ Build: PASS
   ✅ Test: PASS
   ✅ Compliance: PASS
   ⏸ Manual approval: simulated APPROVED
   ✅ Deploy: PASS (simulation)
✅ Pipeline run complete (simulation)
```

![Step 8 — `python3 scripts/simulate_pipeline_run.py`](images/step-08-simulate.png)

---

# Step 9 — Generate CI/CD compliance report

**What you do:** Write the final compliance report and preview it.

```bash
python3 scripts/generate_cicd_report.py
cat ../workspace/lab4/artifacts/cicd_compliance_report_final.json | head -20
```

**Expected:**

```text
✅ CI/CD compliance report generated
{
  "timestamp": "2026-...",
  "pipeline": "banking-ml-cicd",
  "compliance_gates": "PASS",
  "audit_trail": "simulated"
}
```

![Step 9 — report generation and `cat ... | head -20` (scroll down in the same capture for Step 10 validate)](images/step-09-report.png)

---

# Step 10 — Validate lab4

**What you do:** Confirm Lab 4 prerequisites and outputs.

```bash
python3 scripts/validate_lab4.py
```

**Expected:**

```text
Validate Lab 4
============================================================
   ✅ Lab 1 buckets.json
   ✅ Lab 3 best_model.pkl
   ✅ config: compliance_gates.json
   ✅ config: codepipeline_config.json
   ✅ artifacts: pipeline_run_simulation.json
   ✅ cicd_compliance_report_final.json

============================================================
Prerequisites OK — proceed to Step 11
```

![Step 10 — `python3 scripts/validate_lab4.py` (same screenshot as Step 9 — scroll down)](images/step-10-validate.png)

---

# Step 11 — Package and upload pipeline source (AWS)

**What you do:** Build a zip of pipeline source and upload to your banking models bucket.

```bash
cd ~/ai-infra-mlops/optional/lab4b
python3 -m pip install -r requirements.txt
python3 scripts/package_source.py
```

**Expected:**

```text
📦 Package pipeline source for S3
============================================================
   ✅ Uploaded: s3://bank-mlops-<account-id>-models/cicd/lab4b/source.zip
✅ Source artifact ready for CodePipeline
```

---

# Step 12 — Create CodeBuild project (AWS)

```bash
python3 scripts/create_codebuild.py
```

**Expected:**

```text
🔧 CodeBuild project (Lab 4b)
============================================================
   ✅ Created IAM role: BankingLab4bCodeBuildRole
   ✅ Created CodeBuild project: banking-ml-cicd-build-lab4b
✅ CodeBuild ready
```

On re-run: `exists` / `Updated` messages are OK.

---

# Step 13 — Create CodePipeline (AWS)

```bash
python3 scripts/create_codepipeline.py
```

**Expected:**

```text
🔄 CodePipeline (Lab 4b — LIVE AWS)
============================================================
   ✅ Created pipeline: banking-ml-cicd-lab4b-<account-id>
✅ CodePipeline visible in AWS console
```

**Console:** [CodePipeline](https://us-west-2.console.aws.amazon.com/codesuite/codepipeline/pipelines)

![Steps 11–13 — package, CodeBuild, CodePipeline](../optional/lab4b/images/step-01-03-setup.png)

---

# Step 14 — Run the pipeline (AWS)

```bash
python3 scripts/start_pipeline.py
```

**Expected:**

```text
▶ Start CodePipeline execution
============================================================
   ✅ Started execution: <uuid>
   ... status: Succeeded
✅ Pipeline execution succeeded
```

First run may take **5–10 minutes**. If Source stage fails with a permissions error:

```bash
python3 scripts/patch_iam_for_lab4b.py
sleep 30
python3 scripts/start_pipeline.py
```

![Step 14 — pipeline execution **Succeeded**](../optional/lab4b/images/step-04-pipeline-succeeded.png)

---

# Step 15 — Validate CodePipeline

```bash
python3 scripts/validate_lab4b.py
```

**Expected:**

```text
Validate Lab 4b (CodePipeline)
============================================================
   ✅ Pipeline in AWS: banking-ml-cicd-lab4b-<account-id>
   ✅ Status: Succeeded
============================================================
Lab 4b OK — real CodePipeline ran in AWS
```

![Step 15 — `validate_lab4b.py` OK](../optional/lab4b/images/step-05-validate-ok.png)

| | Steps 1–10 | Steps 11–15 |
|---|------------|-------------|
| CodePipeline in console | **No** (JSON simulation) | **Yes** |
| CodeBuild | No | Yes — runs `compliance_check.py` |

> **Do not delete the pipeline during this lab** — you need it for later steps and console review. Optional AWS cleanup is [Lab 10 Step 11](../lab10/STEPS.md) after all labs.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `whoami` = `Administrator` | Reconnect VS Code Remote-SSH to EC2 ([Lab 0 Step 13](../lab0/STEPS.md)) |
| `pytest` shows **`1 passed`** (not five) | Run `git pull` on EC2 — old stub test; you need commit `79e6907` or later |
| `pytest` shows 1–2 failures on Lab 1 configs | Complete [Lab 1](../lab1/STEPS.md) — `buckets.json` and `iam_roles.json` must exist in `workspace/lab1/config/` |
| `test_lab2_pii_report` fails | Complete [Lab 2](../lab2/STEPS.md) Step 6 (`pii_scan.py`) |
| `test_lab3_fairness_pass` fails | Re-run [Lab 3](../lab3/STEPS.md) Step 7 (`fairness_testing.py`) |
| `cp: cannot stat ... best_model.pkl` | Complete Lab 3 Step 8 before Lab 4 Step 2 |
| `Unable to locate credentials` on Step 7 | EC2 instance needs an IAM role with `sts:GetCallerIdentity` ([Lab 0](../lab0/STEPS.md)) |
| `⚠️ not yet created` on Step 10 | Run Steps 6–9 before validating |
| Screenshot shows the **next** step's command at the bottom | Normal — captures were taken in one continuous terminal session |
| `PythonDeprecationWarning` | [Lab 0 Step 17](../lab0/STEPS.md) — upgrade to Python 3.11 |
| Source stage **Failed** (Step 14) | Run `python3 scripts/patch_iam_for_lab4b.py` in `optional/lab4b`, wait 30s, re-run Steps 13–14 |
| `PipelineExecutionNotFoundException` (Step 14) | `git pull` for latest `start_pipeline.py` |
| `AccessDenied` on `create_pipeline` | EC2 role needs CodePipeline/CodeBuild/IAM permissions |

---

## Appendix — Fresh start (optional)

**Reset Lab 4 workspace only:**

```bash
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab4
cd lab4
```

Then re-run **Steps 2–15**. Labs 1–3 artifacts in `workspace/lab1/` … `lab3/` are unchanged.

**Quick run (Steps 1–10 scripts):** `python3 scripts/run_lab4.py` — then run Steps 2, 5, 10, and **11–15** manually.

---

## Lab 4 complete → [Lab 5](../lab5/STEPS.md)
