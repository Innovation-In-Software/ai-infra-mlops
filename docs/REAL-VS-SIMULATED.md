# Real vs simulated AWS in the main labs

The course is designed for **~30 minutes per lab** on a shared instructor account. **All lab commands run on EC2** (`whoami` = `ec2-user`) in VS Code Remote SSH — not on the ProTech Windows VM.

## Instructor verification path (EC2 + AWS)

| Labs | Status | AWS footprint |
|------|--------|----------------|
| **0–1** | Tested on EC2 | STS, KMS, S3, IAM, SageMaker Studio, CloudTrail |
| **2–3** | Tested on EC2 | S3, Feature Store, CloudWatch; training on EC2 CPU |
| **4** | Tested on EC2 | Local CI/CD JSON + compliance scripts (no CodePipeline) |
| **4b** | Tested on EC2 (optional) | **Real CodePipeline** + CodeBuild + S3 source |
| **5** | Run on EC2 | Docker on EC2, **real ECR** create/push/scan |
| **6–10** | Run on EC2 | Mix of real AWS APIs and timeboxed simulations (see below) |

**Optional full-AWS modules:** [Lab 3b](../optional/lab3b/STEPS.md) (SageMaker Processing), [Lab 4b](../optional/lab4b/STEPS.md) (CodePipeline).

## Summary table (Labs 0–10)

| Lab | Real AWS (from EC2) | Local / EC2 / simulated |
|-----|---------------------|-------------------------|
| **0** | STS identity check | Tooling, workspace folders |
| **1** | KMS, S3, IAM, SageMaker Studio, CloudTrail | Config JSON in `workspace/` |
| **2** | S3 uploads, Feature Store, CloudWatch | PII patterns (not Comprehend by default), pandas |
| **3** | SageMaker **Experiments** (optional API) | **Training on EC2** (sklearn/XGBoost), fairness, model files |
| **4** | STS account ID only | **No CodePipeline** — JSON configs + `simulate_pipeline_run.py` |
| **5** | Docker on EC2, **ECR** create/push/**scan** | Container runs locally on EC2 (`:8080`) |
| **6** | Endpoint config JSON, real account IDs | Blue/green traffic shift simulated |
| **7** | CloudWatch dashboards/alarms (where API succeeds) | Model Monitor schedule simulated |
| **8** | Pipeline definition files | SageMaker Pipeline execution simulated |
| **9–10** | Audit/governance where noted | Reports from accumulated artifacts |

## Lab 3 — why training is not a SageMaker Training Job

- **Time:** Submitting and waiting for a training job can exceed the whole lab slot.
- **Cost:** Training instances bill separately from EC2.
- **Focus:** Model comparison, fairness, and experiment tracking — not SageMaker Training configuration.
- **Chain:** Lab 5 needs `best_model.pkl` on disk for Docker.

**Optional full AWS path:** [Lab 3b — SageMaker Processing Job](../optional/lab3b/STEPS.md)

## Lab 4 — why CodePipeline is not created in main Lab 4

- **Time:** First pipeline run often takes 15–30+ minutes.
- **Focus:** Compliance gates (PII, fairness) and CI/CD **workflow** without console wiring in the main slot.

**Optional full AWS path:** [Lab 4b — Real CodePipeline](../optional/lab4b/STEPS.md) — **verified on EC2** with KMS-encrypted S3 buckets.

## How to verify your work in AWS

After Labs 1–3 you should see in **us-west-2**:

- S3 buckets `bank-mlops-<account-id>-*`
- IAM roles `BankingDataScientistRole`, etc.
- SageMaker Feature Store groups from Lab 2
- SageMaker Experiment `banking-risk-experiments` from Lab 3

After **Lab 4b** you should see:

- CodePipeline `banking-ml-cicd-lab4b-<account-id>`
- CodeBuild project `banking-ml-cicd-build-lab4b`

After **Lab 5** you should see:

- ECR repository `banking-ml-inference` with `latest` image and scan results

## EC2 shell rule

```bash
whoami          # must be ec2-user
aws sts get-caller-identity
cd ~/ai-infra-mlops && git pull
```

See [EC2 testing guide](EC2-TESTING.md) and [SSH + VS Code setup](SSH-VSCODE-SETUP.md).
