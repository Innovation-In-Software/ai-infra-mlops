# Lab 0: Environment Setup & Prerequisites

## Class · `ai-mlops-2026-jun30`
## Duration · 30 minutes
## Region · `us-west-2`
## Repo · [github.com/gjkaur/ai-infra-mlops](https://github.com/gjkaur/ai-infra-mlops)
## Platform · **EC2 in us-west-2** + VS Code Remote SSH + bash
## Delivery · [CLOUD-DELIVERY.md](../CLOUD-DELIVERY.md)

---

# Before you start (fresh course run)

If you are **re-testing** Labs 1–2, reset first:

```bash
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab1,lab2
```

First-time setup: continue with Step 1 below.

---

# What you will do

1. Connect to your EC2 lab instance and open the repo in VS Code
2. Clone the participant repo (all labs included)
3. Confirm AWS Console and CLI access (`us-west-2`)
4. Install Python packages for Labs 0–2
5. Create your local `workspace/` folder structure
6. Pass environment verification → proceed to **Lab 1**

| Path | Purpose |
|------|---------|
| `~/ai-infra-mlops/lab0/` | This guide + setup scripts |
| `~/ai-infra-mlops/lab1/` … `lab2/` | Lab guides (more released later) |
| `~/ai-infra-mlops/workspace/` | **Your outputs** (gitignored) |

---

# Credentials (from instructor)

| Item | Value |
|------|-------|
| Console URL | `https://iis-instructor-03.signin.aws.amazon.com/console` |
| Username | `StudentXX` (case-sensitive) |
| Password | From instructor |
| Region | `us-west-2` |
| AWS CLI keys | From instructor **or** EC2 instance role (no keys needed) |

---

# Step 1 — Connect to EC2 with VS Code Remote SSH

### Do this (on your laptop)

1. Open **VS Code**.
2. Install extension **Remote - SSH** (if not installed).
3. **Ctrl+Shift+P** → **Remote-SSH: Connect to Host** → select your student EC2  
   (host entry from instructor, e.g. `student-ec2` in `~/.ssh/config`).
4. After connect: **File → Open Folder** → **`/home/ec2-user/ai-infra-mlops`**  
   (If folder does not exist yet, use `/home/ec2-user` — you clone in Step 3.)
5. **Terminal → New Terminal** — confirm prompt looks like:

   `ec2-user@ip-...:~/ai-infra-mlops$`

### Expected result

VS Code status bar shows **SSH: ec2-user@...**. Terminal is **bash** on the EC2 instance.

---

# Step 2 — Verify built-in tools

### Do this (EC2 terminal)

```bash
clear
python3 --version
git --version
aws --version
```

If `aws` is missing:

```bash
sudo dnf install -y awscli
```

If `python3` is missing:

```bash
sudo dnf install -y python3.11 python3.11-pip
```

### Expected result

- Python **3.8+**
- git **2.x**
- AWS CLI **2.x**

---

# Step 3 — Clone the participant repo

One clone downloads **all** lab folders and `STEPS.md` guides.

```bash
clear
cd ~
git clone https://github.com/gjkaur/ai-infra-mlops.git
cd ai-infra-mlops
ls lab0 lab1 lab2 README.md
```

**Already cloned?** Update instead:

```bash
cd ~/ai-infra-mlops
git pull
```

### Expected result

Repo at `~/ai-infra-mlops` with `lab0/`, `lab1/`, `lab2/`, `README.md`, `CLOUD-DELIVERY.md`.

---

# Step 4 — Confirm lab0 folder

```bash
clear
cd ~/ai-infra-mlops/lab0
ls -la
```

### Expected result

`STEPS.md`, `scripts/`, `config/`, `requirements.txt`, `images/`.

---

# Step 5 — Log in to AWS Console (browser)

1. Open **https://iis-instructor-03.signin.aws.amazon.com/console**
2. Sign in with your **StudentXX** username and password
3. Set region to **US West (Oregon) `us-west-2`** (top-right)

### Expected result

Console home loads without Access Denied; region is `us-west-2`.

---

# Step 6 — Verify console permissions

In the AWS Console (browser):

1. **IAM** → **Users** → your username → confirm **PowerUserAccess** + **IAMFullAccess**
2. Open **SageMaker** console (no error)
3. Open **S3** console (no error)

### Expected result

All three services open without permission errors.

---

# Step 7 — Configure AWS CLI on EC2

### Option A — EC2 instance role (preferred)

If your instructor attached an IAM role to the EC2 instance:

```bash
clear
aws sts get-caller-identity
aws configure get region || aws configure set region us-west-2
aws configure set output json
```

### Option B — Access keys

```bash
clear
aws configure
```

Enter Access Key ID, Secret Access Key, region `us-west-2`, output `json`.

### Verify

```bash
clear
aws sts get-caller-identity
aws configure get region
aws s3 ls --region us-west-2
```

### Expected result

JSON with your IAM ARN; region `us-west-2`; S3 list runs (empty list is OK).

---

# Step 8 — Install Python packages (Labs 0–2)

```bash
clear
cd ~/ai-infra-mlops/lab0
python3 -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r ../lab1/requirements.txt
pip install -r ../lab2/requirements.txt
python3 scripts/test_imports.py
```

### Expected result

`All imports successful!`

---

# Step 9 — Set classroom environment (Lab 2 speed)

```bash
clear
cd ~/ai-infra-mlops/lab0
source scripts/setup_classroom_env.sh
echo "export LAB_NUM_RECORDS=1000" >> ~/.bashrc
echo "export LAB_USE_COMPREHEND=0" >> ~/.bashrc
```

Optional: add the same lines to `/etc/profile.d/mlops-lab.sh` on golden AMIs (instructor).

### Expected result

`LAB_NUM_RECORDS=1000` and `LAB_USE_COMPREHEND=0` for ~30-minute Lab 2.

---

# Step 10 — Create workspace folders

Lab outputs go under `workspace/` inside the repo (gitignored).

```bash
clear
cd ~/ai-infra-mlops/lab0
python3 scripts/setup_lab_directories.py
ls ../workspace
ls ../workspace/lab1 ../workspace/lab2
```

### Expected result

```
workspace/
├── lab1/ … lab10/   (each: config, data, logs, results, scripts)
├── config/
├── logs/
└── ...
```

> `lab0/` in the repo root is the setup guide. **`workspace/lab1`** onward holds your lab outputs.

---

# Step 11 — Verify environment

```bash
clear
cd ~/ai-infra-mlops/lab0
python3 scripts/verify_environment.py --dry-run
python3 scripts/run_lab0_setup.py
python3 scripts/verify_environment.py
```

### Expected result

```
ALL CHECKS PASSED. Environment is ready.
   Proceed to Lab 1 (open lab1/STEPS.md)
```

Results saved to `lab0/logs/verification_results.json`.

---

# Troubleshooting

| Issue | Fix |
|-------|-----|
| SSH fails | Check key, security group port 22, correct host in `~/.ssh/config` |
| `git clone` fails | Check internet; URL `https://github.com/gjkaur/ai-infra-mlops.git` |
| `aws sts` fails | Run `aws configure` or ask instructor to attach EC2 instance role |
| Wrong region | `aws configure set region us-west-2` |
| Missing packages | `pip install -r requirements.txt` in lab0, lab1, lab2 |
| Workspace missing | `python3 scripts/setup_lab_directories.py` from `lab0/` |
| Re-test from scratch | `python3 scripts/reset_course.py --labs lab1,lab2` |

---

## Lab 0 complete

Next: **[Lab 1 — Secure MLOps Environment Setup](../lab1/STEPS.md)** (`lab1/`).

---

# Appendix — Windows local setup (optional)

If you are **not** on EC2, use PowerShell and paths under `D:\Current_work\ai-infra-mlops\`.  
Windows-specific screenshots remain in `lab0/images/`.  
Use `python` and backslashes: `python scripts\setup_lab_directories.py`.
