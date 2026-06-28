"""Validate optional Lab 3b."""
import json
import sys

import boto3

from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 3b (SageMaker Training Job)")
    print("=" * 60)
    ok = True

    cfg_path = CONFIG_DIR / "training_job.json"
    if not cfg_path.exists():
        print("   ❌ Missing config/training_job.json — run run_training_job.py")
        sys.exit(1)

    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)

    job_name = cfg.get("job_name")
    sm = boto3.client("sagemaker", region_name="us-west-2")
    resp = sm.describe_training_job(TrainingJobName=job_name)
    status = resp["TrainingJobStatus"]
    print(f"   ✅ Training job in AWS: {job_name}")
    print(f"   ✅ Status: {status}")
    print(f"   ✅ Model artifact: {resp.get('ModelArtifacts', {}).get('S3ModelArtifacts', 'n/a')}")

    if status != "Completed":
        print(f"   ❌ Expected Completed, got {status}")
        ok = False

    print("\n" + "=" * 60)
    if ok:
        print("Lab 3b OK — training job visible in SageMaker console")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
