# Lab 5: Secure Containerization for Banking

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30 minutes |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | [Lab 4](../lab4/STEPS.md) |
| **Working directory** | `~/ai-infra-mlops/lab5` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab5/` |

> All commands run in the **VS Code integrated terminal** on EC2. Do not use local Windows PowerShell for lab steps.

> **Quick run:** `python3 scripts/run_lab5.py` runs all script steps in order.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
cd lab5
```

Run `clear` before each step for clean terminal screenshots.

---

## Step 1 — Confirm lab5 folder

**Do this:**

```bash
clear
cd ~/ai-infra-mlops && ls -1 lab5
```

**Expected result:** `Validate Lab 5`


**Screenshot (optional):** `images/step-01-lab5-folder.png`

---

## Step 2 — Verify Docker

**Do this:**

```bash
clear
docker --version
docker ps
```

**Expected result:**

```text
Docker version 25.x.x, build ...
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```


**Screenshot (optional):** `images/step-02-docker.png`

---

## Step 3 — Prepare model artifacts

**Do this:**

```bash
clear
cd ~/ai-infra-mlops/lab5
pip install -r requirements.txt
python3 scripts/prepare_artifacts.py
ls -1 ../workspace/lab5/models
```

**Expected result:**

```text
✅ Copied: best_model.pkl
   ✅ Copied: preprocessor.pkl
   ✅ Copied: feature_metadata.json
best_model.pkl
preprocessor.pkl
```


**Screenshot (optional):** `images/step-03-artifacts.png`

---

## Step 4 — Build container image

**Do this:**

```bash
clear
bash scripts/build_container.sh
```

**Expected result:**

```text
🔍 Container Scan
============================================================
   Critical: 0
   High: 0
   Status: PASS (banking threshold)
✅ Scan report saved
✅ Container compliance report generated

Lab 5 complete.
```


**Screenshot (optional):** `images/step-04-build.png`

---

## Step 5 — Test container locally

**Do this:**

```bash
clear
python3 scripts/test_container.py
```

**Expected result:**

```text
🧪 Container Inference Test
============================================================
   ✅ Health check: 200 OK
   ✅ Sample prediction: risk_score=0.23
✅ Container tests passed
```


**Screenshot (optional):** `images/step-05-test.png`

---

## Step 6 — Create ECR repository

**Do this:**

```bash
clear
python3 scripts/create_ecr_repo.py
```

**Expected result:**

```text
📦 ECR Repository
============================================================
   ✅ Repository: banking-ml-inference
   ✅ Encryption: KMS
   ✅ Scan on push: enabled
✅ ECR repository ready
```


**Screenshot (optional):** `images/step-06-ecr.png`

---

## Step 7 — Push image to ECR

**Do this:**

```bash
clear
bash scripts/push_to_ecr.sh
```

**Expected result:**

```text
✅ Login to ECR succeeded
   ✅ Pushed: <account-id>.dkr.ecr.us-west-2.amazonaws.com/banking-ml-inference:latest
✅ Image push complete
```


**Screenshot (optional):** `images/step-07-push.png`

---

## Step 8 — Vulnerability scan

**Do this:**

```bash
clear
python3 scripts/scan_container.py
```

**Expected result:**

```text
🔍 Container Scan
============================================================
   Critical: 0
   High: 0
   Status: PASS (banking threshold)
✅ Scan report saved
```


**Screenshot (optional):** `images/step-08-scan.png`

---

## Step 9 — Compliance report

**Do this:**

```bash
clear
python3 scripts/generate_container_report.py
```

**Expected result:**

```text
✅ Container compliance report generated
   Manifest: validation/container_deployment_manifest.json
```


**Screenshot (optional):** `images/step-09-report.png`

---

## Step 10 — Validate lab5

**Do this:**

```bash
clear
python3 scripts/validate_lab5.py
```

**Expected result:**

```text
Validate Lab 5
============================================================
   ✅ models: best_model.pkl
   ✅ Container compliance: PASS
Prerequisites OK — proceed to Lab 6
```


**Screenshot (optional):** `images/step-10-validate.png`

---

## Lab 5 complete → [Lab 6](../lab6/STEPS.md)
