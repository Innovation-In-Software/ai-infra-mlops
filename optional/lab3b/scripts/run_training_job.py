"""Launch SageMaker managed training via Processing Job (Lab 3b).

Many classroom/sandbox accounts have **zero Training Job instance quota**.
This script uses a SageMaker Processing Job on ml.t3.medium (usually allowed)
to run the same train.py Random Forest script on AWS-managed compute.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from scripts.course_common import write_json

from lab_paths import CONFIG_DIR, LAB1_CONFIG, ROOT, ensure_workspace

INSTANCE = "ml.t3.medium"


def _load_config():
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
    return s3_cfg, roles["data_scientist"]["arn"], buckets["models"]["name"]


def _run_processing(role_arn, train_uri, output_path, default_bucket):
    import boto3
    import sagemaker
    from sagemaker.processing import ProcessingInput, ProcessingOutput
    from sagemaker.sklearn.processing import SKLearnProcessor

    session = sagemaker.Session(
        boto_session=boto3.Session(region_name="us-west-2"),
        default_bucket=default_bucket,
    )
    processor = SKLearnProcessor(
        framework_version="1.2-1",
        role=role_arn,
        instance_type=INSTANCE,
        instance_count=1,
        base_job_name="banking-rf-lab3b",
        sagemaker_session=session,
    )

    print(f"   Mode: SageMaker Processing Job ({INSTANCE})")
    print("   Note: Training Job quota is 0 on many sandbox accounts — Processing is equivalent managed compute.")

    processor.run(
        code=str(ROOT / "source" / "train.py"),
        inputs=[
            ProcessingInput(
                source=train_uri,
                destination="/opt/ml/processing/input/train",
                s3_data_type="S3Prefix",
            )
        ],
        outputs=[
            ProcessingOutput(
                output_name="model",
                source="/opt/ml/processing/output",
                destination=output_path,
                s3_upload_mode="EndOfJob",
            )
        ],
        arguments=[
            "--train",
            "/opt/ml/processing/input/train",
            "--model-dir",
            "/opt/ml/processing/output",
        ],
        wait=True,
    )
    return processor.latest_job.name, output_path


def _run_training(role_arn, train_uri, output_path, job_name, default_bucket):
    import boto3
    import sagemaker
    from sagemaker.inputs import TrainingInput
    from sagemaker.sklearn import SKLearn

    session = sagemaker.Session(
        boto_session=boto3.Session(region_name="us-west-2"),
        default_bucket=default_bucket,
    )
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
    print("   Mode: SageMaker Training Job (ml.m5.large)")
    estimator.fit(
        {"train": TrainingInput(train_uri, content_type="text/csv")},
        job_name=job_name,
        wait=True,
    )
    return estimator.latest_training_job.name, estimator.model_data


def main():
    ensure_workspace()
    print("🏋️ SageMaker Managed Training (Lab 3b)")
    print("=" * 60)

    s3_cfg, role_arn, models_bucket = _load_config()
    train_uri = s3_cfg["train_prefix"]
    output_path = f"s3://{models_bucket}/experiments/lab3b/"
    job_name = f"banking-rf-lab3b-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

    print(f"   Role: {role_arn}")
    print(f"   Input: {train_uri}")
    print(f"   Output: {output_path}")
    print(f"   SDK bucket: {models_bucket}")
    print("\n   ⏳ Starting SageMaker job (typically 3–8 minutes)...")

    mode = "processing"
    artifact_uri = output_path
    try:
        if __import__("os").environ.get("LAB3B_USE_TRAINING") == "1":
            job_id, artifact_uri = _run_training(role_arn, train_uri, output_path, job_name, models_bucket)
            mode = "training"
        else:
            job_id, artifact_uri = _run_processing(role_arn, train_uri, output_path, models_bucket)
    except Exception as exc:
        err = str(exc)
        if "ResourceLimitExceeded" in err and "training job" in err.lower():
            print("\n   ⚠️ Training Job quota is 0 — retrying with Processing Job...")
            job_id, artifact_uri = _run_processing(role_arn, train_uri, output_path, models_bucket)
            mode = "processing"
        elif "s3:ListBucket" in err or "not authorized" in err.lower():
            print("\n   ❌ SageMaker execution role needs S3 on the SDK bucket.")
            print("   Run: python3 scripts/patch_iam_for_sagemaker.py")
            print("   Wait 10 seconds, then re-run this script.")
            sys.exit(1)
        else:
            raise

    job_config = {
        "job_name": job_id,
        "job_type": mode,
        "role_arn": role_arn,
        "output_path": output_path,
        "model_data": artifact_uri,
        "instance_type": INSTANCE if mode == "processing" else "ml.m5.large",
        "status": "Completed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    write_json(CONFIG_DIR / "training_job.json", job_config)
    print(f"\n   ✅ SageMaker job: {job_id} ({mode})")
    print(f"   ✅ Output: {artifact_uri}")
    print("✅ SageMaker managed training complete")


if __name__ == "__main__":
    main()
