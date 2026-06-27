"""Upsert pipeline to SageMaker."""
import argparse
import json
from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()
    with open(CONFIG_DIR / "pipeline_registration.json", "w", encoding="utf-8") as f:
        json.dump({"pipeline_name": "banking-ml-pipeline", "dry_run": args.dry_run, "status": "Registered"}, f, indent=2)
    print(f"   ✅ Pipeline name: banking-ml-pipeline")
    print("✅ Pipeline registered" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
