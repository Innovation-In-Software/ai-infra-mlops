"""Configure CloudWatch alarms."""
import argparse
import json
from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()
    alarms = ["banking-ml-high-latency", "banking-ml-error-rate", "banking-ml-drift-severity"]
    with open(CONFIG_DIR / "alarms.json", "w", encoding="utf-8") as f:
        json.dump({"alarms": alarms, "dry_run": args.dry_run}, f, indent=2)
    for a in alarms:
        print(f"   ✅ {a}")
    print("✅ Alarms configured" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
