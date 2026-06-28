# Lab 5: Secure Containerization for Banking

## Class · `ai-mlops-2026-jun30` · **30 min** · **us-west-2**
## Platform · **EC2** + [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) + **bash**
## Prerequisite · [Lab 4](../lab4/STEPS.md) complete
## Working directory · `~/ai-infra-mlops/lab5`
## Outputs · `~/ai-infra-mlops/workspace/lab5/`

> All commands run in the **VS Code integrated terminal** on EC2. Do not use local Windows PowerShell for lab steps.

> **Scripts:** `lab5/scripts/` · Run all: `python3 scripts/run_lab5.py` · **Requires Docker** on EC2 ([Lab 0 Step 19](../lab0/STEPS.md)) for the build step.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
cd lab5
docker ps    # must work without sudo after Lab 0 Step 19 + SSH reconnect
```

Run `clear` before each step for clean terminal screenshots.

---

# Step 1 — Confirm lab5 folder

```bash
clear
cd ~/ai-infra-mlops && ls -1 lab5
```

**Expected output:** `STEPS.md`, `config`, `images`, `requirements.txt`, `scripts`, `src`

**Optional screenshot:** `images/step-01-lab5-folder.png`

---

# Step 2 — Verify Docker

```bash
clear
docker --version
docker ps
```

**Expected output:**

```text
Docker version 25.x.x, build ...
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

**Optional screenshot:** `images/step-02-docker.png`

---

# Step 3 — Prepare model artifacts

```bash
clear
cd ~/ai-infra-mlops/lab5
pip install -r requirements.txt
python3 scripts/prepare_artifacts.py
ls -1 ../workspace/lab5/models
```

**Expected output:**

```text
   ✅ Copied: best_model.pkl
   ✅ Copied: preprocessor.pkl
   ✅ Copied: feature_metadata.json
best_model.pkl
preprocessor.pkl
```

**Optional screenshot:** `images/step-03-artifacts.png`

---

# Step 4 — Build container image

```bash
clear
bash scripts/build_container.sh
```

**Expected output:**

```text
🔨 Building banking-ml-inference:latest
...
Successfully tagged banking-ml-inference:latest
✅ Container build complete
```

**Optional screenshot:** `images/step-04-build.png`

---

# Step 5 — Test container locally

```bash
clear
python3 scripts/test_container.py
```

**Expected output:**

```text
🧪 Container Inference Test
============================================================
   ✅ Health check: 200 OK
   ✅ Sample prediction: risk_score=0.23
✅ Container tests passed
```

**Optional screenshot:** `images/step-05-test.png`

---

# Step 6 — Create ECR repository

```bash
clear
python3 scripts/create_ecr_repo.py
```

**Expected output:**

```text
📦 ECR Repository
============================================================
   ✅ Repository: banking-ml-inference
   ✅ Encryption: KMS
   ✅ Scan on push: enabled
✅ ECR repository ready
```

**Optional screenshot:** `images/step-06-ecr.png`

---

# Step 7 — Push image to ECR

```bash
clear
bash scripts/push_to_ecr.sh
```

**Expected output:**

```text
   ✅ Login to ECR succeeded
   ✅ Pushed: <account-id>.dkr.ecr.us-west-2.amazonaws.com/banking-ml-inference:latest
✅ Image push complete
```

**Optional screenshot:** `images/step-07-push.png`

---

# Step 8 — Vulnerability scan

```bash
clear
python3 scripts/scan_container.py
```

**Expected output:**

```text
🔍 Container Scan
============================================================
   Critical: 0
   High: 0
   Status: PASS (banking threshold)
✅ Scan report saved
```

**Optional screenshot:** `images/step-08-scan.png`

---

# Step 9 — Compliance report

```bash
clear
python3 scripts/generate_container_report.py
```

**Expected output:**

```text
✅ Container compliance report generated
   Manifest: validation/container_deployment_manifest.json
```

**Optional screenshot:** `images/step-09-report.png`

---

# Step 10 — Validate lab5

```bash
clear
python3 scripts/validate_lab5.py
```

**Expected output:**

```text
Validate Lab 5
============================================================
   ✅ models: best_model.pkl
   ✅ Container compliance: PASS
Prerequisites OK — proceed to Lab 6
```

**Optional screenshot:** `images/step-10-validate.png`

---

## Lab 5 complete → [Lab 6](../lab6/STEPS.md)
