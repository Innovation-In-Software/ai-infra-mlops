"""Start Lab 4b pipeline execution and wait for completion."""
import json
import sys
import time
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from scripts.course_common import write_json

from lab_paths import CONFIG_DIR, REGION, ensure_workspace


def main():
    ensure_workspace()
    print("▶ Start CodePipeline execution")
    print("=" * 60)

    cfg_path = CONFIG_DIR / "codepipeline.json"
    if not cfg_path.exists():
        print("   ❌ Run create_codepipeline.py first.")
        sys.exit(1)

    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)

    pipeline_name = cfg["pipeline_name"]
    cp = boto3.client("codepipeline", region_name=REGION)
    resp = cp.start_pipeline_execution(name=pipeline_name)
    execution_id = resp["pipelineExecutionId"]
    print(f"   ✅ Started execution: {execution_id}")

    deadline = time.time() + 900
    while time.time() < deadline:
        status = cp.get_pipeline_execution(
            pipelineName=pipeline_name, pipelineExecutionId=execution_id
        )["pipelineExecution"]["status"]
        print(f"   ... status: {status}")
        if status in ("Succeeded", "Failed", "Stopped", "Superseded"):
            break
        time.sleep(15)

    write_json(
        CONFIG_DIR / "last_execution.json",
        {"pipeline_name": pipeline_name, "execution_id": execution_id, "status": status},
    )

    if status == "Succeeded":
        print("✅ Pipeline execution succeeded")
    else:
        print(f"❌ Pipeline ended with status: {status}")
        print("   Check CodePipeline console → execution history → Build logs")
        sys.exit(1)


if __name__ == "__main__":
    main()
