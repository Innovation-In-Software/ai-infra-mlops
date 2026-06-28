# Real vs simulated AWS in the main labs

The course is designed for **~30 minutes per lab** on a shared instructor account. Most work runs on **EC2**; AWS is used where it teaches the banking MLOps story without long waits or high cost.

## Summary table (Labs 0–10)

| Lab | Real AWS | Local / EC2 / simulated |
|-----|----------|-------------------------|
| **0** | STS identity check | Tooling, workspace folders |
| **1** | KMS, S3, IAM, SageMaker Studio, CloudTrail | Config JSON in `workspace/` |
| **2** | S3 uploads, Feature Store, CloudWatch | PII patterns (not Comprehend by default), pandas |
| **3** | SageMaker **Experiments** (optional API) | **Training on EC2** (sklearn/XGBoost), fairness, model files |
| **4** | STS account ID only | **No CodePipeline** — JSON configs + `simulate_pipeline_run.py` |
| **5** | Docker, ECR create/push | Vulnerability scan simulated |
| **6–8** | Mix (deploy, monitoring setup) | Some traffic/pipeline steps simulated |
| **9–10** | Audit/governance where noted | Reports from accumulated artifacts |

## Lab 3 — why training is not a SageMaker Training Job

- **Time:** Submitting and waiting for a training job can exceed the whole lab slot.
- **Cost:** Training instances bill separately from EC2.
- **Focus:** Model comparison, fairness, and experiment tracking — not SageMaker Training configuration.
- **Chain:** Lab 5 needs `best_model.pkl` on disk for Docker.

**Optional full AWS path:** [Lab 3b — SageMaker Training Job](../optional/lab3b/STEPS.md)

## Lab 4 — why CodePipeline is not created

- **Time:** Repo connection, CodeBuild, and first pipeline run often take 15–30+ minutes.
- **Complexity:** IAM and artifact wiring block many classrooms if something fails.
- **Focus:** Compliance gates (PII, fairness) and CI/CD **workflow**, not console pipeline wiring.
- **Sequencing:** Real packaging/deploy is Labs 5–6.

**Optional full AWS path:** [Lab 4b — Real CodePipeline](../optional/lab4b/STEPS.md)

## How to verify your work in AWS

After Labs 1–3 you should see in **us-west-2**:

- S3 buckets `bank-mlops-<account-id>-*`
- IAM roles `BankingDataScientistRole`, etc.
- SageMaker Feature Store groups from Lab 2
- SageMaker Experiment `banking-risk-experiments` from Lab 3

After Lab 4 you should **not** see a CodePipeline (expected until Lab 4b).
