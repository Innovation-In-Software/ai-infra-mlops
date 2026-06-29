# Optional follow-on labs (post-course)

These modules run **after** the main Labs 0–10 path. They use **real AWS services** that the classroom labs simplify for time and cost.

| Module | AWS services | Time | Prerequisite |
|--------|--------------|------|--------------|
| **[Lab 3b](lab3b/STEPS.md)** | SageMaker **Training Job** (managed compute) | ~45–60 min | Labs 1–3 complete |
| **[Lab 4b](lab4b/STEPS.md)** | **CodePipeline** + **CodeBuild** | ~45–60 min | Labs 1–4 complete · **verified on EC2** |

## Why these exist

- **Lab 3** trains models on EC2 CPU and only registers SageMaker Experiments.
- **Lab 4** writes pipeline JSON locally and does not create CodePipeline.

Labs **3b** and **4b** close that gap for participants who want full AWS execution.

## Paths

| Purpose | Location |
|---------|----------|
| Guides | `~/ai-infra-mlops/optional/lab3b/STEPS.md`, `optional/lab4b/STEPS.md` |
| Scripts | `optional/lab3b/scripts/`, `optional/lab4b/scripts/` |
| Outputs | `~/ai-infra-mlops/workspace/optional-lab3b/`, `workspace/optional-lab4b/` |

## Cost warning

- **Lab 3b:** SageMaker `ml.m5.large` training (~$0.12/hr; a few minutes of billable time).
- **Lab 4b:** CodePipeline + CodeBuild (small charge per run).

Run **`teardown_lab3b.py`** / **`teardown_lab4b.py`** when finished to avoid ongoing cost.

**Lab 4b note:** Banking S3 buckets use SSE-KMS. If Source stage fails, run `python3 scripts/patch_iam_for_lab4b.py` on EC2 (see [lab4b/STEPS.md](lab4b/STEPS.md)).

## Start here

```bash
cd ~/ai-infra-mlops && git pull
cd optional/lab3b    # or optional/lab4b
```

See also: [Real vs simulated in main labs](../docs/REAL-VS-SIMULATED.md)
