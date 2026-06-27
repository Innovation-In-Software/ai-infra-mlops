"""Simulate incident response."""
import json
from datetime import datetime, timezone
from lab_paths import LOGS_DIR, ensure_workspace


def main():
    ensure_workspace()
    log = {"incident": "latency_spike", "timestamp": datetime.now(timezone.utc).isoformat(), "resolved": True}
    with open(LOGS_DIR / "incident_drill.json", "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)
    print("⚠️ Simulated incident: latency spike")
    print("   ✅ Alarm triggered")
    print("   ✅ Runbook executed")
    print("✅ Incident drill complete")


if __name__ == "__main__":
    main()
