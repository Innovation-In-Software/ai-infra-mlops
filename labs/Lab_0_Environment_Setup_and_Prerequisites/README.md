# Lab 0: Environment Setup & Prerequisites
## Banking MLOps - Complete Lab Guide

![Lab overview](images/lab_overview.png)

> **Scripts:** All scripts in this guide are in the `scripts/` folder. Run from lab root.
>
> **Prerequisite:** None — this is the starting lab. Use `--dry-run` to verify Python, packages, and course folders without AWS credentials.

---

## LAB OVERVIEW

### 📋 Lab Information
| Aspect | Details |
|--------|---------|
| **Duration** | 30 minutes |
| **Difficulty** | ⭐ (Beginner) |
| **Module** | Pre-Lab Setup |
| **Banking Focus** | Secure Environment Configuration |
| **Prerequisites** | None - This is the starting lab |

### 🎯 Learning Objectives
After completing this lab, you will be able to:
- ✅ Access your AWS environment with provided credentials
- ✅ Configure AWS CLI with banking security settings
- ✅ Verify permissions and region settings
- ✅ Set up a secure development environment
- ✅ Validate connectivity to AWS services
- ✅ Create the lab directory structure

### 🏦 Banking Context
> *"Before building any ML models, we must ensure a secure, compliant development environment. This lab establishes the foundation for all subsequent banking MLOps labs by verifying access, permissions, and tooling."*

---

## QUICK START

Complete the full lab walkthrough below for learning. Use this sequence for a **5-minute quick validation** within the 30-minute lab window:

```bash
cd Labs_Banking_Edition/Lab_0_Environment_Setup_and_Prerequisites
pip install -r requirements.txt

# Verify without AWS (classroom / local prep)
python scripts/verify_environment.py --dry-run

# Create student workspace + verify (Windows VM)
python scripts/run_lab0_setup.py --dry-run
```

**With live AWS credentials configured:**

```bash
python scripts/verify_environment.py
aws sts get-caller-identity
aws configure get region
```

---

## PART 1: Student Environment Information

### 📌 Your Assigned Credentials

| Credential | Value |
|------------|-------|
| **AWS Console URL** | `https://us-west-2.console.aws.amazon.com/` |
| **Username** | `StudentXX` (XX = your assigned number, case-sensitive) |
| **Password** | Provided by instructor |
| **AWS Access Key ID** | Provided by instructor |
| **AWS Secret Access Key** | Provided by instructor |
| **Default Region** | `us-west-2` (Oregon) |
| **Windows VM** | Provided by instructor (RDP credentials) |

### 🔐 Permission Level
- **Your Account**: PowerUserAccess + IAMFullAccess
- **Note**: All work is confined to `us-west-2` region
- **Important**: Usernames are **case-sensitive** (`Student01` ≠ `student01`)

---

## PART 2: AWS Console Access

### Step 2.1: Login to AWS Console

1. Navigate to: `https://us-west-2.console.aws.amazon.com/`
2. Enter Account ID, IAM username `StudentXX`, and password
3. Verify region is **US West (Oregon) us-west-2** (top-right corner)
4. Confirm access — alert instructor if you see "Access Denied"

### Step 2.2: Verify Your Permissions

1. **IAM Console**: `Services → Security, Identity, & Compliance → IAM → Users → StudentXX`
2. Confirm policies: `PowerUserAccess`, `IAMFullAccess`
3. **SageMaker Console**: `Services → Machine Learning → SageMaker` — dashboard loads
4. **S3 Console**: `Services → Storage → S3` — dashboard loads
5. Take screenshot: save as `results/sagemaker_dashboard.png`

---

## PART 3: AWS CLI Configuration

### Step 3.1: Install/Verify AWS CLI

```cmd
aws --version
```

Expected: `aws-cli/2.x.x`. Install from https://aws.amazon.com/cli/ if missing.

### Step 3.2: Configure AWS CLI

```cmd
aws configure
```

```
AWS Access Key ID: [from instructor]
AWS Secret Access Key: [from instructor]
Default region name: us-west-2
Default output format: json
```

**Profile option (shared VM):**

```cmd
aws configure --profile student
aws sts get-caller-identity --profile student
```

### Step 3.3: Verify AWS CLI Configuration

```cmd
aws sts get-caller-identity
aws configure get region
aws s3 ls --region us-west-2
aws sagemaker list-domains --region us-west-2
```

### Step 3.4: Troubleshooting AWS CLI

| Issue | Solution |
|-------|----------|
| `aws: command not found` | Install AWS CLI v2 |
| `InvalidAccessKeyId` | Re-copy Access Key ID carefully |
| `SignatureDoesNotMatch` | Re-copy Secret Access Key carefully |
| `Unable to locate credentials` | Run `aws configure` again |
| Region not set | `aws configure set region us-west-2` |

---

## PART 4: Lab Directory Structure

### Step 4.1: Create Lab Directories (Automated)

**Recommended — run the setup script:**

```cmd
cd Labs_Banking_Edition\Lab_0_Environment_Setup_and_Prerequisites
python scripts\setup_lab_directories.py
```

Creates `%USERPROFILE%\Documents\banking-mlops-labs` with:

```
banking-mlops-labs/
├── lab0/ ... lab10/         (each with scripts, config, data, results, logs)
├── shared_data/
├── scripts/
├── config/
│   ├── setup_info.txt
│   └── labs_mapping.json    (maps lab folders to Labs_Banking_Edition)
├── results/
└── logs/
```

**Manual (Windows CMD):**

```cmd
cd C:\Users\%USERNAME%\Documents
mkdir banking-mlops-labs
cd banking-mlops-labs
mkdir lab0 lab1 lab2 lab3 lab4 lab5 lab6 lab7 lab8 lab9 lab10
mkdir shared_data scripts config results logs
```

### Step 4.2: Course Repository

The full lab content lives in `Labs_Banking_Edition/`:

| Student Folder | Course Lab |
|----------------|------------|
| lab0 | Lab_0_Environment_Setup_and_Prerequisites |
| lab1 | Lab_1.1_Secure_MLOps_Environment_Setup |
| lab2 | Lab_1.2_Banking_Data_Management_and_PII_Protection |
| lab3 | Lab_2.1_Model_Training_and_Fairness_Testing |
| lab4 | Lab_3.1_CICD_Pipeline_with_Compliance_Gates |
| lab5 | Lab_4.1_Secure_Containerization_for_Banking |
| lab6 | Lab_5.1_Model_Deployment_with_Blue_Green |
| lab7 | Lab_6.1_Compliance_Monitoring_and_Observability |
| lab8 | Lab_7.1_End_to_End_SageMaker_Pipeline |
| lab9 | Lab_8.1_Banking_Security_and_Governance_Framework |
| lab10 | Lab_9.1_Enterprise_MLOps_Architecture |

Work from `Labs_Banking_Edition/Lab_X.X_.../` folders during the course.

---

## PART 5: Python & Package Setup

### Step 5.1: Verify Python

```cmd
python --version
```

Requires Python 3.8 or higher.

### Step 5.2: Install Required Packages

```cmd
cd Labs_Banking_Edition\Lab_0_Environment_Setup_and_Prerequisites
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5.3: Test Imports

```cmd
python scripts\test_imports.py
```

Expected: `All imports successful!`

---

## PART 6: Git & Source Control Setup

```cmd
git --version
git config --global user.name "StudentXX"
git config --global user.email "studentXX@banking-training.com"
```

If initializing a personal workspace:

```cmd
cd C:\Users\%USERNAME%\Documents\banking-mlops-labs
git init
```

> **Note:** Do not commit AWS credentials. The course `.gitignore` excludes `.aws/` and credential files.

---

## PART 7: Environment Verification Script

### Step 7.1: Run Verification

**Script:** `scripts/verify_environment.py`

```cmd
python scripts\verify_environment.py --dry-run
```

**Live AWS verification:**

```cmd
python scripts\verify_environment.py
```

**Full Lab 0 orchestration:**

```cmd
python scripts\run_lab0_setup.py --dry-run
```

### Expected Output (dry-run)

```
Banking MLOps Environment Verification
============================================================
Mode: dry-run (AWS checks skipped)
   [PASS] Python Version: Python 3.x.x
   [PASS] Required Packages: Installed: 12, Missing: 0
   [PASS] Default Region Config: us-west-2
   [PASS] AWS CLI Region: Skipped (--dry-run)
   [PASS] AWS CLI Credentials: Skipped (--dry-run)
   [PASS] Boto3 AWS Access: Skipped (--dry-run)
   [PASS] Course Lab Folders: Found 11 labs in Labs_Banking_Edition
   [PASS] Student Workspace: ...
   [PASS] Git Repository: Course repo detected

ALL CHECKS PASSED. Environment is ready.
   Proceed to Lab 1.1
```

Results saved to: `logs/verification_results.json`

---

## PART 8: Cloud9 IDE Setup (Optional)

1. `Services → Developer Tools → Cloud9`
2. Create environment: `Banking-MLOps-StudentXX`, t3.medium, Amazon Linux 2
3. Clone course repo and run Lab 0 verification

---

## PART 9: Quick Access Utilities

**Windows batch menu:**

```cmd
quick_commands.bat
```

Options: verify (dry-run/live), create workspace, full setup, AWS status, SageMaker console.

**PowerShell helpers (optional):**

```powershell
function Start-MLOpsLab {
    Set-Location "$env:USERPROFILE\Documents\banking-mlops-labs"
    Write-Host "Welcome to Banking MLOps Labs!"
}

function Test-MLOpsEnvironment {
    python Labs_Banking_Edition\Lab_0_Environment_Setup_and_Prerequisites\scripts\verify_environment.py --dry-run
}
```

---

## PART 10: Final Verification Checklist

| Task | Status | Notes |
|------|--------|-------|
| AWS Console Access | [ ] | Login and dashboard visible |
| Region us-west-2 | [ ] | Top-right corner |
| AWS CLI Configured | [ ] | `aws sts get-caller-identity` works |
| Python 3.8+ | [ ] | `python --version` |
| Required Packages | [ ] | `pip install -r requirements.txt` |
| Lab Directory Structure | [ ] | `setup_lab_directories.py` |
| Verification Script | [ ] | All checks pass |
| Cloud9 (Optional) | [ ] | IDE accessible |

### Final Commands

```cmd
cd Labs_Banking_Edition\Lab_0_Environment_Setup_and_Prerequisites
python scripts\run_lab0_setup.py
python scripts\verify_environment.py
aws sagemaker list-domains --region us-west-2
```

---

## TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Cannot login to AWS Console | Check case-sensitive username; contact instructor |
| AWS CLI Access Denied | Re-run `aws configure`; verify keys and region |
| Python not found | Install from python.org with "Add to PATH" |
| Package install fails | `python -m pip install -r requirements.txt --user` |
| Verification fails on packages | Install missing packages listed in output |
| Student workspace missing | Run `python scripts/setup_lab_directories.py` |

---

## LAB COMPLETION CHECKLIST

### ✅ Completed Tasks
- [ ] AWS Console login successful
- [ ] AWS CLI configured and working
- [ ] Python and packages installed
- [ ] Lab directory structure created
- [ ] Verification script ran successfully
- [ ] All checks passed

### 🎯 Ready for Next Lab
**Proceed to [Lab 1.1: Secure MLOps Environment Setup](../Lab_1.1_Secure_MLOps_Environment_Setup/)**

---

## FILE STRUCTURE

```
Lab_0_Environment_Setup_and_Prerequisites/
├── README.md
├── requirements.txt
├── quick_commands.bat
├── config/
│   └── environment_config.json
├── logs/
│   └── verification_results.json   (generated)
├── results/                        (screenshots for submission)
└── scripts/
    ├── setup_lab_directories.py
    ├── verify_environment.py
    ├── test_imports.py
    └── run_lab0_setup.py
```

---

## INSTRUCTOR NOTES

### Lab Preparation Checklist
- [ ] Student AWS accounts and access keys distributed
- [ ] Windows VMs accessible
- [ ] Python 3.8+ available on VMs
- [ ] Course repo cloned to student machines
- [ ] Verification script tested with `--dry-run` and live AWS

### Time Management

| Activity | Duration |
|----------|----------|
| AWS Console Access | 5 min |
| AWS CLI Setup | 5 min |
| Directory Structure | 3 min |
| Python/Packages | 10 min |
| Verification | 5 min |
| Review & troubleshooting | 2 min |
| **Total** | **30 min** |

### Key Teaching Points
1. **Region lock**: All banking labs use `us-west-2` only
2. **Case-sensitive usernames**: Common login failure
3. **Dry-run first**: Demo `verify_environment.py --dry-run` before live AWS
4. **Two locations**: Student workspace vs. `Labs_Banking_Edition` course folders

---

**Lab 0 Complete! Proceed to Lab 1.1: Secure MLOps Environment Setup**
