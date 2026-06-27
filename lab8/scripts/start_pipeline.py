"""Start pipeline execution."""
import argparse
import json
from datetime import datetime, timezone
from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()
    execution = {
        "execution_arn": f"arn:aws:sagemaker:us-west-2:000000000000:pipeline/banking-ml-pipeline/execution/{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "status": "Executing" if args.dry_run else "Submitted",
        "dry_run": args.dry_run,
    }
    with open(CONFIG_DIR / "pipeline_execution.json", "w", encoding="utf-8") as f:
        json.dump(execution, f, indent=2)
    print("▶️ Pipeline Execution")
    print("=" * 60)
    print(f"   Execution ARN: {execution['execution_arn']}")
    print("✅ Pipeline started" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
