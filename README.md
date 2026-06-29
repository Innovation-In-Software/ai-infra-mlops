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

| Lab | Topic | Guides |
|:---:|-------|--------|
| **0** | Environment setup | [STEPS](lab0/STEPS.md) · [README](lab0/README.md) |
| **1** | Secure MLOps environment | [STEPS](lab1/STEPS.md) · [README](lab1/README.md) |
| **2** | Banking data & PII | [STEPS](lab2/STEPS.md) · [README](lab2/README.md) |
| **3** | Model training & fairness | [STEPS](lab3/STEPS.md) · [README](lab3/README.md) |
| **4** | CI/CD & compliance gates | [STEPS](lab4/STEPS.md) · [README](lab4/README.md) |
| **5** | Secure containerization | [STEPS](lab5/STEPS.md) · [README](lab5/README.md) |
| **6** | Blue-green deployment | [STEPS](lab6/STEPS.md) · [README](lab6/README.md) |
| **7** | Monitoring & observability | [STEPS](lab7/STEPS.md) · [README](lab7/README.md) |
| **8** | SageMaker Pipelines | [STEPS](lab8/STEPS.md) · [README](lab8/README.md) |
| **9** | Security & governance | [STEPS](lab9/STEPS.md) · [README](lab9/README.md) |
| **10** | Enterprise architecture capstone | [STEPS](lab10/STEPS.md) · [README](lab10/README.md) |

- **`STEPS.md`** — commands, expected output, and screenshots (follow this in class).
- **`README.md`** — lab flow, script reference, and workspace outputs (study / instructor notes).

**Classroom defaults (Lab 2):** `export LAB_NUM_RECORDS=1000` and `export LAB_USE_COMPREHEND=0`

---

## Lab overviews

### Lab 0 — Environment Setup & Prerequisites (~50–65 min)

Connect to EC2 via the training portal and VS Code Remote SSH, install Python, AWS CLI, and Docker, clone this repo, and scaffold `workspace/lab1`–`lab10`. Ends with **9/9** environment checks — no banking AWS resources are created yet.

### Lab 1 — Secure MLOps Environment Setup (~30–45 min)

Provision the AWS foundation: **KMS** keys, six **KMS-encrypted S3** buckets, three **IAM** banking roles, **SageMaker Studio**, and **CloudTrail** audit logging. All later labs depend on `workspace/lab1/config/`. Validation: **13/13 COMPLIANT**.

### Lab 2 — Banking Data Management & PII Protection (~30 min)

Generate synthetic banking data, detect and anonymize **PII**, run quality validation and **feature engineering**, load features into **SageMaker Feature Store**, and set a drift baseline. Produces `engineered_banking_data.csv` and `preprocessor.pkl` used through Lab 9.

### Lab 3 — Model Training & Fairness Testing (~30 min)

Train Logistic Regression, Random Forest, and **XGBoost** models; log runs to **SageMaker Experiments**; run **fairness** testing (disparate impact on `age_group`); select `best_model.pkl`. Optional Steps 10–12 (`optional/lab3b/`) run a managed SageMaker Processing training job.

### Lab 4 — CI/CD Pipeline with Compliance Gates (~30 min)

Scaffold a CI/CD project, run **pytest** compliance tests, enforce **PII / fairness / security** gates, simulate a **CodePipeline** run, and generate a CI/CD compliance report. Optional Steps 11–15 (`optional/lab4b/`) deploy a real **CodeBuild + CodePipeline** in AWS.

### Lab 5 — Secure Containerization for Banking (~30 min)

Package `best_model.pkl` into a **Docker** image (`banking-ml-inference`), test `/ping` and `/invocations` locally, push to **ECR** with KMS encryption, and run an **image vulnerability scan** for banking compliance.

### Lab 6 — Model Deployment with Blue-Green (~30–45 min)

Deploy the ECR image to **real SageMaker endpoints**: staging first, then production with **blue/green variants**, gradual **traffic shift**, and a **rollback** drill. Live AWS — no simulation.

### Lab 7 — Compliance Monitoring & Observability (~30 min)

Build **CloudWatch** dashboards and alarms on the production endpoint, run **data drift** and **model quality** checks, and complete an **incident response** drill. Links monitoring back to Lab 2 baseline data.

### Lab 8 — End-to-End SageMaker Pipeline (~30 min)

Define, upsert, and execute pipeline **`banking-ml-pipeline`** on SageMaker; monitor steps; **register** the model in the **`banking-risk-models`** Model Registry. Uses `pipeline/validate_data.py` as the processing-step entrypoint. Refresh IAM via `lab1/scripts/create_banking_iam_roles.py` before starting.

### Lab 9 — Banking Security & Governance Framework (~30 min)

**IAM** least-privilege review, **encryption** audit (S3, ECR, KMS), model **approval workflow**, **SHAP** explainability, governance **fairness** check, **CloudTrail** audit export, and final governance compliance report. Links Lab 1 security and Lab 8 model registry.

### Lab 10 — Enterprise MLOps Architecture (~30 min)

**Course capstone** (Module 11 maps here — no `lab11` folder). Collect artifacts from Labs 1–9, score **seven architecture layers** (target **100/100**), gap analysis, implementation roadmap, executive summary, and **`course_compliance_bundle.zip`**. Success: `🎉 COURSE COMPLETE`. Optional teardown: [Lab 10 Step 11](lab10/STEPS.md).

---

## Paths on EC2

| What | Where |
|------|--------|
| Repo | `~/ai-infra-mlops` |
| Step guides | `~/ai-infra-mlops/labN/STEPS.md` |
| Lab overviews & scripts | `~/ai-infra-mlops/labN/README.md` |
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
- [Lab 3b / 4b script folders](optional/README.md)
- [SSH + VS Code setup](docs/SSH-VSCODE-SETUP.md)
- [Instructor ProTech VM + EC2 setup](docs/PROTECH-VM-SETUP.md)
- [Instructor cloud delivery](CLOUD-DELIVERY.md)
- [EC2 testing notes](docs/EC2-TESTING.md)
- [Canonical repo / clone instructions](CANONICAL-REPO.md)
