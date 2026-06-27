"""Blue-green deployment plan."""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import write_json

from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()
    print("🔄 Blue-Green Plan")
    print("=" * 60)
    plan = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "blue_variant": {"name": "banking-model-blue", "weight": 100},
        "green_variant": {"name": "banking-model-green", "weight": 0},
        "traffic_shift_steps": ["90/10", "50/50", "0/100"],
        "dry_run": args.dry_run,
    }
    write_json(CONFIG_DIR / "blue_green_plan.json", plan)
    prefix = "[dry-run] " if args.dry_run else ""
    print(f"   {prefix}Blue variant: banking-model-blue (100%)")
    print(f"   {prefix}Green variant: banking-model-green (0%)")
    print("✅ Plan saved: config/blue_green_plan.json")


if __name__ == "__main__":
    main()
