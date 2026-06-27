# Lab 0: Environment Setup & Prerequisites

![Lab 0 overview](LAB_SLIDE.png)

| | |
|---|---|
| **Class** | ai-mlops-2026-jun30 |
| **Duration** | 30 minutes |
| **Region** | `us-west-2` |
| **Repo** | [github.com/gjkaur/ai-infra-mlops](https://github.com/gjkaur/ai-infra-mlops) |
| **Editor** | VS Code |
| **Terminal** | PowerShell (integrated terminal only) |

---

## How to use this guide

Do every step **in order**. All terminal commands run in **VS Code → PowerShell terminal** (bottom panel). AWS Console steps use your **browser**.

| Use | Do not use |
|-----|------------|
| VS Code integrated terminal | External terminal / CMD |
| **PowerShell** (`PS C:\...>`) | Command Prompt (`C:\...>`) |

---

## Credentials (from instructor)

| Item | Value |
|------|-------|
| Console URL | `https://iis-instructor-03.signin.aws.amazon.com/console` |
| Username | `StudentXX` (case-sensitive) |
| Password | From instructor |
| Access Key ID | From instructor |
| Secret Access Key | From instructor |
| Region | `us-west-2` |

---

## Step 1 — Open VS Code and set PowerShell as default terminal

**Do this:**

1. Open **VS Code** on your laptop.
2. Open the terminal panel at the bottom (**Terminal → New Terminal** or **Ctrl+Shift+`**).
3. In the **terminal toolbar** (top-right of the terminal panel), click the **˅** (down arrow) next to the **+** button.
4. Click **Select Default Profile**.

![Step 1a — Open terminal menu and click Select Default Profile](images/step-01a-select-default-profile.png)

5. In **Select your default terminal profile**, click **PowerShell**  
   (path: `C:\Program Files\PowerShell\7\pwsh.exe` — **not** Command Prompt or Windows PowerShell).

![Step 1b — Choose PowerShell as default profile](images/step-01b-choose-powershell.png)

6. **Terminal → New Terminal** (or click **+** in the terminal panel).
7. Confirm the prompt shows **`PS C:\...>`** and the profile label shows **pwsh**.

**Expected result:** Default terminal is PowerShell. New terminals open with a `PS` prompt.

| Correct | Wrong |
|---------|-------|
| **PowerShell** (`pwsh.exe`) | Command Prompt |
| Prompt: `PS C:\...>` | Prompt: `C:\...>` |

---

## Step 2 — Clone the participant repo

**Do this (VS Code terminal):**

```powershell
cd D:\Current_work
git clone https://github.com/gjkaur/ai-infra-mlops.git
```

If `D:\Current_work` does not exist, create it first:

```powershell
New-Item -ItemType Directory -Force -Path D:\Current_work
cd D:\Current_work
git clone https://github.com/gjkaur/ai-infra-mlops.git
```

**Expected result:** Folder `D:\Current_work\ai-infra-mlops` is created with `lab0`, `README.md`, etc.

![Step 2 — git clone successful](images/step-02-git-clone.png)

---

## Step 3 — Open the repo in VS Code

**Do this:**

1. **File → Open Folder**

![Step 3a — File → Open Folder](images/step-03a-open-folder-menu.png)

2. Navigate to **`D:\Current_work\ai-infra-mlops`**
3. Click **Select Folder**

![Step 3b — Select ai-infra-mlops folder](images/step-03b-select-folder.png)

4. In the **Explorer** (left panel), expand folders and confirm you see:
   - `README.md`
   - `lab0/`
   - `lab0/STEPS.md` ← this file
   - `lab0/LAB_SLIDE.png`
   - `lab0/scripts/`

![Step 3c — Repo open in VS Code Explorer](images/step-03c-repo-in-explorer.png)

**Expected result:** VS Code title bar shows `ai-infra-mlops`. Explorer shows the repo tree.

---

## Step 4 — View the lab slide and confirm lab folder

**Do this:**

1. In Explorer, click **`lab0/LAB_SLIDE.png`** to preview the lab overview.
2. Open a new terminal if needed: **Terminal → New Terminal**
3. Run:

```powershell
cd D:\Current_work\ai-infra-mlops\lab0
Get-ChildItem
```

**Expected result:** Terminal lists `scripts`, `config`, `requirements.txt`, `LAB_SLIDE.png`, `STEPS.md`, `images`.

![Step 4 — Get-ChildItem in lab0 folder](images/step-04-lab0-folder.png)

---

## Step 5 — Log in to AWS Console

**Do this (browser):**

1. Open **https://iis-instructor-03.signin.aws.amazon.com/console**
2. Enter your **username** (case-sensitive) and **password**
3. If prompted to set a new password, do so and save it securely

![Step 5a — AWS console sign-in](images/step-05a-aws-console-login.png)

4. Set region to **US West (Oregon) `us-west-2`** (top-right corner)

![Step 5b — Region set to us-west-2](images/step-05b-aws-region-us-west-2.png)

Keep VS Code open — you will return to the terminal in Step 7.

**Expected result:** AWS Console home loads with no "Access Denied"; region is `us-west-2`.

---

## Step 6 — Verify console permissions

**Do this (browser):**

1. Search **IAM** → open **IAM**

![Step 6a — Search IAM](images/step-06a-iam-search.png)

2. **Users** → click your username

![Step 6b — IAM users list](images/step-06b-iam-users.png)

3. Confirm attached policies (student accounts: **PowerUserAccess** + **IAMFullAccess**)

![Step 6c — IAM user permissions](images/step-06c-iam-policies.png)

4. Search **SageMaker** → open console

![Step 6d — Search SageMaker](images/step-06d-sagemaker-search.png)

![Step 6e — SageMaker console](images/step-06e-sagemaker-console.png)

5. Search **S3** → open console

![Step 6f — Search S3](images/step-06f-s3-search.png)

**Expected result:** IAM, SageMaker, and S3 all open without permission errors.

---

## Step 7 — Install AWS CLI

**Do this (VS Code terminal first):**

```powershell
aws --version
```

If `aws` is not recognized, install it:

![Step 7a — aws command not found](images/step-07a-aws-not-found.png)

1. Open https://aws.amazon.com/cli/ → **Get started**

![Step 7b — AWS CLI homepage](images/step-07b-aws-cli-homepage.png)

![Step 7c — AWS CLI getting started docs](images/step-07c-aws-cli-getting-started-docs.png)

![Step 7d — AWS CLI install documentation](images/step-07d-aws-cli-install-docs.png)

![Step 7e — AWS CLI install for Windows](images/step-07e-aws-cli-install-windows-docs.png)

2. Download **AWSCLIV2.msi** → save to Downloads

![Step 7f — Save AWS CLI MSI installer](images/step-07f-aws-cli-msi-save.png)

![Step 7g — AWS CLI MSI in Downloads](images/step-07g-aws-cli-msi-downloads.png)

3. Run the installer

![Step 7h — Ready to install AWS CLI](images/step-07h-aws-cli-ready-install.png)

![Step 7i — Installing AWS CLI](images/step-07i-aws-cli-installing.png)

![Step 7j — Validating AWS CLI install](images/step-07j-aws-cli-validating.png)

![Step 7k — AWS CLI install complete](images/step-07k-aws-cli-install-complete.png)

4. Try `aws --version` again — it may **still fail** if you only open a new terminal:

![Step 7l — aws still not found after install](images/step-07l-aws-not-found-after-install.png)

![Step 7m — New terminal alone does not fix PATH](images/step-07m-new-terminal-still-fails.png)

5. **Fully close VS Code** — **File → Exit** (not just Kill Terminal)

![Step 7n — Close VS Code completely](images/step-07n-close-vscode.png)

6. Reopen VS Code → **File → Open Folder** → `D:\Current_work\ai-infra-mlops` → **Terminal → New Terminal**

```powershell
cd D:\Current_work\ai-infra-mlops\lab0
aws --version
```

![Step 7o — aws --version success after VS Code restart](images/step-07o-aws-version-success.png)

**Expected result:** `aws-cli/2.x.x Python/3.x.x Windows/...`

> **Kill Terminal is not enough on Windows.** You must restart VS Code so the updated PATH is loaded.

---

## Step 8 — Configure AWS CLI

**Do this (VS Code terminal):**

```powershell
aws configure
```

Enter when prompted (use values from your instructor handout — **never** commit keys to Git):

| Prompt | Enter |
|--------|-------|
| AWS Access Key ID | From instructor handout |
| AWS Secret Access Key | From instructor handout |
| Default region name | `us-west-2` |
| Default output format | `json` |

![Step 8a — aws configure prompt](images/step-08a-aws-configure-prompt.png)

Verify:

```powershell
aws sts get-caller-identity
aws configure get region
aws s3 ls --region us-west-2
```

![Step 8b — aws configure complete and verified](images/step-08b-aws-configure-verify.png)

**Expected result:** JSON with your IAM user ARN; region is `us-west-2`; S3 command runs (empty list is OK).

---

## Step 9 — Install Python packages

**Do this (VS Code terminal):**

```powershell
cd D:\Current_work\ai-infra-mlops\lab0
```

Review `requirements.txt`:

![Step 9a — requirements.txt](images/step-09a-requirements-file.png)

Confirm lab folder:

![Step 9b — lab0 folder contents](images/step-09b-lab0-folder-list.png)

Install packages:

```powershell
python --version
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts\test_imports.py
```

![Step 9c — pip upgrade](images/step-09c-pip-upgrade.png)

![Step 9d — pip install requirements](images/step-09d-pip-install.png)

![Step 9e — All imports successful](images/step-09e-test-imports.png)

**Expected result:** Python 3.8+; terminal prints `All imports successful!`

---

## Step 10 — Create your workspace (inside the repo)

Your lab outputs live in a **`workspace`** folder **inside the same repo** you cloned — not in Documents.

**Do this (VS Code terminal):**

```powershell
cd D:\Current_work\ai-infra-mlops\lab0
python scripts\setup_lab_directories.py
Get-ChildItem ..\workspace
```

**Expected result:** Under `D:\Current_work\ai-infra-mlops\workspace\` you see:

```
workspace/
├── lab0/ ... lab10/     (each with scripts, config, data, results, logs)
├── config/
├── shared_data/
├── scripts/
├── results/
└── logs/
```

> **`lab0/`** (course guide + scripts) is for instructions. **`workspace/lab0/`** is where you save lab outputs during the course. The `workspace/` folder is gitignored — your work stays local.

**Screenshot:** `images/step-10-workspace-folders.png` *(pending — capture after running setup)*

---

## Step 11 — Run environment verification

**Do this (VS Code terminal):**

```powershell
cd D:\Current_work\ai-infra-mlops\lab0
python scripts\verify_environment.py --dry-run
python scripts\run_lab0_setup.py
python scripts\verify_environment.py
```

**Expected result:**

```
ALL CHECKS PASSED. Environment is ready.
   Proceed to Lab 1.1
```

**Screenshot:** `images/step-11-verification-pass.png` *(pending)*

---

## Step 12 — Completion checklist

| Task | Done |
|------|------|
| VS Code open on `ai-infra-mlops` | [ ] |
| Repo cloned from GitHub | [ ] |
| Terminal is PowerShell (`PS ...>`) | [ ] |
| Lab slide viewed (`LAB_SLIDE.png`) | [ ] |
| AWS Console login | [ ] |
| Region `us-west-2` | [ ] |
| AWS CLI installed (restarted VS Code after install) | [ ] |
| Python packages installed | [ ] |
| Workspace created | [ ] |
| Verification passed | [ ] |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Terminal shows `C:\...>` not `PS` | Terminal panel → **˅** next to **+** → **Select Default Profile** → **PowerShell** (see Step 1 screenshots) |
| `git` not found | Install Git from https://git-scm.com/ and restart VS Code |
| Clone fails | Check internet; confirm URL: `https://github.com/gjkaur/ai-infra-mlops.git` |
| `aws` not found after install | **Fully close VS Code** (File → Exit), reopen, then run `aws --version`. Kill Terminal alone is not enough on Windows. |
| Login fails | Username is case-sensitive (`Student01` ≠ `student01`) |
| Wrong region | Browser: US West (Oregon); terminal: `aws configure set region us-west-2` |
| Packages missing | `pip install -r requirements.txt` |
| Workspace missing | Re-run `python scripts\setup_lab_directories.py` from `lab0/`; check `..\workspace` |

---

**Lab 0 complete.** Lab 1.1 will be added as `lab1/` when published.

---

## Screenshot index (37 images)

| Step | Files |
|------|-------|
| 1 | `step-01a`, `step-01b` |
| 2 | `step-02` |
| 3 | `step-03a`, `step-03b`, `step-03c` |
| 4 | `step-04` |
| 5 | `step-05a`, `step-05b` |
| 6 | `step-06a` … `step-06f` |
| 7 | `step-07a` … `step-07o` |
| 8 | `step-08a`, `step-08b` |
| 9 | `step-09a` … `step-09e` |
| 10 | `step-10` *(pending)* |
| 11 | `step-11` *(pending)* |
