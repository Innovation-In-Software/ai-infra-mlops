"""Monitor pipeline step status from SageMaker."""
import argparse
import json
import sys
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION, write_json

from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()

    exec_path = CONFIG_DIR / "pipeline_execution.json"
    if not exec_path.exists():
        print("   ❌ Run start_pipeline.py first.")
        sys.exit(1)
    with open(exec_path, encoding="utf-8") as f:
        execution = json.load(f)

    if args.dry_run or execution.get("dry_run"):
        steps = {"DataValidation": "Succeeded"}
        write_json(CONFIG_DIR / "pipeline_monitor.json", steps)
        for name, status in steps.items():
            print(f"   {name:<22} ✅ {status}")
        print("✅ All steps succeeded (dry-run)")
        return

    sm = boto3.client("sagemaker", region_name=REGION)
    arn = execution["execution_arn"]
    resp = sm.list_pipeline_execution_steps(PipelineExecutionArn=arn)
    steps = {}
    for step in resp.get("PipelineExecutionSteps", []):
        name = step.get("StepName", "unknown")
        status = step.get("StepStatus", "Unknown")
        steps[name] = status
        mark = "✅" if status == "Succeeded" else "❌" if status == "Failed" else "…"
        print(f"   {name:<22} {mark} {status}")

    write_json(CONFIG_DIR / "pipeline_monitor.json", {"steps": steps, "source": "sagemaker"})
    failed = [s for s, st in steps.items() if st != "Succeeded"]
    if failed:
        print(f"   ❌ Failed steps: {', '.join(failed)}")
        sys.exit(1)
    print("✅ All pipeline steps succeeded")


if __name__ == "__main__":
    main()
