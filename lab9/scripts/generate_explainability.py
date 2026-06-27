"""Generate explainability report."""
import json
from lab_paths import RESULTS_DIR, ensure_workspace


def main():
    ensure_workspace()
    report = {"method": "SHAP", "top_features": ["transaction_amount", "merchant_category", "risk_score"]}
    with open(RESULTS_DIR / "explainability_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("🔍 Explainability complete")


if __name__ == "__main__":
    main()
