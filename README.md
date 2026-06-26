# AI Infrastructure & MLOps on AWS
## Class: `ai-mlops-2026-jun30`

**Repository:** [github.com/Innovation-In-Software/ai-infra-mlops](https://github.com/Innovation-In-Software/ai-infra-mlops)

This is the **only repo participants need**. It contains lab scripts, step-by-step guides, and screenshots.

**Region:** `us-west-2` (Oregon) only.

---

## What you need on your laptop

| Tool | Check |
|------|-------|
| VS Code | Installed |
| Python 3.8+ | `python --version` |
| Git | `git --version` |
| AWS CLI v2 | `aws --version` |
| AWS credentials | From instructor handout |

---

## Setup (one time)

```powershell
cd D:\Current_work
git clone https://github.com/Innovation-In-Software/ai-infra-mlops.git
cd ai-infra-mlops
code .
```

Then open **[GETTING_STARTED.md](GETTING_STARTED.md)** and follow Lab 0.

---

## Folder layout

```
ai-infra-mlops/
├── README.md              ← You are here
├── GETTING_STARTED.md     ← Credentials + first steps
├── guides/                ← Step-by-step with screenshots
│   └── lab0/
│       ├── LAB_GUIDE.md
│       └── images/
└── labs/                  ← Lab scripts (run from here)
    └── Lab_0_Environment_Setup_and_Prerequisites/
        ├── scripts/
        ├── requirements.txt
        └── ...
```

Your personal workspace (created in Lab 0) lives at:

`%USERPROFILE%\Documents\banking-mlops-labs`

---

## Lab index

| Lab | Guide | Scripts folder |
|-----|-------|----------------|
| **0** | [guides/lab0/LAB_GUIDE.md](guides/lab0/LAB_GUIDE.md) | `labs/Lab_0_Environment_Setup_and_Prerequisites/` |
| 1.1 | *coming soon* | *coming soon* |
| 1.2 | *coming soon* | *coming soon* |

---

## Security

- Never commit AWS keys or passwords.
- Usernames are **case-sensitive** (`Student01` ≠ `student01`).

**Start Lab 0:** [guides/lab0/LAB_GUIDE.md](guides/lab0/LAB_GUIDE.md)
