"""Shift traffic between blue and green SageMaker variants."""
import argparse
import json

from lab_paths import CONFIG_DIR, ensure_workspace
from sm_deploy import update_traffic_weights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--steps", default="90,50,0")
    args = parser.parse_args()
    ensure_workspace()

    prod_path = CONFIG_DIR / "production_deployment.json"
    if not prod_path.exists():
        print("   ❌ Missing production_deployment.json — run deploy_production.py first.")
        raise SystemExit(1)
    with open(prod_path, encoding="utf-8") as f:
        prod = json.load(f)
    endpoint_name = prod.get("endpoint")
    if not endpoint_name:
        print("   ❌ No production endpoint name in config")
        raise SystemExit(1)

    dry_run = args.dry_run or prod.get("dry_run", False)
    step_records = []
    for blue_pct in args.steps.split(","):
        blue = int(blue_pct.strip())
        green = 100 - blue
        label = f"Blue {blue}% / Green {green}%"
        if not dry_run:
            update_traffic_weights(endpoint_name, blue, green, dry_run=False)
        step_records.append(label)
        print(f"   Step {len(step_records)}: {label}")

    with open(CONFIG_DIR / "traffic_shift.json", "w", encoding="utf-8") as f:
        json.dump(
            {"steps": step_records, "endpoint": endpoint_name, "dry_run": dry_run, "source": "sagemaker"},
            f,
            indent=2,
        )
    print("✅ Traffic shift complete" + (" (dry-run)" if dry_run else ""))


if __name__ == "__main__":
    main()
