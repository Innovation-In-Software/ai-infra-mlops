"""Sync Lab 6 workspace config from live SageMaker endpoints and finish Steps 7–10.

Use when deploy_production.py failed on quota but endpoints exist, or after
manual endpoint cleanup. Run on EC2 with course AWS credentials:

    cd ~/ai-infra-mlops/lab6
    python3 scripts/repair_lab6_from_aws.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION, sample_features_for_model

from lab_paths import CONFIG_DIR, LAB3, ensure_workspace
from sm_deploy import invoke_endpoint, update_traffic_weights

PREFIXES = ("banking-endpoint-staging-", "banking-endpoint-prod-")


def _latest_endpoint(sm, prefix: str) -> dict | None:
    resp = sm.list_endpoints(
        SortBy="CreationTime",
        SortOrder="Descending",
        MaxResults=100,
        NameContains=prefix.rstrip("-"),
    )
    for ep in resp.get("Endpoints", []):
        name = ep["EndpointName"]
        if name.startswith(prefix) and ep.get("EndpointStatus") == "InService":
            detail = sm.describe_endpoint(EndpointName=name)
            return detail
    return None


def _sync_deployment_json(sm, detail: dict, *, environment: str) -> dict:
    name = detail["EndpointName"]
    cfg_name = detail["EndpointConfigName"]
    cfg = sm.describe_endpoint_config(EndpointConfigName=cfg_name)
    variants = cfg.get("ProductionVariants", [])
    record = {
        "endpoint": name,
        "endpoint_arn": detail["EndpointArn"],
        "endpoint_status": detail["EndpointStatus"],
        "endpoint_config": cfg_name,
        "instance_type": variants[0]["InstanceType"] if variants else "ml.m5.large",
        "region": REGION,
        "created_at": detail.get("CreationTime", datetime.now(timezone.utc)).isoformat(),
        "environment": environment,
        "dry_run": False,
        "reused": True,
        "source": "repair_lab6_from_aws",
    }
    if environment == "staging":
        record["model"] = variants[0]["ModelName"] if variants else ""
        record["variant"] = variants[0]["VariantName"] if variants else "staging"
    else:
        record["variants"] = [v["VariantName"] for v in variants]
        record["autoscaling"] = False
    return record


def main():
    ensure_workspace()
    print("Lab 6 — repair from AWS")
    print("=" * 60)

    # Ensure prerequisite JSON exists (reads Labs 1/3/5 workspace)
    from configure_blue_green import main as bg_main
    from prepare_deployment import main as prep_main

    if not (CONFIG_DIR / "deployment_state.json").exists():
        prep_main()
    if not (CONFIG_DIR / "blue_green_plan.json").exists():
        bg_main()

    sm = boto3.client("sagemaker", region_name=REGION)
    staging_detail = _latest_endpoint(sm, PREFIXES[0])
    prod_detail = _latest_endpoint(sm, PREFIXES[1])

    if not staging_detail:
        print("   ❌ No InService staging endpoint found (banking-endpoint-staging-*)")
        sys.exit(1)
    if not prod_detail:
        print("   ❌ No InService production endpoint found (banking-endpoint-prod-*)")
        print("   Free 2 ml.m5.large slots, then run: python3 scripts/deploy_production.py")
        sys.exit(1)

    staging = _sync_deployment_json(sm, staging_detail, environment="staging")
    prod = _sync_deployment_json(sm, prod_detail, environment="production")

    with open(CONFIG_DIR / "staging_deployment.json", "w", encoding="utf-8") as f:
        json.dump(staging, f, indent=2)
    with open(CONFIG_DIR / "production_deployment.json", "w", encoding="utf-8") as f:
        json.dump(prod, f, indent=2)
    print(f"   ✅ Synced staging: {staging['endpoint']}")
    print(f"   ✅ Synced production: {prod['endpoint']}")

    # Step 5 — test staging if missing
    test_path = CONFIG_DIR / "test_staging.json"
    if not test_path.exists():
        print("\n▶ Test staging")
        result = invoke_endpoint(staging["endpoint"])
        with open(test_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"   ✅ Staging test latency: {result['latency_ms']}ms")

    # Steps 7–8 — traffic shift + rollback
    endpoint = prod["endpoint"]
    print("\n▶ Traffic shift (90 → 50 → 0 blue)")
    steps = []
    for blue in (90, 50, 0):
        green = 100 - blue
        update_traffic_weights(endpoint, blue, green, dry_run=False)
        label = f"Blue {blue}% / Green {green}%"
        steps.append(label)
        print(f"   Step {len(steps)}: {label}")

    with open(CONFIG_DIR / "traffic_shift.json", "w", encoding="utf-8") as f:
        json.dump(
            {"steps": steps, "endpoint": endpoint, "dry_run": False, "source": "sagemaker"},
            f,
            indent=2,
        )

    print("\n▶ Rollback drill")
    update_traffic_weights(endpoint, 100, 0, dry_run=False)
    rollback = {
        "endpoint": endpoint,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dry_run": False,
        "status": "ROLLED_BACK",
        "blue_weight": 100,
        "green_weight": 0,
        "source": "sagemaker",
    }
    with open(CONFIG_DIR / "rollback_log.json", "w", encoding="utf-8") as f:
        json.dump(rollback, f, indent=2)
    print("   ✅ Restored blue variant to 100%")

    # Step 9 — report
    from generate_deployment_report import main as report_main

    report_main()

    # Step 10 — validate
    from validate_lab6 import main as validate_main

    print()
    validate_main()


if __name__ == "__main__":
    main()
