# Lab 0: Environment Setup & Prerequisites

![Lab 0 overview](LAB_SLIDE.png)

| | |
|---|---|
| **Class** | ai-mlops-2026-jun30 |
| **Duration** | 30 minutes |
| **Region** | `us-west-2` |
| **Editor** | VS Code |
| **Terminal** | PowerShell (integrated terminal only) |

---

## Before you start

**Credentials (from instructor):**

| Item | Value |
|------|-------|
| Console URL | `https://iis-instructor-03.signin.aws.amazon.com/console` |
| Username | `StudentXX` (case-sensitive) |
| Password | From instructor |
| Access Key ID | From instructor |
| Secret Access Key | From instructor |
| Region | `us-west-2` |

**One-time VS Code setup:**

1. **File → Open Folder** → `D:\Current_work\ai-infra-mlops`
2. **Terminal → Select Default Profile → PowerShell**
3. **Terminal → New Terminal** — confirm prompt shows `PS ...>`

All commands below run in the **VS Code PowerShell terminal**.

---

## Step 1 — Confirm repo layout

**Do this:**

1. In Explorer, confirm you see the `lab0` folder with `STEPS.md`, `LAB_SLIDE.png`, and `scripts/`
2. Run:

```powershell
cd D:\Current_work\ai-infra-mlops\lab0
Get-ChildItem
```

**Expected result:** You see `scripts`, `config`, `requirements.txt`, `LAB_SLIDE.png`, `STEPS.md`.

**Screenshot:** `images/step-01-vscode-repo.png`

---

## Step 2 — Log in to AWS Console

**Do this (browser):**

1. Open **https://iis-instructor-03.signin.aws.amazon.com/console**
2. Enter username and password (username is **case-sensitive**)
3. Set region to **US West (Oregon) `us-west-2`** (top-right corner)

**Expected result:** AWS Console home loads — no "Access Denied".

**Screenshots:**
- `images/step-02-aws-console-login.png`
- `images/step-03-aws-region-us-west-2.png`

---

## Step 3 — Verify console permissions

**Do this (browser):**

1. Search **IAM** → **Users** → your username
2. Confirm policies: **PowerUserAccess**, **IAMFullAccess**
3. Search **SageMaker** → dashboard loads
4. Search **S3** → bucket list loads

**Expected result:** All three services open without permission errors.

**Screenshots:**
- `images/step-04-iam-policies.png`
- `images/step-05-sagemaker-console.png`
- `images/step-06-s3-console.png`

---

## Step 4 — Install AWS CLI

**Do this (VS Code terminal):**

```powershell
aws --version
```

If `aws` is not recognized:

1. Install AWS CLI v2 from https://aws.amazon.com/cli/
2. **Terminal → Kill Terminal** → **Terminal → New Terminal**
3. Run `aws --version` again

**Expected result:** `aws-cli/2.x.x`

**Screenshot:** `images/step-07-aws-cli-version.png`

---

## Step 5 — Configure AWS CLI

**Do this (VS Code terminal):**

```powershell
aws configure
```

| Prompt | Enter |
|--------|-------|
| AWS Access Key ID | From instructor |
| AWS Secret Access Key | From instructor |
| Default region name | `us-west-2` |
| Default output format | `json` |

Verify:

```powershell
aws sts get-caller-identity
aws configure get region
aws s3 ls --region us-west-2
```

**Expected result:** JSON with your IAM user ARN; region is `us-west-2`; S3 command runs (empty list is OK).

**Screenshot:** `images/step-08-aws-sts-identity.png`

---

## Step 6 — Install Python packages

**Do this (VS Code terminal):**

```powershell
cd D:\Current_work\ai-infra-mlops\lab0
python --version
pip install -r requirements.txt
python scripts\test_imports.py
```

**Expected result:** Python 3.8+; `All imports successful!`

**Screenshot:** `images/step-09-python-imports.png`

---

## Step 7 — Create your workspace

**Do this (VS Code terminal):**

```powershell
python scripts\setup_lab_directories.py
Get-ChildItem $env:USERPROFILE\Documents\banking-mlops-labs
```

**Expected result:** Folders `lab0` through `lab10`, plus `config`, `shared_data`, `logs`, etc.

This workspace is on your PC (`Documents\banking-mlops-labs`) — not in the Git repo.

**Screenshot:** `images/step-10-workspace-folders.png`

---

## Step 8 — Run verification

**Do this (VS Code terminal):**

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

**Screenshot:** `images/step-11-verification-pass.png`

---

## Step 9 — Completion checklist

| Task | Done |
|------|------|
| VS Code open on `ai-infra-mlops` | [ ] |
| Terminal is PowerShell | [ ] |
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
| Terminal shows `C:\...>` not `PS` | **Terminal → Select Default Profile → PowerShell** |
| `aws` not found after install | Kill terminal and open a new one |
| Login fails | Check username case (`Student01` ≠ `student01`) |
| Wrong region | Browser: US West (Oregon); terminal: `aws configure set region us-west-2` |
| Packages missing | `pip install -r requirements.txt` |
| Workspace missing | Re-run `python scripts\setup_lab_directories.py` |

**Lab 0 complete.** Lab 1.1 will be added as `lab1/` when published.
