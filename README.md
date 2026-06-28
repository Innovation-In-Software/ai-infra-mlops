# AI-MLOps on AWS — Participant Guide

**Class:** `ai-mlops-2026-jun30` · **Region:** `us-west-2`

Hands-on banking MLOps labs on **Amazon EC2** using **VS Code Remote SSH** and **bash**.  
Outputs are saved under `workspace/labN/` (not committed to git).

---

## How to follow the labs

1. **Lab 0:** [labs.protechtraining.com](https://labs.protechtraining.com) → training VM → AWS (`us-west-2`) → EC2 → [VS Code Remote SSH](docs/SSH-VSCODE-SETUP.md) — full steps in [lab0/STEPS.md](lab0/STEPS.md).
2. Open folder: `/home/ec2-user/ai-infra-mlops`
3. Configure AWS on EC2: `aws configure` with your instructor access keys — **never commit keys to git**.
4. Work through labs **in order** using each folder’s **`STEPS.md`** guide.
5. Each step has:
   - **Do this** — command to run in the terminal
   - **Expected result** — what you should see
   - **Screenshot (optional)** — for your notes only

```bash
cd ~/ai-infra-mlops
git pull
cd lab0    # then lab1, lab2, … lab10
```

---

## Lab path (0 → 10)

| Lab | Topic | Open this guide |
|:---:|-------|-----------------|
| **0** | Environment setup | [lab0/STEPS.md](lab0/STEPS.md) |
| **1** | Secure MLOps environment (KMS, S3, IAM, SageMaker) | [lab1/STEPS.md](lab1/STEPS.md) |
| **2** | Banking data, PII, Feature Store | [lab2/STEPS.md](lab2/STEPS.md) |
| **3** | Model training & fairness | [lab3/STEPS.md](lab3/STEPS.md) |
| **4** | CI/CD with compliance gates | [lab4/STEPS.md](lab4/STEPS.md) |
| **5** | Secure containerization (Docker, ECR) | [lab5/STEPS.md](lab5/STEPS.md) |
| **6** | Blue-green deployment | [lab6/STEPS.md](lab6/STEPS.md) |
| **7** | Monitoring & observability | [lab7/STEPS.md](lab7/STEPS.md) |
| **8** | SageMaker Pipelines | [lab8/STEPS.md](lab8/STEPS.md) |
| **9** | Security & governance | [lab9/STEPS.md](lab9/STEPS.md) |
| **10** | Enterprise architecture & course wrap-up | [lab10/STEPS.md](lab10/STEPS.md) |

**Classroom defaults (Lab 2):** `export LAB_NUM_RECORDS=1000` and `export LAB_USE_COMPREHEND=0`

---

## Paths on EC2

| What | Where |
|------|--------|
| Repo | `~/ai-infra-mlops` |
| Step guides | `~/ai-infra-mlops/labN/STEPS.md` |
| Your work / outputs | `~/ai-infra-mlops/workspace/labN/` |

---

## Fresh start (re-run labs)

```bash
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab1,lab2,lab3,lab4,lab5,lab6,lab7,lab8,lab9,lab10
cd lab2 && python3 scripts/cleanup_lab2.py --aws   # optional: Feature Groups
```

Then start again from [Lab 0](lab0/STEPS.md).

---

## After the course (instructor)

Teardown AWS resources: [Lab 10 Step 11](lab10/STEPS.md) → `python3 scripts/teardown_course.py --yes`

---

## More help

- [How to read STEPS.md](docs/READING-THE-LABS.md)
- [Real vs simulated AWS](docs/REAL-VS-SIMULATED.md)
- [Optional: Lab 3b SageMaker Training & Lab 4b CodePipeline](optional/README.md)
- [SSH + VS Code setup](docs/SSH-VSCODE-SETUP.md)
- [Instructor ProTech VM + EC2 setup](docs/PROTECH-VM-SETUP.md)
- [Instructor cloud delivery](CLOUD-DELIVERY.md)
- [EC2 testing notes](docs/EC2-TESTING.md)
- [Canonical repo / clone instructions](CANONICAL-REPO.md)
