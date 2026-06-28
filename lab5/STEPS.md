# Lab 5: Secure Containerization for Banking

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30 minutes |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | [Lab 4](../lab4/STEPS.md) complete · **Docker** installed ([Lab 0 Step 19](../lab0/STEPS.md)) |
| **Working directory** | `~/ai-infra-mlops/lab5` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab5/` |

> **Run Steps 1–10 once, in order.** Run each command block below, then compare your terminal to the screenshot under that step.  
> All commands run in the **VS Code terminal on EC2** (`whoami` = `ec2-user`). Do not use Windows PowerShell on the ProTech VM.

> **Requires Docker** — `docker ps` must work **without sudo** after Lab 0 Step 19 and an SSH reconnect.  
> **Quick run:** `python3 scripts/run_lab5.py` — then run Step 10 to validate.

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

3. Confirm Lab 4 outputs exist:

```bash
cd ~/ai-infra-mlops/lab4 && python3 scripts/validate_lab4.py
```

**Expected:** `Prerequisites OK — proceed to Lab 5`

![Lab 4 validation — `python3 scripts/validate_lab4.py`](images/step-00b-lab4-validate.png)

4. Confirm Docker works:

```bash
docker ps
```

**Expected:** Header row with `CONTAINER ID` (empty list is OK — no error).

5. Go to Lab 5:

```bash
cd ~/ai-infra-mlops/lab5
```

---

## Lab 5 roadmap

| Step | What you create |
|------|-----------------|
| **1–2** | Confirm repo and Docker |
| **3** | Copy Lab 3 model artifacts into `workspace/lab5/` |
| **4** | Build `banking-ml-inference:latest` image |
| **5** | Health check + sample inference on `:8080` |
| **6** | ECR repository config (real AWS create if needed) |
| **7** | Push image to ECR |
| **8** | Vulnerability scan report |
| **9** | Container compliance manifest |
| **10** | Lab 5 validation |

---

# Step 1 — Confirm lab5 folder

**What you do:** Verify the Lab 5 course files are in the repo.

```bash
cd ~/ai-infra-mlops
ls -1 lab5
```

**Expected:**

```text
Dockerfile
STEPS.md
config
images
requirements.txt
scripts
src
```

![Step 1 — `ls -1 lab5`](images/step-01-lab5-folder.png)

---

# Step 2 — Verify Docker

**What you do:** Confirm Docker CLI and daemon are available.

```bash
docker --version
docker ps
```

**Expected:**

```text
Docker version 25.x.x, build ...
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

If you see `permission denied`, reconnect VS Code SSH after Lab 0 Step 19.

![Step 2 — `docker --version` and `docker ps`](images/step-02-docker.png)

---

# Step 3 — Prepare model artifacts

**What you do:** Copy Lab 3 model files into the Lab 5 workspace for the Docker build.

```bash
cd ~/ai-infra-mlops/lab5
python3 -m pip install -r requirements.txt
python3 scripts/prepare_artifacts.py
ls -1 ../workspace/lab5/models
```

**Expected:**

```text
📦 Preparing container artifacts from Lab 3
============================================================
   ✅ Copied: best_model.pkl
   ✅ Copied: preprocessor.pkl
   ✅ Copied: feature_metadata.json
✅ Artifacts ready for Docker build
best_model.pkl
preprocessor.pkl
```

> Requires Lab 3 Steps 4 and 8 (`best_model.pkl`, `preprocessor.pkl`, `feature_metadata.json`).

![Step 3 — `python3 scripts/prepare_artifacts.py`](images/step-03-artifacts.png)

---

# Step 4 — Build container image

**What you do:** Build the inference image from `lab5/Dockerfile`.

```bash
bash scripts/build_container.sh
```

**Expected:**

```text
🔨 Building banking-ml-inference:latest
...
Successfully tagged banking-ml-inference:latest
✅ Container build complete
```

The build may take 1–3 minutes on first run while base layers download.

![Step 4 — `bash scripts/build_container.sh`](images/step-04-build.png)

---

# Step 5 — Test container locally

**What you do:** Start the container, call `/ping` and `/invocations`, then remove the test container.

```bash
python3 scripts/test_container.py
```

**Expected:**

```text
🧪 Container Inference Test
============================================================
   ✅ Health check: 200 OK
   ✅ Sample prediction: risk_score=0.XX
✅ Container tests passed
```

`risk_score` varies with the trained model — any value between `0.00` and `1.00` is OK.

![Step 5 — `python3 scripts/test_container.py`](images/step-05-test.png)

---

# Step 6 — Create ECR repository

**What you do:** Create (or confirm) the ECR repo and save config JSON.

```bash
python3 scripts/create_ecr_repo.py
```

**Expected:**

```text
📦 ECR Repository
============================================================
   ✅ Created ECR repository: banking-ml-inference
   ✅ Repository: banking-ml-inference
   ✅ Encryption: KMS
   ✅ Scan on push: enabled
✅ ECR repository ready
```

On re-run you may see `Repository already exists` instead of `Created` — that is OK.

![Step 6 — `python3 scripts/create_ecr_repo.py`](images/step-06-ecr.png)

---

# Step 7 — Push image to ECR

**What you do:** Log in to ECR and push `banking-ml-inference:latest`.

```bash
bash scripts/push_to_ecr.sh
```

**Expected:**

```text
   ✅ Login to ECR succeeded
   ✅ Pushed: <account-id>.dkr.ecr.us-west-2.amazonaws.com/banking-ml-inference:latest
✅ Image push complete
```

Replace `<account-id>` with your 12-digit AWS account ID.

![Step 7 — `bash scripts/push_to_ecr.sh`](images/step-07-push.png)

---

# Step 8 — Vulnerability scan

**What you do:** Record a classroom vulnerability scan summary.

```bash
python3 scripts/scan_container.py
```

**Expected:**

```text
🔍 Container Scan
============================================================
   Critical: 0
   High: 0
   Status: PASS (banking threshold)
✅ Scan report saved
```

![Step 8 — `python3 scripts/scan_container.py`](images/step-08-scan.png)

---

# Step 9 — Compliance report

**What you do:** Write the container deployment manifest.

```bash
python3 scripts/generate_container_report.py
```

**Expected:**

```text
✅ Container compliance report generated
   Manifest: validation/container_deployment_manifest.json
```

![Step 9 — `python3 scripts/generate_container_report.py`](images/step-09-report.png)

---

# Step 10 — Validate lab5

**What you do:** Confirm Lab 5 prerequisites and outputs.

```bash
python3 scripts/validate_lab5.py
```

**Expected:**

```text
Validate Lab 5
============================================================
   ✅ Lab 3 best_model.pkl
   ✅ models: best_model.pkl
   ✅ models: preprocessor.pkl
   ✅ config: ecr_config.json
   ✅ config: scan_report.json
   ✅ validation: container_deployment_manifest.json
   ✅ validation: container_test.json
   ✅ Container compliance: PASS

============================================================
Prerequisites OK — proceed to Lab 6
```

![Step 10 — `python3 scripts/validate_lab5.py`](images/step-10-validate.png)

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `whoami` = `Administrator` | Reconnect VS Code Remote-SSH to EC2 ([Lab 0 Step 13](../lab0/STEPS.md)) |
| `docker: permission denied` | Complete Lab 0 Step 19, then **reconnect** VS Code SSH |
| `docker: command not found` | Re-run Lab 0 Step 19 |
| `Lab 3 model not found` | Complete [Lab 3](../lab3/STEPS.md) Step 8 before Lab 5 Step 3 |
| `Missing Lab 3 config: preprocessor.pkl` | Re-run Lab 3 Step 4 (`load_training_data.py`) |
| `Failed to start container` | Run Step 4 first; check `docker images \| grep banking-ml` |
| `Health check timed out` | Port 8080 may be in use — run `docker rm -f banking-ml-test` and retry |
| `Run create_ecr_repo.py first` | Complete Step 6 before Step 7 |
| ECR push fails (`no basic auth`) | EC2 instance needs ECR permissions ([Lab 0](../lab0/STEPS.md) IAM role) |
| `RepositoryAlreadyExistsException` | OK on re-run — repo already created |
| Screenshot shows the **next** step's command at the bottom | Normal — continuous terminal session |
| `PythonDeprecationWarning` | [Lab 0 Step 17a](../lab0/STEPS.md) — upgrade to Python 3.11 |

---

## Appendix — Fresh start (optional)

**Reset Lab 5 workspace only:**

```bash
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab5
cd lab5
```

Then re-run **Steps 3–10**. Lab 3 artifacts are unchanged.

**Quick run:** `python3 scripts/run_lab5.py` — then run Step 10 to validate.

---

## Lab 5 complete → [Lab 6](../lab6/STEPS.md)
