# Lab 0: Environment Setup & Prerequisites

**Class:** `ai-mlops-2026-jun30` · **Region:** `us-west-2` · **Duration:** ~50–65 min

Hands-on steps: [STEPS.md](STEPS.md)

---

## Overview

Lab 0 prepares the **EC2 lab machine** and the **student workspace** used by Labs 1–10. You sign in through the training portal, connect to EC2 with VS Code Remote SSH, install tools, clone this repository, and verify that Python, AWS CLI, Docker, and the workspace layout are ready.

Nothing in Lab 0 creates banking AWS resources. It only validates your environment and scaffolds local directories under `~/ai-infra-mlops/workspace/`.

---

## Prerequisites

- Training portal access and EC2 instance (see STEPS.md Steps 1–13)
- AWS access keys configured on EC2 (`aws configure`, region `us-west-2`)

---

## Lab flow

```
Portal / RDP → AWS EC2 launch → VS Code SSH → clone repo
    → Python 3.11 + pip → Docker → classroom env vars
    → workspace directories → verify 9/9 checks → Lab 1
```

| Phase | What happens |
|-------|----------------|
| **Infrastructure** | EC2 `t3.large`, security group, key pair, public IP |
| **Tooling** | `git`, `python3`, `aws` CLI v2, Docker |
| **Workspace** | `workspace/lab1`–`lab10`, `shared_data`, `logs`, etc. |
| **Verification** | Nine automated checks must all pass |

**Success gate:** `verify_environment.py` reports **9/9 passed** → proceed to [Lab 1](../lab1/STEPS.md).

---

## Scripts reference

All scripts live in `lab0/scripts/`.

### `verify_environment.py`

Runs nine environment checks:

1. Python version (3.8+)
2. Required Python packages (`boto3`, `pandas`, etc.)
3. AWS CLI installed
4. AWS credentials and caller identity
5. Region set to `us-west-2`
6. Repository clone present
7. Workspace directory exists
8. Lab folders scaffolded
9. Docker available (for Lab 5+)

Writes results to `lab0/logs/verification_results.json`.

### `setup_lab_directories.py`

Creates the student workspace tree under `~/ai-infra-mlops/workspace/`:

- Per-lab folders: `lab1` … `lab10`, each with `config/`, `data/`, `results/`, `logs/`, `scripts/`
- Shared folders: `shared_data`, `config`, `results`, `logs`
- `workspace/config/labs_mapping.json` and `setup_info.txt`

### `test_imports.py`

Quick smoke test that core Python packages import without error. Run after `pip install -r requirements.txt`.

### `run_lab0_setup.py`

Orchestrator: runs `setup_lab_directories.py` then prints next steps. Use after workspace creation.

### `setup_classroom_env.sh`

Shell script that exports classroom defaults:

- `AWS_DEFAULT_REGION=us-west-2`
- `LAB_NUM_RECORDS=1000` (synthetic data size for Lab 2+)
- `LAB_USE_COMPREHEND=0` (skip Comprehend API in PII lab)

Source it with: `source scripts/setup_classroom_env.sh`

---

## Configuration

| File | Purpose |
|------|---------|
| `config/environment_config.json` | Course lab list, workspace directory names, Python minimum version |
| `config/screenshot_map.json` | Instructor screenshot mappings for STEPS.md images |
| `requirements.txt` | Python dependencies for Lab 0 and early labs |

---

## Outputs

| Location | Contents |
|----------|----------|
| `~/ai-infra-mlops/workspace/` | Empty scaffold for Labs 1–10 |
| `lab0/logs/verification_results.json` | Pass/fail per check |
| `workspace/logs/lab0-setup.log` | Setup timestamp log |

---

## Next lab

[Lab 1: Secure MLOps Environment Setup](../lab1/README.md) — creates KMS, S3, IAM, SageMaker Studio, and CloudTrail in AWS.
