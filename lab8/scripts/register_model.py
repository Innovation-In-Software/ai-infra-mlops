"""Register model in Model Registry."""
import argparse
import json
from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()
    reg = {
        "model_package_group": "banking-risk-models",
        "approval_status": "PendingManualApproval",
        "dry_run": args.dry_run,
    }
    with open(CONFIG_DIR / "model_registry.json", "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2)
    print("📋 Model Registry")
    print("=" * 60)
    print(f"   ✅ Model package group: {reg['model_package_group']}")
    print("✅ Model registered" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
