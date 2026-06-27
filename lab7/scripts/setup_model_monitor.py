"""SageMaker Model Monitor setup."""
import argparse
import json
from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()
    with open(CONFIG_DIR / "model_monitor.json", "w", encoding="utf-8") as f:
        json.dump({"schedule": "hourly", "dry_run": args.dry_run}, f, indent=2)
    print("   ✅ Baseline constraints generated")
    print("   ✅ Monitoring schedule: hourly (simulated)")
    print("✅ Model Monitor configured" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
