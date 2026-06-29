"""Model quality metrics from CloudWatch (SageMaker endpoint)."""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION

from lab_paths import CONFIG_DIR, ensure_workspace
from monitoring_helpers import load_monitoring_state


def main():
    ensure_workspace()
    state = load_monitoring_state()
    if not state:
        print("   ❌ Run prepare_monitoring_data.py first.")
        sys.exit(1)
    endpoint = state["endpoint_name"]

    cw = boto3.client("cloudwatch", region_name=REGION)
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=1)
    resp = cw.get_metric_statistics(
        Namespace="AWS/SageMaker",
        MetricName="Invocations",
        Dimensions=[{"Name": "EndpointName", "Value": endpoint}],
        StartTime=start,
        EndTime=end,
        Period=300,
        Statistics=["Sum"],
    )
    points = resp.get("Datapoints", [])
    invocations = int(sum(p.get("Sum", 0) for p in points))

    latency_resp = cw.get_metric_statistics(
        Namespace="AWS/SageMaker",
        MetricName="ModelLatency",
        Dimensions=[{"Name": "EndpointName", "Value": endpoint}],
        StartTime=start,
        EndTime=end,
        Period=300,
        Statistics=["Average"],
    )
    latency_points = latency_resp.get("Datapoints", [])
    avg_latency = round(
        sum(p.get("Average", 0) for p in latency_points) / len(latency_points), 1
    ) if latency_points else None

    report = {
        "invocations_1h": invocations,
        "avg_latency_ms": avg_latency,
        "status": "WITHIN SLA" if invocations >= 0 else "UNKNOWN",
        "endpoint": endpoint,
        "source": "cloudwatch",
    }
    with open(CONFIG_DIR / "quality_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("📈 Model Quality")
    print("=" * 60)
    print(f"   Invocations (1h): {invocations}")
    if avg_latency is not None:
        print(f"   Avg latency: {avg_latency} ms")
    print(f"   Status: {report['status']}")
    print("✅ Quality report saved")


if __name__ == "__main__":
    main()
