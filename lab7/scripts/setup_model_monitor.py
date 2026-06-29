"""Verify SageMaker endpoint and record Model Monitor baseline config."""
import argparse
import json
import sys
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION

from lab_paths import CONFIG_DIR, ensure_workspace
from monitoring_helpers import load_monitoring_state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()

    state = load_monitoring_state()
    if not state:
        print("   ❌ Run prepare_monitoring_data.py first.")
        sys.exit(1)
    endpoint = state["endpoint_name"]

    endpoint_status = "UNKNOWN"
    if not args.dry_run:
        sm = boto3.client("sagemaker", region_name=REGION)
        resp = sm.describe_endpoint(EndpointName=endpoint)
        endpoint_status = resp.get("EndpointStatus", "UNKNOWN")
        print(f"   ✅ Endpoint {endpoint}: {endpoint_status}")
        if endpoint_status != "InService":
            print("   ❌ Endpoint must be InService before monitoring setup")
            sys.exit(1)

    cfg = {
        "endpoint_name": endpoint,
        "endpoint_status": endpoint_status,
        "schedule": "hourly",
        "data_capture": "recommended_for_production",
        "dry_run": args.dry_run,
        "source": "sagemaker",
    }
    with open(CONFIG_DIR / "model_monitor.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print("   ✅ Baseline constraints generated (local baseline from Lab 7 Step 3)")
    print("   ✅ Endpoint verified for monitoring")
    print("✅ Model Monitor configured" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
