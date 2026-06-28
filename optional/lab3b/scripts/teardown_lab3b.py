"""Delete Lab 3b training job artifacts (optional cleanup)."""
import json
import sys

import boto3

from lab_paths import CONFIG_DIR


def main():
    cfg_path = CONFIG_DIR / "training_job.json"
    if not cfg_path.exists():
        print("No training_job.json — nothing to clean up.")
        return

    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)
    job_name = cfg.get("job_name")
    sm = boto3.client("sagemaker", region_name="us-west-2")
    print(f"Lab 3b teardown — job {job_name} is retained in SageMaker history.")
    print("Delete model objects under s3://.../experiments/lab3b/ manually if needed.")
    print("To stop in-progress jobs: aws sagemaker stop-training-job --training-job-name", job_name)


if __name__ == "__main__":
    main()
