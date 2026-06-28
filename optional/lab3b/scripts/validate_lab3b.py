"""Validate optional Lab 3b."""
import json
import sys

import boto3
from botocore.exceptions import ClientError

from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 3b (SageMaker managed job)")
    print("=" * 60)

    cfg_path = CONFIG_DIR / "training_job.json"
    if not cfg_path.exists():
        print("   ❌ Missing config/training_job.json — run run_training_job.py")
        sys.exit(1)

    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)

    job_name = cfg.get("job_name")
    job_type = cfg.get("job_type", "training")
    sm = boto3.client("sagemaker", region_name="us-west-2")

    try:
        if job_type == "processing":
            resp = sm.describe_processing_job(ProcessingJobName=job_name)
            status = resp["ProcessingJobStatus"]
            print(f"   ✅ Processing job in AWS: {job_name}")
        else:
            resp = sm.describe_training_job(TrainingJobName=job_name)
            status = resp["TrainingJobStatus"]
            print(f"   ✅ Training job in AWS: {job_name}")
    except ClientError as exc:
        print(f"   ❌ {exc.response['Error']['Message']}")
        sys.exit(1)

    print(f"   ✅ Status: {status}")
    print(f"   ✅ Job type: {job_type}")
    print(f"   ✅ Instance: {cfg.get('instance_type', 'n/a')}")

    if status != "Completed":
        print(f"   ❌ Expected Completed, got {status}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Lab 3b OK — SageMaker job visible in AWS console")


if __name__ == "__main__":
    main()
