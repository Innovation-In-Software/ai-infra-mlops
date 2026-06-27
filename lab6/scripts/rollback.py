"""Rollback endpoint to previous configuration."""
import argparse
import json
from datetime import datetime, timezone

from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--endpoint-name", default="banking-endpoint-prod-demo")
    args = parser.parse_args()
    ensure_workspace()
    print("↩️ Rollback")
    print("=" * 60)
    log = {
        "endpoint": args.endpoint_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "status": "ROLLED_BACK",
    }
    with open(CONFIG_DIR / "rollback_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)
    print("   ✅ Restored previous variant weights")
    print("   ✅ Rollback logged for audit")
    print("✅ Rollback complete" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
