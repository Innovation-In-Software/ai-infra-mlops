"""Launch a SageMaker sklearn Training Job (Lab 3b)."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from scripts.course_common import write_json

from lab_paths import CONFIG_DIR, LAB1_CONFIG, ROOT, ensure_workspace


def main():
    ensure_workspace()
    print("🏋️ SageMaker Training Job (Lab 3b)")
    print("=" * 60)

    s3_cfg_path = CONFIG_DIR / "s3_training_data.json"
    if not s3_cfg_path.exists():
        print("   ❌ Run upload_training_data.py first.")
        sys.exit(1)

    with open(s3_cfg_path, encoding="utf-8") as f:
        s3_cfg = json.load(f)
    with open(LAB1_CONFIG / "iam_roles.json", encoding="utf-8") as f:
        roles = json.load(f)
    with open(LAB1_CONFIG / "buckets.json", encoding="utf-8") as f:
        buckets = json.load(f)

    role_arn = roles["data_scientist"]["arn"]
    output_path = f"s3://{buckets['models']['name']}/experiments/lab3b/"
    job_name = f"banking-rf-lab3b-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

    import boto3
    import sagemaker
    from sagemaker.inputs import TrainingInput
    from sagemaker.sklearn import SKLearn

    session = sagemaker.Session(boto_session=boto3.Session(region_name="us-west-2"))
    train_uri = s3_cfg["train_prefix"]

    estimator = SKLearn(
        entry_point="train.py",
        source_dir=str(ROOT / "source"),
        role=role_arn,
        instance_count=1,
        instance_type="ml.m5.large",
        framework_version="1.2-1",
        py_version="py3",
        output_path=output_path,
        sagemaker_session=session,
        base_job_name="banking-rf-lab3b",
    )

    print(f"   Role: {role_arn}")
    print(f"   Input: {train_uri}")
    print(f"   Output: {output_path}")
    print(f"   Instance: ml.m5.large")
    print("\n   ⏳ Starting training job (typically 3–8 minutes)...")

    estimator.fit(
        {"train": TrainingInput(train_uri, content_type="text/csv")},
        job_name=job_name,
        wait=True,
    )

    job_config = {
        "job_name": estimator.latest_training_job.name,
        "role_arn": role_arn,
        "output_path": output_path,
        "model_data": estimator.model_data,
        "status": "Completed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    write_json(CONFIG_DIR / "training_job.json", job_config)
    print(f"\n   ✅ Training job: {job_config['job_name']}")
    print(f"   ✅ Model artifact: {job_config['model_data']}")
    print("✅ SageMaker training complete")


if __name__ == "__main__":
    main()
