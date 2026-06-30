# Cloud delivery guide (EC2 + SSH)

Class: **ai-mlops-2026-jun30** · Region: **us-west-2** · Target: **≤30 minutes per lab**

Participants run **every step** on an **EC2 instance** in `us-west-2` via **SSH** and **VS Code Remote SSH**. All lab outputs stay in `workspace/` (gitignored).

**Do not use local Windows PowerShell for lab steps.** Laptop is only for SSH + browser (AWS Console).

---

## Architecture

| Component | Spec |
|-----------|------|
| EC2 | `t3.large`, Amazon Linux 2023, **us-west-2** |
| Access | SSH key or SSM Session Manager |
| Editor | VS Code **Remote - SSH** |
| AWS auth | **`aws configure` access keys** (instructor demo) or IAM instance role |
| Repo path | `~/ai-infra-mlops` |

**Golden AMI (build before class):**

```bash
sudo dnf install -y git python3.11 python3.11-pip docker aws-cli
sudo systemctl enable --now docker
sudo usermod -aG docker ec2-user
sudo alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
sudo alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2
sudo alternatives --set python3 /usr/bin/python3.11
python3 -m pip install awscli
git clone https://github.com/gjkaur/ai-infra-mlops.git ~/ai-infra-mlops
cd ~/ai-infra-mlops/lab0
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
cd ../lab1 && python3 -m pip install -r requirements.txt
cd ../lab2 && python3 -m pip install -r requirements.txt
```

Optional classroom env (faster Lab 2 — still run all scripts):

```bash
export LAB_NUM_RECORDS=1000      # default in scripts; increase for deep testing
export LAB_USE_COMPREHEND=0      # pattern PII (~5 min); set 1 for Comprehend (~hours)
```

Add those lines to `/etc/profile.d/mlops-lab.sh` on the AMI.

---

## Fresh start (instructor or participant)

### 1. Reset local workspace

```bash
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab1,lab2,lab3,lab4,lab5,lab6,lab7,lab8,lab9,lab10
```

### 2. Reset Lab 2 AWS feature groups (if re-running Step 8)

```bash
cd ~/ai-infra-mlops/lab2
python3 scripts/cleanup_lab2.py --aws
```

### 3. Reset Lab 1 AWS (full wipe)

From `lab1/` use existing delete scripts, then re-run Lab 1 STEPS:

```bash
cd ~/ai-infra-mlops/lab1
python3 scripts/delete_audit_logging.py
python3 scripts/delete_sagemaker_studio.py
python3 scripts/delete_banking_buckets.py
# Delete IAM roles and KMS keys in console if needed, then re-run Lab 1
```

### 4. Pull latest repo (if instructor pushed updates)

```bash
cd ~/ai-infra-mlops
git pull
```

---

## 30-minute lab timing

| Lab | Critical path |
|-----|----------------|
| **0** | VS Code SSH; verify Python/AWS; clone repo; workspace; Docker; `verify_environment.py` |
| **1** | KMS → S3 → IAM → **SageMaker domain** (longest) → CloudTrail → validate |
| **2** | Steps 4–7 (~15 min with 1k rows + pattern PII); Step 8 Feature Store (~10–15 min) |
| **3–10** | Follow each `labN/STEPS.md`; run steps as written (live AWS with your access keys) |

**Lab 1 rule:** Run KMS, S3, and IAM before SageMaker — the domain script needs keys and buckets from earlier steps.

**Lab 2 rule:** Keep `LAB_USE_COMPREHEND=0` in class unless you allocate extra time.

---

## VS Code Remote SSH

See [docs/SSH-VSCODE-SETUP.md](docs/SSH-VSCODE-SETUP.md) for full setup.

**Instructor dual setup (ProTech VM + EC2):** [docs/PROTECH-VM-SETUP.md](docs/PROTECH-VM-SETUP.md) — slides/browser on ProTech, lab commands on EC2.

1. Install **Remote - SSH** extension on your laptop.
2. Connect to EC2 via `~/.ssh/config` host entry.
3. **File → Open Folder → `/home/ec2-user/ai-infra-mlops`**
4. Terminal → bash; run commands from each `labN/STEPS.md`.

Each step includes **Expected output** blocks (from EC2 terminal testing) and optional screenshot filenames.

---

## Path reference (EC2 only)

| Purpose | Path |
|---------|------|
| Repo root | `~/ai-infra-mlops` |
| Lab guides | `~/ai-infra-mlops/labN/STEPS.md` |
| Student outputs | `~/ai-infra-mlops/workspace/labN/` |
| Verification logs | `~/ai-infra-mlops/lab0/logs/` |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| SSH timeout | Check instance running, public IP, security group **port 22** from your IP |
| `aws: command not found` on EC2 | Re-run **Lab 0 Step 17** — **17.1** (`sudo dnf install -y aws-cli`) and **17.3** (`python3 -m pip install awscli`) |
| `ModuleNotFoundError: No module named 'awscli'` | **Lab 0 Step 17.3** — `python3 -m pip install awscli` ([lab0/STEPS.md](lab0/STEPS.md)) |
| Feature Store AccessDenied | Re-run `lab1/scripts/create_banking_iam_roles.py` |
| Feature group already exists | `python3 scripts/cleanup_lab2.py --aws` then Step 8 again |
| PII too slow | `export LAB_USE_COMPREHEND=0` |
| Lab 2 over 30 min | Confirm `LAB_NUM_RECORDS=1000`; run Step 8 while discussing Step 9 |
| `ModuleNotFoundError: dnf` after Python 3.11 | Install OS packages in **Step 17.1** before `alternatives --set`; later use `sudo /usr/bin/python3.9 /usr/bin/dnf` ([Lab 0 Step 17](lab0/STEPS.md)) |
| Docker permission denied | **Lab 0 Step 17.1** + **17.6** — `sudo usermod -aG docker ec2-user` then reconnect SSH |
| `docker: command not found` / `ModuleNotFoundError: dnf` | [Lab 0 Docker install error](lab0/STEPS.md#error-docker-command-not-found-or-modulenotfounderror-dnf) |
| `docker ps` permission denied | [Lab 0 Docker permission error](lab0/STEPS.md#error-docker-ps--permission-denied-on-varrundockersock) |
