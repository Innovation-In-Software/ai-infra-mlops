"""Select best model using performance and fairness scores."""
import json
import shutil
from datetime import datetime, timezone

import joblib
from lab_paths import CONFIG_DIR, MODELS_DIR, RESULTS_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("📋 Banking Model Selection")
    print("=" * 60)

    with open(CONFIG_DIR / "training_results.json", encoding="utf-8") as f:
        training = json.load(f)
    with open(RESULTS_DIR / "fairness_report.json", encoding="utf-8") as f:
        fairness = json.load(f)

    fairness_ok = fairness.get("status") == "PASS"
    fairness_score = 1.0 if fairness_ok else 0.5

    model_scores = {}
    for name, results in training["all_results"].items():
        auc = results["metrics"]["auc"]
        performance_score = auc
        combined = 0.6 * performance_score + 0.4 * fairness_score
        model_scores[name] = {
            "performance_score": performance_score,
            "fairness_score": fairness_score,
            "combined_score": combined,
            "auc": auc,
            "fairness_passing": fairness_ok,
        }
        print(f"   {name}: combined={combined:.3f} AUC={auc:.2f}")

    best_name = max(model_scores.items(), key=lambda x: x[1]["combined_score"])[0]
    src = MODELS_DIR / f"{best_name.lower()}_model.pkl"
    shutil.copy2(src, MODELS_DIR / "best_model.pkl")

    selection = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "best_model": best_name,
        "best_score": model_scores[best_name],
        "all_scores": model_scores,
    }
    with open(CONFIG_DIR / "selection_results.json", "w", encoding="utf-8") as f:
        json.dump(selection, f, indent=2)

    training_report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "best_model": best_name,
        "metrics": training["all_results"][best_name]["metrics"],
        "fairness_status": fairness.get("status"),
    }
    with open(RESULTS_DIR / "training_report_final.json", "w", encoding="utf-8") as f:
        json.dump(training_report, f, indent=2)

    print(f"\n✅ Best model: {best_name} (AUC {model_scores[best_name]['auc']:.2f}, fairness {fairness.get('status')})")
    print(f"   Saved: models/best_model.pkl")


if __name__ == "__main__":
    main()
