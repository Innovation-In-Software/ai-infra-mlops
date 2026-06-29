"""Build and upsert SageMaker Pipeline."""
import argparse
import json
import sys
from pathlib import Path

import boto3
import sagemaker
from sagemaker.processing import ProcessingInput
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.workflow.parameters import ParameterString
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION, load_buckets, load_iam_role, write_json

from lab_paths import CONFIG_DIR, PIPELINE_DIR, ensure_workspace

PIPELINE_NAME = "banking-ml-pipeline"
PROCESSING_INSTANCE = "ml.t3.medium"


def _load_params():
    path = CONFIG_DIR / "pipeline_params.json"
    if not path.exists():
        print("   ❌ Run define_pipeline_params.py first.")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_pipeline(session, role_arn, input_s3_uri):
    param_input = ParameterString(name="InputDataUri", default_value=input_s3_uri)
    processor = SKLearnProcessor(
        framework_version="1.2-1",
        role=role_arn,
        instance_type=PROCESSING_INSTANCE,
        instance_count=1,
        base_job_name="banking-pipeline-validate",
        sagemaker_session=session,
    )
    step = ProcessingStep(
        name="DataValidation",
        processor=processor,
        inputs=[ProcessingInput(source=param_input, destination="/opt/ml/processing/input")],
        code=str(PIPELINE_DIR / "validate_data.py"),
        job_arguments=["--input", "/opt/ml/processing/input"],
    )
    return Pipeline(
        name=PIPELINE_NAME,
        parameters=[param_input],
        steps=[step],
        sagemaker_session=session,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()
    params = _load_params()
    input_uri = params.get("input_s3_uri")
    if not input_uri:
        print("   ❌ pipeline_params.json missing input_s3_uri")
        sys.exit(1)

    if args.dry_run:
        reg = {"pipeline_name": PIPELINE_NAME, "dry_run": True, "status": "Registered"}
        write_json(CONFIG_DIR / "pipeline_registration.json", reg)
        print(f"   ✅ Pipeline name: {PIPELINE_NAME}")
        print("✅ Pipeline registered (dry-run)")
        return

    role_arn = load_iam_role("ml_engineer")
    buckets = load_buckets()
    default_bucket = buckets["processed"]["name"]
    session = sagemaker.Session(
        boto_session=boto3.Session(region_name=REGION),
        default_bucket=default_bucket,
    )
    pipeline = build_pipeline(session, role_arn, input_uri)
    response = pipeline.upsert(role_arn=role_arn)
    arn = response["PipelineArn"]
    reg = {
        "pipeline_name": PIPELINE_NAME,
        "pipeline_arn": arn,
        "input_s3_uri": input_uri,
        "status": "Registered",
        "source": "sagemaker",
    }
    write_json(CONFIG_DIR / "pipeline_registration.json", reg)
    print(f"   ✅ Pipeline name: {PIPELINE_NAME}")
    print(f"   ✅ Pipeline ARN: {arn}")
    print("✅ Pipeline registered")


if __name__ == "__main__":
    main()
