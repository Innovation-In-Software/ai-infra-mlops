"""Rollback production endpoint to blue variant (100% blue)."""
import argparse
import json
from datetime import datetime, timezone

from lab_paths import CONFIG_DIR, ensure_workspace
from sm_deploy import update_traffic_weights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--endpoint-name", default=None)
    args = parser.parse_args()
    ensure_workspace()
    print("↩️ Rollback")
    print("=" * 60)

    prod_path = CONFIG_DIR / "production_deployment.json"
    endpoint_name = args.endpoint_name
    dry_run = args.dry_run
    if prod_path.exists():
        with open(prod_path, encoding="utf-8") as f:
            prod = json.load(f)
        endpoint_name = endpoint_name or prod.get("endpoint")
        dry_run = dry_run or prod.get("dry_run", False)

    if not endpoint_name:
        print("   ❌ Provide --endpoint-name or run deploy_production.py first.")
        raise SystemExit(1)

    if not dry_run:
        update_traffic_weights(endpoint_name, 100, 0, dry_run=False)
        print("   ✅ Restored blue variant to 100%")

    log = {
        "endpoint": endpoint_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "status": "ROLLED_BACK",
        "blue_weight": 100,
        "green_weight": 0,
        "source": "sagemaker",
    }
    with open(CONFIG_DIR / "rollback_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)
    print("   ✅ Rollback logged for audit")
    print("✅ Rollback complete" + (" (dry-run)" if dry_run else ""))


if __name__ == "__main__":
    main()
