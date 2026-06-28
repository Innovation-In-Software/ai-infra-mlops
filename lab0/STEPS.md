# Lab 0: Environment Setup & Prerequisites

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~45–60 minutes |
| **Region** | `us-west-2` (Oregon) |
| **Platform** | AWS Console (browser) → EC2 → [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) → **bash** |
| **Prerequisite** | None — start here |
| **Working directory (after SSH)** | `~/ai-infra-mlops/lab0` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab0/` |
| **Repo** | [github.com/gjkaur/ai-infra-mlops](https://github.com/gjkaur/ai-infra-mlops) |

> **Steps 1–10:** AWS Console in your **browser** + VS Code on your **ProTech VM or laptop** (not on EC2 yet).  
> **Steps 11–18:** All commands in the **VS Code integrated terminal** on EC2 (**bash**). Do not use Windows PowerShell for lab commands.

**Instructor dual setup:** [docs/PROTECH-VM-SETUP.md](../docs/PROTECH-VM-SETUP.md)

---

## Before you start

1. Use a machine with a **web browser** and **VS Code** (ProTech VM `COMPUTER540` or your laptop).
2. Have your **AWS sign-in URL**, **username**, and **password** from the instructor handout.
3. Have **VS Code** installed. Install the **Remote - SSH** extension before Step 9.
4. Keep AWS access keys in the handout only — **never paste keys into git, chat, or screenshots**.

---

## Instructor account — this class (copy-paste)

Use these values when you **demo or test** Lab 0. Password and access keys come from your **instructor handout only** (not stored in git).

| Field | Copy this value |
|-------|-----------------|
| **AWS sign-in URL** | `https://iis-instructor-03.signin.aws.amazon.com/console` |
| **Account ID** | `028417007274` |
| **IAM user name** | `Instructor01` (case-sensitive) |
| **Console region** | `us-west-2` (United States Oregon) |
| **ProTech portal** | `https://labs.protechtraining.com` |
| **ProTech host** | `COMPUTER540` |
| **ProTech portal user** | `PTACCESS540` |

**Pre-built instructor EC2** (skip Steps 4–6 if you use this instance):

| Field | Copy this value |
|-------|-----------------|
| Instance name | `ai-mlops-lab` |
| Instance ID | `i-0326933d0bc3b45f1` |
| Key pair name | `ai-mlops-instructor` |
| PEM file (ProTech VM) | `C:\Users\Administrator\.ssh\ai-mlops-instructor.pem` |
| SSH user | `ec2-user` |
| Security group | `mlops-lab-sg` |
| IAM instance profile | `EC2MLOpsLabProfile` |
| Root volume | 30 GiB |

**Refresh public IP** (IP changes after stop/start) — run on ProTech VM with AWS CLI configured, or on EC2:

```bash
aws ec2 describe-instances --instance-ids i-0326933d0bc3b45f1 --region us-west-2 --query "Reservations[0].Instances[0].PublicIpAddress" --output text
```

Example output at last test: `35.161.45.178` — replace in SSH config if different.

---

## Step 1 — Open the AWS sign-in page (browser)

**Do this:**

1. Open your browser (Chrome or Edge on the ProTech VM is fine).
2. Go to the **AWS access portal URL** from your handout (example format: `https://YOUR-ACCOUNT.signin.aws.amazon.com/console`).
3. Bookmark the page for the rest of the course.

**Expected result:** The AWS sign-in page loads with fields for **Account ID** (or alias), **IAM user name**, and **Password**.

**Instructor example (copy-paste):**

```
https://iis-instructor-03.signin.aws.amazon.com/console
```

Paste that URL into the browser address bar and press Enter.

**Screenshot (optional):** `images/step-01-aws-signin-page.png`

---

## Step 2 — Sign in to your AWS account (browser)

**Do this:**

1. Enter **Account ID** or **account alias** from the handout.
2. Enter your **IAM user name** (example: `Instructor01` or your student user).
3. Enter your **password**.
4. Complete **MFA** if prompted.
5. Click **Sign in**.

**Expected result:** The **AWS Management Console** home page opens. The top navigation bar shows **Services**, **Search**, and your user name on the right.

**Instructor example (copy-paste):**

| Field | Value |
|-------|--------|
| Account ID | `028417007274` |
| IAM user name | `Instructor01` |
| Password | *(from instructor handout — do not commit)* |

After sign-in, top-right should show **`Instructor01`** and account **`028417007274`**.

**Screenshot (optional):** `images/step-02-console-home.png`

---

## Step 3 — Set the console region to us-west-2 (browser)

**Do this:**

1. Look at the **region selector** in the top-right of the console (next to your user name).
2. Click the region name.
3. Select **United States (Oregon) `us-west-2`**.
4. Confirm the region label now shows **Oregon** or **us-west-2**.

**Expected result:** Every EC2, S3, and SageMaker resource you create in this course must be in **`us-west-2`**. If the wrong region is selected, later lab steps will fail or create resources in the wrong place.

**Tip:** Before each lab session, glance at the region selector — it sometimes resets after logout.

**Instructor example (copy-paste):**

1. Console search bar → type `EC2` → open **EC2**.
2. Region selector (top-right) → choose **United States (Oregon) us-west-2**.

Or open EC2 directly for this class:

```
https://us-west-2.console.aws.amazon.com/ec2/home?region=us-west-2
```

**Screenshot (optional):** `images/step-03-region-us-west-2.png`

---

## Step 4 — Open EC2 and create a key pair (browser)

**Do this:**

1. In the console **Search** bar, type `EC2` and open **EC2**.
2. Confirm the region (top-right) is still **us-west-2**.
3. In the left menu, under **Network & Security**, click **Key Pairs**.
4. Click **Create key pair**.
5. Use these settings:

   | Setting | Value |
   |---------|--------|
   | Name | `mlops-lab-key` (or your name, e.g. `student1-mlops-key`) |
   | Key pair type | **RSA** |
   | Private key format | **`.pem`** (for SSH from VS Code) |

6. Click **Create key pair**.
7. Save the downloaded `.pem` file to a safe folder, for example:
   - **Windows (ProTech VM):** `C:\Users\Administrator\.ssh\mlops-lab-key.pem`
   - **macOS/Linux:** `~/.ssh/mlops-lab-key.pem`

**Expected result:** A `.pem` file downloads once. You cannot download it again — if you lose it, create a new key pair and attach it to a new instance.

**Security:** Do not email the `.pem` file or commit it to git.

**Instructor example (copy-paste):**

| Setting | Instructor value |
|---------|------------------|
| Key pair name | `ai-mlops-instructor` |
| PEM on ProTech VM | `C:\Users\Administrator\.ssh\ai-mlops-instructor.pem` |

If `ai-mlops-instructor` already exists in EC2 → **Key Pairs**, you cannot re-download it — use the PEM from your secure folder. Students create their own key (e.g. `mlops-lab-key`).

**Screenshot (optional):** `images/step-04-key-pair.png`

---

## Step 5 — Create a security group for SSH (browser)

**Do this:**

1. In the EC2 left menu, under **Network & Security**, click **Security Groups**.
2. Click **Create security group**.
3. Use these settings:

   | Setting | Value |
   |---------|--------|
   | Security group name | `mlops-lab-sg` |
   | Description | `SSH access for MLOps lab EC2` |
   | VPC | **default** (unless your handout says otherwise) |

4. **Inbound rules** — click **Add rule**:

   | Type | Port | Source |
   |------|------|--------|
   | SSH | 22 | **My IP** (recommended) |

   If **My IP** is unavailable, use your instructor’s allowed CIDR from the handout.

5. Leave **Outbound rules** as default (all traffic allowed).
6. Click **Create security group**.

**Expected result:** Security group `mlops-lab-sg` appears in the list with inbound **SSH (22)** from your IP.

**Instructor example (copy-paste):**

| Setting | Instructor value |
|---------|------------------|
| Security group name | `mlops-lab-sg` |
| Inbound | SSH **22** from **My IP** |

If `mlops-lab-sg` already exists, open it → **Inbound rules** → **Edit** → add **My IP** on port 22 if SSH times out.

**Screenshot (optional):** `images/step-05-security-group.png`

---

## Step 6 — Launch your lab EC2 instance (browser)

**Do this:**

1. EC2 left menu → **Instances** → **Launch instances**.
2. Configure the instance:

   | Section | Setting | Value |
   |---------|---------|--------|
   | **Name** | Instance name | `mlops-lab` |
   | **Application and OS Images** | AMI | **Amazon Linux 2023** (64-bit x86) |
   | **Instance type** | Type | **`t3.large`** (2 vCPU, 8 GiB RAM) |
   | **Key pair** | Key pair | Select the key from Step 4 |
   | **Network settings** | Security group | Select existing → **`mlops-lab-sg`** |
   | **Configure storage** | Root volume | **30 GiB**, **gp3** (required for Lab 0 pip installs) |

3. Expand **Advanced details** (optional): if your handout provides an **IAM instance profile** for labs, select it. Otherwise skip — you will use `aws configure` with access keys in Step 14.
4. Review summary on the right: **1 instance**, **Amazon Linux 2023**, **t3.large**.
5. Click **Launch instance**.
6. Click **View all instances**.

**Expected result:** Instance `mlops-lab` shows state **Pending**, then **Running**. Wait until **Status check** shows **2/2 checks passed** (may take 2–5 minutes).

**Instructor example (copy-paste):**

**Shortcut:** Instance **`ai-mlops-lab`** is already provisioned for this class. EC2 → **Instances** → confirm it is **Running** → skip to **Step 7**.

If you launch a new instance for testing, use:

| Setting | Value |
|---------|--------|
| Name | `ai-mlops-lab` |
| AMI | Amazon Linux 2023 |
| Instance type | `t3.large` |
| Key pair | `ai-mlops-instructor` |
| Security group | `mlops-lab-sg` |
| Storage | 30 GiB gp3 |
| IAM instance profile | `EC2MLOpsLabProfile` (optional — enables role-based `aws` on EC2) |

**Screenshot (optional):** `images/step-06-launch-instance.png`

---

## Step 7 — Note the instance public IP (browser)

**Do this:**

1. EC2 → **Instances** → select **`mlops-lab`**.
2. In the **Details** tab, find **Public IPv4 address** (example: `35.161.45.178`).
3. Copy the IP to a notepad — you need it for SSH and VS Code.
4. Confirm:
   - **Instance state:** Running
   - **Status check:** 2/2 checks passed
   - **Region:** us-west-2

**Expected result:** You have a **Public IPv4 address** written down. This IP **changes** if you stop and start the instance — update SSH config after a restart.

**Instructor example (copy-paste):**

Console: EC2 → Instances → select **`ai-mlops-lab`** (`i-0326933d0bc3b45f1`) → copy **Public IPv4 address**.

CLI (ProTech VM or EC2, with `aws` configured):

```bash
aws ec2 describe-instances --instance-ids i-0326933d0bc3b45f1 --region us-west-2 --query "Reservations[0].Instances[0].PublicIpAddress" --output text
```

Example output (yours may differ):

```text
35.161.45.178
```

**Screenshot (optional):** `images/step-07-public-ip.png`

---

## Step 8 — Install VS Code and Remote SSH (local machine)

**Do this:**

On your **ProTech VM** or **laptop** (not on EC2):

1. Install [Visual Studio Code](https://code.visualstudio.com/) if not already installed.
2. Open VS Code → **Extensions** (`Ctrl+Shift+X`).
3. Search for **Remote - SSH** (publisher: Microsoft) → **Install**.
4. Optional but helpful: install **Remote Explorer** (same publisher).

**Expected result:** The VS Code status bar can show remote connections; **Remote Explorer** appears in the activity bar (monitor icon).

**Instructor example (copy-paste):**

On ProTech VM **`COMPUTER540`**, install VS Code if needed:

```powershell
winget install Microsoft.VisualStudioCode
```

Then in VS Code → Extensions → install **`ms-vscode-remote.remote-ssh`**.

**Screenshot (optional):** `images/step-08-vscode-remote-ssh-ext.png`

---

## Step 9 — Configure SSH for your EC2 instance (local machine)

**Do this:**

1. Move your `.pem` file from Step 4 into your SSH folder (if not already there):
   - Windows: `C:\Users\Administrator\.ssh\mlops-lab-key.pem`
   - macOS/Linux: `~/.ssh/mlops-lab-key.pem`

2. **Restrict PEM permissions** (required for SSH):
   - **Windows (PowerShell — setup only):**
     ```powershell
     icacls C:\Users\Administrator\.ssh\mlops-lab-key.pem /inheritance:r
     icacls C:\Users\Administrator\.ssh\mlops-lab-key.pem /grant:r "$($env:USERNAME):(R)"
     ```
   - **macOS/Linux:**
     ```bash
     chmod 400 ~/.ssh/mlops-lab-key.pem
     ```

3. Create or edit SSH config:
   - **Windows:** `C:\Users\Administrator\.ssh\config`
   - **macOS/Linux:** `~/.ssh/config`

4. Add this block (replace `YOUR_PUBLIC_IP` with the IP from Step 7):

   ```
   Host mlops-lab-ec2
       HostName YOUR_PUBLIC_IP
       User ec2-user
       IdentityFile C:/Users/Administrator/.ssh/mlops-lab-key.pem
   ```

   On macOS/Linux, use `IdentityFile ~/.ssh/mlops-lab-key.pem`.

5. Test SSH from a **local** terminal (optional):

   ```bash
   ssh mlops-lab-ec2
   ```

   Type `exit` after you see the Amazon Linux prompt.

**Expected result:** SSH connects as `ec2-user@...` without a password prompt (key-based auth). First connect may ask to trust the host fingerprint — type `yes`.

**Instructor example (copy-paste):**

**1. PEM permissions (ProTech VM — PowerShell):**

```powershell
icacls C:\Users\Administrator\.ssh\ai-mlops-instructor.pem /inheritance:r
icacls C:\Users\Administrator\.ssh\ai-mlops-instructor.pem /grant:r "$($env:USERNAME):(R)"
```

**2. SSH config** — edit `C:\Users\Administrator\.ssh\config` (create file if missing). Replace `35.161.45.178` with the IP from Step 7 if different:

```
Host ai-mlops-lab
    HostName 35.161.45.178
    User ec2-user
    IdentityFile C:/Users/Administrator/.ssh/ai-mlops-instructor.pem
```

**3. Test SSH (PowerShell or Git Bash):**

```bash
ssh ai-mlops-lab
```

Type `exit` when you see `[ec2-user@...]$`.

**Screenshot (optional):** `images/step-09-ssh-config.png`

---

## Step 10 — Connect VS Code to EC2 (local → remote)

**Do this:**

1. Open **VS Code** on your ProTech VM or laptop.
2. Press **`Ctrl+Shift+P`** → type **`Remote-SSH: Connect to Host`** → select **`ai-mlops-lab`** (instructor) or **`mlops-lab-ec2`** (your own host name from Step 9).
3. Wait for VS Code to install the VS Code Server on EC2 (first connect takes 1–2 minutes).
4. **File → Open Folder** → enter `/home/ec2-user` → **OK**.
5. **Terminal → New Terminal** — confirm the shell is **bash**.
6. Run:

   ```bash
   clear
   whoami
   pwd
   ```

**Expected result:**

```text
ec2-user
/home/ec2-user
```

Status bar shows **`SSH: ai-mlops-lab`** (or your host alias). The integrated terminal prompt looks like:

```text
[ec2-user@ip-172-31-xx-xx ~]$
```

**Instructor example (copy-paste):** After connect, run:

```bash
clear
whoami
hostname
pwd
```

Expected:

```text
ec2-user
ip-172-31-xx-xx.us-west-2.compute.internal
/home/ec2-user
```

From this step onward, **all lab commands** run in this EC2 terminal — not in Windows PowerShell.

**Screenshot (optional):** `images/step-10-vscode-connected.png`

---

## Step 11 — Verify tools on EC2

**Do this:**

```bash
clear
python3 --version
git --version
aws --version
uname -a
```

**Expected result:**

```text
Python 3.9.x
git version 2.x.x
aws-cli/2.x.x ...
Linux ... amzn2023.x86_64 ...
```

If `aws` is missing:

```bash
sudo dnf install -y awscli
```

**Instructor example (copy-paste):**

```bash
clear
python3 --version
git --version
aws --version
uname -a
```

Expected (versions may vary slightly):

```text
Python 3.9.25
git version 2.50.1
aws-cli/2.33.15 Python/3.9.25 Linux/6.12.92-122.166.amzn2023.x86_64 source/x86_64.amzn.2023
Linux ... amzn2023.x86_64 GNU/Linux
```

**Screenshot (optional):** `images/step-11-tools.png`

---

## Step 12 — Clone the course repo on EC2

**Do this:**

```bash
clear
cd ~
git clone https://github.com/gjkaur/ai-infra-mlops.git
cd ai-infra-mlops
git pull
ls -1
```

**Expected result:**

```text
CLOUD-DELIVERY.md
README.md
docs
lab0
lab1
lab2
...
scripts
```

**Instructor example (copy-paste):**

If repo already exists, pull instead of clone:

```bash
clear
cd ~
if [ -d ai-infra-mlops ]; then cd ai-infra-mlops && git pull; else git clone https://github.com/gjkaur/ai-infra-mlops.git && cd ai-infra-mlops; fi
ls -1
```

**Screenshot (optional):** `images/step-12-clone.png`

---

## Step 13 — Open the lab0 folder in VS Code

**Do this:**

1. **File → Open Folder** → `/home/ec2-user/ai-infra-mlops`
2. In the terminal:

   ```bash
   clear
   cd ~/ai-infra-mlops/lab0
   ls -1
   ```

**Expected result:**

```text
STEPS.md
config
images
requirements.txt
scripts
```

**Instructor example (copy-paste):**

VS Code: **File → Open Folder** → paste:

```
/home/ec2-user/ai-infra-mlops
```

Terminal:

```bash
clear
cd ~/ai-infra-mlops/lab0 && ls -1
```

**Screenshot (optional):** `images/step-13-lab0-folder.png`

---

## Step 14 — Configure AWS CLI on EC2

**Do this:**

Configure the CLI with **access keys from your handout** (demo/training account). Keys stay on this EC2 instance only.

```bash
clear
aws configure set region us-west-2
aws configure set output json
aws configure set aws_access_key_id YOUR_ACCESS_KEY_ID
aws configure set aws_secret_access_key YOUR_SECRET_ACCESS_KEY
aws sts get-caller-identity
aws configure get region
```

Replace `YOUR_ACCESS_KEY_ID` and `YOUR_SECRET_ACCESS_KEY` with values from the handout — do not commit them.

**Expected result:**

```text
{
    "UserId": "...",
    "Account": "028417007274",
    "Arn": "arn:aws:iam::028417007274:user/Instructor01"
}
us-west-2
```

Account ID and ARN will match your assigned user. Region must be **`us-west-2`**.

**Alternative:** If your instance has an IAM **instance profile**, `aws sts get-caller-identity` may show an `assumed-role` ARN instead of a user — that is OK if your instructor confirms the role has lab permissions.

**Instructor example (copy-paste):**

**Option A — access keys** (paste keys from handout when prompted; not stored in git):

```bash
clear
aws configure set region us-west-2
aws configure set output json
aws configure
```

At the prompts, enter access key ID and secret from the handout. Then:

```bash
aws sts get-caller-identity
aws configure get region
```

Expected:

```text
{
    "UserId": "AIDAXXXXXXXXXXXXXXXXX",
    "Account": "028417007274",
    "Arn": "arn:aws:iam::028417007274:user/Instructor01"
}
us-west-2
```

**Option B — instance profile** (no keys; `ai-mlops-lab` with `EC2MLOpsLabProfile`):

```bash
clear
aws configure set region us-west-2
aws configure set output json
aws sts get-caller-identity
aws configure get region
```

Expected:

```text
{
    "UserId": "AROAQNHOJD2VP3ODHKF4S:i-0326933d0bc3b45f1",
    "Account": "028417007274",
    "Arn": "arn:aws:sts::028417007274:assumed-role/EC2MLOpsLabRole/i-0326933d0bc3b45f1"
}
us-west-2
```

Quick S3 check:

```bash
aws s3 ls --region us-west-2 | head -5
```

**Screenshot (optional):** `images/step-14-aws-cli.png`

---

## Step 15 — Install Python packages

**Do this:**

```bash
clear
cd ~/ai-infra-mlops/lab0
python3 -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r ../lab1/requirements.txt
pip install -r ../lab2/requirements.txt
python3 scripts/test_imports.py
```

**Expected result:**

```text
All imports successful!
```

If pip fails with **no space left on device**, return to Step 6 and increase the root volume to **30 GiB**, then expand the filesystem or relaunch the instance.

**Instructor example (copy-paste):**

```bash
clear
cd ~/ai-infra-mlops/lab0
python3 -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r ../lab1/requirements.txt
pip install -r ../lab2/requirements.txt
python3 scripts/test_imports.py
```

Expected last line:

```text
All imports successful!
```

**Screenshot (optional):** `images/step-15-pip.png`

---

## Step 16 — Set classroom environment variables

**Do this:**

```bash
clear
source ~/ai-infra-mlops/lab0/scripts/setup_classroom_env.sh
grep LAB_ ~/.bashrc || { echo 'export LAB_NUM_RECORDS=1000' >> ~/.bashrc; echo 'export LAB_USE_COMPREHEND=0' >> ~/.bashrc; }
echo $LAB_NUM_RECORDS $LAB_USE_COMPREHEND
```

**Expected result:**

```text
MLOps lab env: LAB_NUM_RECORDS=1000 LAB_USE_COMPREHEND=0 region=us-west-2
1000 0
```

**Instructor example (copy-paste):**

```bash
clear
source ~/ai-infra-mlops/lab0/scripts/setup_classroom_env.sh
grep LAB_ ~/.bashrc || { echo 'export LAB_NUM_RECORDS=1000' >> ~/.bashrc; echo 'export LAB_USE_COMPREHEND=0' >> ~/.bashrc; }
echo $LAB_NUM_RECORDS $LAB_USE_COMPREHEND
```

**Screenshot (optional):** `images/step-16-env.png`

---

## Step 17 — Create the student workspace

**Do this:**

```bash
clear
cd ~/ai-infra-mlops/lab0
python3 scripts/setup_lab_directories.py
ls ../workspace
```

**Expected result:**

```text
Creating Banking MLOps Lab Directory Structure
============================================================
   Target: /home/ec2-user/ai-infra-mlops/workspace
   Directories created: 15
   Mapping file: .../workspace/config/labs_mapping.json

Directory structure ready.
config  lab1  lab2  lab3  ...  logs  results  scripts  shared_data
```

**Instructor example (copy-paste):**

```bash
clear
cd ~/ai-infra-mlops/lab0
python3 scripts/setup_lab_directories.py
ls ../workspace
```

**Screenshot (optional):** `images/step-17-workspace.png`

---

## Step 18 — Verify the full environment

**Do this:**

```bash
clear
cd ~/ai-infra-mlops/lab0
python3 scripts/run_lab0_setup.py
python3 scripts/verify_environment.py
```

**Expected result:**

```text
Banking MLOps Environment Verification
============================================================
   [PASS] Python Version: Python 3.9.x
   [PASS] Required Packages: Installed: 12, Missing: 0
   [PASS] Default Region Config: us-west-2
   [PASS] AWS CLI Region: Region: us-west-2
   [PASS] AWS CLI Credentials: Arn: arn:aws:...
   [PASS] Boto3 AWS Access: Account: ...
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

**Instructor example (copy-paste):**

```bash
clear
cd ~/ai-infra-mlops/lab0
python3 scripts/run_lab0_setup.py
python3 scripts/verify_environment.py
```

Expected summary (account/ARN matches Option A or B from Step 14):

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
```

**Screenshot (optional):** `images/step-18-verify-pass.png`

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| SSH timeout | Instance running? Correct **public IP** in SSH config? Security group allows **port 22** from your IP? |
| `Permission denied (publickey)` | PEM path in SSH config; Windows `icacls` on `.pem`; user must be **`ec2-user`** |
| Wrong region in console | Set **us-west-2** before creating EC2 (Step 3) |
| Public IP changed | Run Step 7 IP command; update `HostName` in `C:\Users\Administrator\.ssh\config` |
| `aws sts` AccessDenied | Re-run Step 14; confirm keys and IAM permissions with instructor |
| Pip / disk full | Root volume **30 GiB** minimum (Step 6) |

---

## Lab 0 complete → [Lab 1](../lab1/STEPS.md)
