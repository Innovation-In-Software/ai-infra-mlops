# Lab 0: Environment Setup & Prerequisites

| | |
|---|---|
| **Class** | ai-mlops-2026-jun30 |
| **Duration** | ~30 minutes |
| **Region** | `us-west-2` only |

---

## Before you start

- [ ] You cloned [ai-infra-mlops](https://github.com/Innovation-In-Software/ai-infra-mlops)
- [ ] VS Code is open on that folder
- [ ] You have AWS credentials from the instructor
- [ ] Terminal is open (**Terminal → New Terminal**)

---

## Step 1 — Open the participant repo in VS Code

**Do this:**

1. Open VS Code.
2. **File → Open Folder** → select your clone, e.g.  
   `D:\Current_work\ai-infra-mlops`
3. In Explorer, confirm you see:
   - `guides/`
   - `labs/`
4. Open terminal and run:

```powershell
cd D:\Current_work\ai-infra-mlops
dir labs
```

**Expected result:** You see `Lab_0_Environment_Setup_and_Prerequisites`.

**Screenshot:** save as `guides/lab0/images/step-01-vscode-repo.png`

---

## Step 2 — Log in to AWS Console

**Do this:**

1. Browser → **https://iis-instructor-03.signin.aws.amazon.com/console**
2. Enter your username (case-sensitive) and password.
3. Set region to **US West (Oregon) `us-west-2`** (top-right).

**Expected result:** AWS Console loads with no "Access Denied".

**Screenshots:**
- `step-02-aws-console-login.png`
- `step-03-aws-region-us-west-2.png`

---

## Step 3 — Verify console access (IAM, SageMaker, S3)

1. **IAM** → Users → your username → confirm **PowerUserAccess** + **IAMFullAccess**
2. **SageMaker** → dashboard loads
3. **S3** → bucket list loads

**Screenshots:**
- `step-04-iam-policies.png`
- `step-05-sagemaker-console.png`
- `step-06-s3-console.png`

---

## Step 4 — Install AWS CLI (if needed)

```powershell
aws --version
```

If not found: install from https://aws.amazon.com/cli/ → restart VS Code terminal → run again.

**Expected result:** `aws-cli/2.x.x`

**Screenshot:** `step-07-aws-cli-version.png`

---

## Step 5 — Configure AWS CLI

```powershell
aws configure
```

| Prompt | Value |
|--------|-------|
| Access Key ID | From instructor |
| Secret Access Key | From instructor |
| Region | `us-west-2` |
| Output | `json` |

Verify:

```powershell
aws sts get-caller-identity
aws configure get region
aws s3 ls --region us-west-2
```

**Screenshot:** `step-08-aws-sts-identity.png`

---

## Step 6 — Install Python packages

```powershell
cd D:\Current_work\ai-infra-mlops\labs\Lab_0_Environment_Setup_and_Prerequisites
python --version
pip install -r requirements.txt
python scripts\test_imports.py
```

**Expected result:** `All imports successful!`

**Screenshot:** `step-09-python-imports.png`

---

## Step 7 — Create your workspace

```powershell
python scripts\setup_lab_directories.py
dir $env:USERPROFILE\Documents\banking-mlops-labs
```

**Expected result:** Folders `lab0` … `lab10`, `config`, `shared_data`, etc.

**Screenshot:** `step-10-workspace-folders.png`

---

## Step 8 — Run verification

```powershell
python scripts\verify_environment.py --dry-run
python scripts\run_lab0_setup.py
python scripts\verify_environment.py
```

**Expected result:**

```
ALL CHECKS PASSED. Environment is ready.
   Proceed to Lab 1.1
```

**Screenshot:** `step-11-verification-pass.png`

---

## Step 9 — Done checklist

| Task | Done |
|------|------|
| AWS Console login | [ ] |
| Region `us-west-2` | [ ] |
| AWS CLI configured | [ ] |
| Python packages installed | [ ] |
| Workspace created | [ ] |
| Verification passed | [ ] |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Login fails | Username is case-sensitive |
| Wrong region | Select US West (Oregon); `aws configure set region us-west-2` |
| `aws` not found | Install AWS CLI v2; restart terminal |
| Verification fails on workspace | Re-run `python scripts\setup_lab_directories.py` |

**Lab 0 complete → proceed to Lab 1.1** (guide coming soon)
