"""Log training metrics to SageMaker Experiments (classroom-safe)."""
import argparse
import json
from datetime import datetime, timezone

import boto3
from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Skip AWS API calls")
    args = parser.parse_args()
    ensure_workspace()

    print("📊 SageMaker Experiments")
    print("=" * 60)

    with open(CONFIG_DIR / "training_results.json", encoding="utf-8") as f:
        training = json.load(f)

    experiment_name = "banking-risk-experiments"
    trial_name = f"trial-{training.get('best_by_auc', 'model').lower()}-{datetime.now(timezone.utc).strftime('%Y%m%d')}"

    logged = {}
    for model_name, results in training.get("all_results", {}).items():
        logged[model_name] = results.get("metrics", {})

    if args.dry_run:
        print("   [dry-run] Skipping SageMaker Experiment API calls")
    else:
        try:
            sm = boto3.client("sagemaker", region_name="us-west-2")
            try:
                sm.create_experiment(ExperimentName=experiment_name)
            except sm.exceptions.ResourceInUse:
                pass
            sm.create_trial(TrialName=trial_name, ExperimentName=experiment_name)
            for model_name, metrics in logged.items():
                for metric, value in metrics.items():
                    sm.log_metric(
                        TrialName=trial_name,
                        MetricName=f"{model_name}_{metric}",
                        Value=float(value),
                    )
            print(f"   ✅ Experiment: {experiment_name}")
            print(f"   ✅ Trial: {trial_name}")
        except Exception as exc:
            print(f"   ⚠️ SageMaker Experiments skipped: {exc}")

    config = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "experiment_name": experiment_name,
        "trial_name": trial_name,
        "metrics_logged": logged,
        "dry_run": args.dry_run,
    }
    with open(CONFIG_DIR / "experiment_tracking.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print("   ✅ Metrics logged: auc, accuracy, f1")
    print("✅ Experiment tracking complete")


if __name__ == "__main__":
    main()
