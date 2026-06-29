"""Create CloudWatch dashboard for SageMaker endpoint metrics."""
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
        print("   ❌ Run prepare_monitoring_data.py first (needs Lab 6 endpoint).")
        sys.exit(1)
    endpoint = state["endpoint_name"]
    dashboard_name = "Banking-MLOps-Model-Monitor"

    body = {
        "widgets": [
            {
                "type": "metric",
                "x": 0,
                "y": 0,
                "width": 12,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/SageMaker", "Invocations", "EndpointName", endpoint, "VariantName", "staging"],
                        ["...", "...", "...", endpoint, "...", "banking-model-blue"],
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": REGION,
                    "title": "Invocations",
                    "period": 300,
                    "stat": "Sum",
                },
            },
            {
                "type": "metric",
                "x": 12,
                "y": 0,
                "width": 12,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/SageMaker", "ModelLatency", "EndpointName", endpoint],
                    ],
                    "view": "timeSeries",
                    "region": REGION,
                    "title": "Model Latency",
                    "period": 300,
                    "stat": "Average",
                },
            },
        ]
    }

    cfg = {
        "dashboard": dashboard_name,
        "endpoint_name": endpoint,
        "widgets": ["invocations", "latency"],
        "dry_run": args.dry_run,
        "source": "cloudwatch",
    }

    if not args.dry_run:
        cw = boto3.client("cloudwatch", region_name=REGION)
        cw.put_dashboard(DashboardName=dashboard_name, DashboardBody=json.dumps(body))
        print(f"   ✅ Dashboard created in CloudWatch: {dashboard_name}")

    with open(CONFIG_DIR / "dashboard_config.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print("📊 CloudWatch Dashboard")
    print("=" * 60)
    print(f"   ✅ Dashboard: {dashboard_name}")
    print("✅ Dashboard configuration saved")


if __name__ == "__main__":
    main()
