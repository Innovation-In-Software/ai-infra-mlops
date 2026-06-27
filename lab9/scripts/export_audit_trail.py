"""Export audit trail."""
import json
from datetime import datetime, timezone
from lab_paths import LOGS_DIR, ensure_workspace


def main():
    ensure_workspace()
    export = {"timestamp": datetime.now(timezone.utc).isoformat(), "cloudtrail_events": "sampled", "pipelines_linked": True}
    with open(LOGS_DIR / "governance_audit_export.json", "w", encoding="utf-8") as f:
        json.dump(export, f, indent=2)
    print("📝 Audit export complete")


if __name__ == "__main__":
    main()
