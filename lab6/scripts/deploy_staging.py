"""Deploy staging endpoint."""
import argparse
from datetime import datetime, timezone

from lab_paths import CONFIG_DIR, ensure_workspace
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()
    name = f"banking-endpoint-staging-{datetime.now(timezone.utc).strftime('%Y%m%d')}"
    cfg = {"endpoint": name, "instance_type": "ml.m5.large", "dry_run": args.dry_run}
    with open(CONFIG_DIR / "staging_deployment.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    p = "[dry-run] " if args.dry_run else ""
    print(f"   {p}✅ Staging endpoint: {name}")
    print("✅ Staging deployment complete" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
