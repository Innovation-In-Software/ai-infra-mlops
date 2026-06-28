# Lab 0: Environment Setup & Prerequisites

## Class · `ai-mlops-2026-jun30` · **30 min** · **us-west-2**
## Platform · **EC2** + [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) + **bash**
## Repo · [github.com/gjkaur/ai-infra-mlops](https://github.com/gjkaur/ai-infra-mlops)

> **All steps run on EC2** in the VS Code integrated terminal. Do not use local Windows PowerShell for labs.

---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull    # get latest guides
```

Re-testing Labs 1–2? Run `python3 scripts/reset_course.py --labs lab1,lab2` first.

---

# Step 1 — Connect VS Code to EC2

**Do:** Follow [docs/SSH-VSCODE-SETUP.md](../docs/SSH-VSCODE-SETUP.md). Open folder `/home/ec2-user/ai-infra-mlops` (or `/home/ec2-user` before clone).

**Expected result:** Status bar shows `SSH: ec2-user@...`. Terminal is bash.

**Optional screenshot:** `images/step-01-vscode-remote-ssh.png`

---

# Step 2 — Verify tools

```bash
clear
python3 --version
git --version
aws --version
```

**Expected output:**

```text
Python 3.9.25
git version 2.50.1
aws-cli/2.33.15 Python/3.9.25 Linux/6.12.92-122.166.amzn2023.x86_64 source/x86_64.amzn.2023
```

If missing: `sudo dnf install -y awscli python3.11 python3.11-pip`

**Optional screenshot:** `images/step-02-tools.png`

---

# Step 3 — Clone repo

```bash
clear
cd ~
git clone https://github.com/gjkaur/ai-infra-mlops.git
cd ai-infra-mlops
git pull
ls -1
```

**Expected output:**

```text
CLOUD-DELIVERY.md
README.md
docs
lab0
lab1
lab2
lab3
...
scripts
```

**Optional screenshot:** `images/step-03-clone.png`

---

# Step 4 — Confirm lab0 folder

```bash
clear
cd ~/ai-infra-mlops/lab0
ls -1
```

**Expected output:**

```text
STEPS.md
config
images
requirements.txt
scripts
```

**Optional screenshot:** `images/step-04-lab0-folder.png`

---

# Step 5 — AWS Console login (browser)

1. Open instructor console URL · sign in as `StudentXX`
2. Region **US West (Oregon) `us-west-2`**

**Expected result:** Console home loads; region `us-west-2`.

**Optional screenshot:** `images/step-05-console.png`

---

# Step 6 — Console permissions (browser)

Open **IAM**, **SageMaker**, **S3** — no Access Denied.

**Optional screenshot:** `images/step-06-iam.png`

---

# Step 7 — AWS CLI on EC2

```bash
clear
aws sts get-caller-identity
aws configure get region || aws configure set region us-west-2
aws configure set output json
aws s3 ls --region us-west-2 | head
```

**Expected output:**

```text
{
    "UserId": "AROAQNHOJD2VP3ODHKF4S:i-0326933d0bc3b45f1",
    "Account": "028417007274",
    "Arn": "arn:aws:sts::028417007274:assumed-role/EC2MLOpsLabRole/i-0326933d0bc3b45f1"
}
us-west-2
```

**Optional screenshot:** `images/step-07-aws-cli.png`

---

# Step 8 — Install Python packages

```bash
clear
cd ~/ai-infra-mlops/lab0
python3 -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r ../lab1/requirements.txt
pip install -r ../lab2/requirements.txt
python3 scripts/test_imports.py
```

**Expected output:**

```text
All imports successful!
```

**Optional screenshot:** `images/step-08-pip.png`

---

# Step 9 — Classroom env vars

```bash
clear
source ~/ai-infra-mlops/lab0/scripts/setup_classroom_env.sh
grep LAB_ ~/.bashrc || { echo 'export LAB_NUM_RECORDS=1000' >> ~/.bashrc; echo 'export LAB_USE_COMPREHEND=0' >> ~/.bashrc; }
```

**Expected output:**

```text
MLOps lab env: LAB_NUM_RECORDS=1000 LAB_USE_COMPREHEND=0 region=us-west-2
```

**Optional screenshot:** `images/step-09-env.png`

---

# Step 10 — Create workspace

```bash
clear
cd ~/ai-infra-mlops/lab0
python3 scripts/setup_lab_directories.py
ls ../workspace
```

**Expected output:**

```text
Creating Banking MLOps Lab Directory Structure
============================================================
   Target: /home/ec2-user/ai-infra-mlops/workspace
   Directories created: 15
   Mapping file: .../workspace/config/labs_mapping.json

Directory structure ready.
config  lab1  lab2  lab3  ...  logs  results  scripts  shared_data
```

**Optional screenshot:** `images/step-10-workspace.png`

---

# Step 11 — Verify environment

```bash
clear
cd ~/ai-infra-mlops/lab0
python3 scripts/verify_environment.py --dry-run
python3 scripts/run_lab0_setup.py
python3 scripts/verify_environment.py
```

**Expected output:**

```text
Banking MLOps Environment Verification
============================================================
   [PASS] Python Version: Python 3.9.25
   [PASS] Required Packages: Installed: 12, Missing: 0
   [PASS] Default Region Config: us-west-2
   [PASS] AWS CLI Region: Region: us-west-2
   [PASS] AWS CLI Credentials: Arn: arn:aws:sts::028417007274:assumed-role/EC2MLOpsLabRole/i-0326933d0bc3b45f1
   [PASS] Boto3 AWS Access: Account: 028417007274
   [PASS] Course Lab Folders: Found 11 lab folder(s) in repo
   [PASS] Student Workspace: Workspace: /home/ec2-user/ai-infra-mlops/workspace (0 missing)
   [PASS] Git Repository: Repo cloned

============================================================
Verification Summary:
   Total Checks: 9
   Passed: 9
   Failed: 0

ALL CHECKS PASSED. Environment is ready.
   Proceed to Lab 1 (open lab1/STEPS.md)

Results saved: /home/ec2-user/ai-infra-mlops/lab0/logs/verification_results.json
```

**Optional screenshot:** `images/step-11-verify-pass.png`

---

## Lab 0 complete → [Lab 1](../lab1/STEPS.md)
