"""Validate optional Lab 4b — pipeline exists and last run succeeded."""
import json
import sys

import boto3

from lab_paths import CONFIG_DIR, REGION, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 4b (CodePipeline)")
    print("=" * 60)
    ok = True

    cfg_path = CONFIG_DIR / "codepipeline.json"
    if not cfg_path.exists():
        print("   ❌ Missing codepipeline.json")
        sys.exit(1)

    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)

    pipeline_name = cfg["pipeline_name"]
    cp = boto3.client("codepipeline", region_name=REGION)
    cp.get_pipeline(name=pipeline_name)
    print(f"   ✅ Pipeline in AWS: {pipeline_name}")

    exec_path = CONFIG_DIR / "last_execution.json"
    if exec_path.exists():
        with open(exec_path, encoding="utf-8") as f:
            last = json.load(f)
        print(f"   ✅ Last execution: {last.get('execution_id')}")
        print(f"   ✅ Status: {last.get('status')}")
        if last.get("status") != "Succeeded":
            ok = False
    else:
        print("   ⚠️ No last_execution.json — run start_pipeline.py")
        ok = False

    print("\n" + "=" * 60)
    if ok:
        print("Lab 4b OK — real CodePipeline ran in AWS")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
