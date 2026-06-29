"""Start SageMaker Pipeline execution."""
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION, wait_for_status, write_json

from lab_paths import CONFIG_DIR, ensure_workspace

PIPELINE_NAME = "banking-ml-pipeline"
MAX_WAIT_SEC = 1800


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()

    reg_path = CONFIG_DIR / "pipeline_registration.json"
    if not reg_path.exists():
        print("   ❌ Run upsert_pipeline.py first.")
        sys.exit(1)
    with open(reg_path, encoding="utf-8") as f:
        reg = json.load(f)

    params_path = CONFIG_DIR / "pipeline_params.json"
    with open(params_path, encoding="utf-8") as f:
        params = json.load(f)
    input_uri = params.get("input_s3_uri")

    if args.dry_run or reg.get("dry_run"):
        execution = {
            "execution_arn": f"arn:aws:sagemaker:{REGION}:000000000000:pipeline/{PIPELINE_NAME}/execution/dryrun",
            "status": "Executing",
            "dry_run": True,
        }
        write_json(CONFIG_DIR / "pipeline_execution.json", execution)
        print(f"   Execution ARN: {execution['execution_arn']}")
        print("✅ Pipeline started (dry-run)")
        return

    sm = boto3.client("sagemaker", region_name=REGION)
    resp = sm.start_pipeline_execution(
        PipelineName=PIPELINE_NAME,
        PipelineParameters=[{"Name": "InputDataUri", "Value": input_uri}],
    )
    execution_arn = resp["PipelineExecutionArn"]
    print("▶️ Pipeline Execution")
    print("=" * 60)
    print(f"   Execution ARN: {execution_arn}")

    def describe():
        return sm.describe_pipeline_execution(PipelineExecutionArn=execution_arn)

    final = wait_for_status(
        describe,
        "PipelineExecutionStatus",
        {"Succeeded", "Failed", "Stopped"},
        timeout_sec=MAX_WAIT_SEC,
        poll_sec=30,
        label="pipeline execution",
    )
    status = final["PipelineExecutionStatus"]
    execution = {
        "execution_arn": execution_arn,
        "status": status,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "source": "sagemaker",
    }
    write_json(CONFIG_DIR / "pipeline_execution.json", execution)
    if status != "Succeeded":
        print(f"   ❌ Pipeline finished with status: {status}")
        steps_resp = sm.list_pipeline_execution_steps(PipelineExecutionArn=execution_arn)
        for step in steps_resp.get("PipelineExecutionSteps", []):
            step_status = step.get("StepStatus", "Unknown")
            if step_status in ("Failed", "Stopped"):
                reason = step.get("FailureReason") or step.get("Metadata", {}).get("FailureReason", "unknown")
                print(f"   Step {step.get('StepName')}: {step_status} — {reason}")
        sys.exit(1)
    print("✅ Pipeline started and completed successfully")


if __name__ == "__main__":
    main()
