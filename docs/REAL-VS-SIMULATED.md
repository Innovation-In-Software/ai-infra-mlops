# Real vs simulated AWS in the main labs

All lab commands run on **EC2** (`whoami` = `ec2-user`) in VS Code Remote SSH — not on the ProTech Windows VM.

## Lab path (what runs where)

| Lab | Real AWS (from EC2) | Simulated / local on EC2 |
|-----|---------------------|---------------------------|
| **0** | STS identity check | Tooling, workspace folders |
| **1** | KMS, S3, IAM, SageMaker Studio, CloudTrail | Config JSON in `workspace/` |
| **2** | S3 uploads, Feature Store, CloudWatch | PII patterns (not Comprehend by default) |
| **3** (Steps 1–9) | SageMaker **Experiments** API | Training on EC2 CPU |
| **3** (Steps 10–12) | **SageMaker Processing Job**, S3 training data | — |
| **4** (Steps 1–10) | STS account ID | CI/CD JSON + `simulate_pipeline_run.py` |
| **4** (Steps 11–15) | **CodePipeline**, **CodeBuild**, S3 artifacts | — |
| **5** | Docker on EC2, **ECR** create/push/scan | Container test on `:8080` |
| **6** | **SageMaker** staging + production endpoints, blue/green traffic shift, invoke test | Blue/green plan JSON (local) |
| **7** | **CloudWatch** dashboard + alarms, endpoint metrics | Drift CSV analysis (local) |
| **8** | **SageMaker Pipeline** (Processing step), **Model Registry** | Local pipeline definition mirror |
| **9** | **IAM** review, S3/ECR encryption audit, **CloudTrail** lookup | Fairness report from Lab 3 |
| **10** | Artifact collection + live resource checks | Roadmap/checklist reports (local) |

## Why Lab 3 has two training paths

- **Steps 1–9:** Fast EC2 training for model comparison, fairness, and `best_model.pkl` (needed for Lab 5 Docker).
- **Steps 10–12:** Same Random Forest on **SageMaker managed compute** so you see Processing jobs in the console.

## Why Lab 4 has two CI/CD paths

- **Steps 1–10:** Compliance gates and pipeline **workflow** without waiting for CodeBuild in class.
- **Steps 11–15:** **Real** S3 → CodeBuild pipeline in AWS (KMS-encrypted banking buckets).

## How to verify in the AWS console (`us-west-2`)

After **Lab 3 Step 12:**

- SageMaker → **Processing jobs** → `banking-rf-lab3b-*` → **Completed**

After **Lab 4 Step 15:**

- CodePipeline → `banking-ml-cicd-lab4b-<account-id>` → last run **Succeeded**
- CodeBuild → `banking-ml-cicd-build-lab4b`

After **Lab 5:**

- ECR → `banking-ml-inference` → image `latest` + scan results

After **Lab 6:**

- SageMaker → **Endpoints** → `banking-endpoint-staging-*` and `banking-endpoint-prod-*` → **In service**

After **Lab 8:**

- SageMaker → **Pipelines** → `banking-ml-pipeline` → execution **Succeeded**
- SageMaker → **Model registry** → `banking-risk-models`

## EC2 shell rule

```bash
whoami          # ec2-user
aws sts get-caller-identity
cd ~/ai-infra-mlops && git pull
```

Guides: [Lab 3 Steps 10–12](lab3/STEPS.md) · [Lab 4 Steps 11–15](lab4/STEPS.md) · [Lab 10 optional teardown](lab10/STEPS.md) · [EC2 testing](EC2-TESTING.md)
