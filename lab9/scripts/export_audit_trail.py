"""Export CloudTrail governance events."""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION

from lab_paths import LOGS_DIR, ensure_workspace

LOOKBACK_HOURS = 24
EVENT_NAMES = [
    "CreateEndpoint",
    "CreateModel",
    "CreatePipeline",
    "StartPipelineExecution",
    "CreateModelPackage",
]


def main():
    ensure_workspace()
    ct = boto3.client("cloudtrail", region_name=REGION)
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=LOOKBACK_HOURS)

    events = []
    try:
        for event_name in EVENT_NAMES:
            resp = ct.lookup_events(
                LookupAttributes=[{"AttributeKey": "EventName", "AttributeValue": event_name}],
                StartTime=start,
                EndTime=end,
                MaxResults=10,
            )
            for ev in resp.get("Events", []):
                events.append(
                    {
                        "event_name": ev.get("EventName"),
                        "event_time": ev.get("EventTime").isoformat() if ev.get("EventTime") else None,
                        "username": ev.get("Username"),
                        "source": ev.get("EventSource"),
                    }
                )
    except ClientError as exc:
        print(f"   ⚠️ CloudTrail lookup limited: {exc.response['Error']['Code']}")
        events = [{"note": "CloudTrail lookup requires cloudtrail:LookupEvents on this principal"}]

    export = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "region": REGION,
        "lookback_hours": LOOKBACK_HOURS,
        "event_count": len(events),
        "events": events,
        "pipelines_linked": any(e.get("event_name") == "StartPipelineExecution" for e in events),
        "source": "cloudtrail",
    }
    with open(LOGS_DIR / "governance_audit_export.json", "w", encoding="utf-8") as f:
        json.dump(export, f, indent=2, default=str)
    print("📝 Audit export complete")
    print(f"   Events sampled: {len(events)}")


if __name__ == "__main__":
    main()
