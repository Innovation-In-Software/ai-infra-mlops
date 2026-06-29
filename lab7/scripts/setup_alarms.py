"""Configure CloudWatch alarms for SageMaker endpoint."""
import argparse
import json
import sys
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION, account_id

from lab_paths import CONFIG_DIR, ensure_workspace
from monitoring_helpers import load_monitoring_state


def _put_alarm(cw, name, metric, endpoint, threshold, comparison, dry_run):
    if dry_run:
        return
    cw.put_metric_alarm(
        AlarmName=name,
        AlarmDescription=f"Banking MLOps — {metric} on {endpoint}",
        MetricName=metric,
        Namespace="AWS/SageMaker",
        Statistic="Average",
        Dimensions=[{"Name": "EndpointName", "Value": endpoint}],
        Period=300,
        EvaluationPeriods=1,
        Threshold=threshold,
        ComparisonOperator=comparison,
        TreatMissingData="notBreaching",
    )


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
    acct = account_id(args.dry_run)

    alarms = [
        ("banking-ml-high-latency", "ModelLatency", 500, "GreaterThanThreshold"),
        ("banking-ml-error-rate", "ModelInvocation4XXErrors", 5, "GreaterThanThreshold"),
    ]

    cw = boto3.client("cloudwatch", region_name=REGION)
    for name, metric, threshold, comparison in alarms:
        _put_alarm(cw, name, metric, endpoint, threshold, comparison, args.dry_run)
        print(f"   ✅ {name}")

    cfg = {
        "alarms": [a[0] for a in alarms],
        "endpoint_name": endpoint,
        "dry_run": args.dry_run,
        "source": "cloudwatch",
        "account_id": acct,
    }
    with open(CONFIG_DIR / "alarms.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print("✅ Alarms configured" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
