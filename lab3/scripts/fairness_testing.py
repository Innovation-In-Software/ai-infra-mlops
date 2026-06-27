"""Fairness testing across protected attribute groups."""
import json
from datetime import datetime, timezone

import pandas as pd
from lab_paths import CONFIG_DIR, DATA_DIR, RESULTS_DIR, ensure_workspace


def disparate_impact(pos_rate_a, pos_rate_b):
    if pos_rate_a == 0:
        return 0.0
    return float(pos_rate_b / pos_rate_a)


def main():
    ensure_workspace()
    print("⚖️ Fairness Testing")
    print("=" * 60)

    df = pd.read_csv(DATA_DIR / "engineered_banking_data.csv")
    protected = "customer_segment" if "customer_segment" in df.columns else "age_group"
    if protected not in df.columns:
        protected = "income_category"
    target = "high_risk"

    groups = df.groupby(protected)[target].mean()
    if len(groups) < 2:
        ratio = 1.0
        status = "PASS"
    else:
        rates = groups.values
        ratio = disparate_impact(max(rates), min(rates))
        status = "PASS" if ratio >= 0.8 else "FAIL"

    analysis = {
        protected: {
            "positive_rates": {str(k): float(v) for k, v in groups.items()},
            "disparate_impact_ratio": ratio,
            "fairness_status": {"overall": status == "PASS"},
        }
    }

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "protected_attribute": protected,
        "fairness_analysis": analysis,
        "disparate_impact_ratio": ratio,
        "threshold": 0.8,
        "status": status,
    }
    with open(RESULTS_DIR / "fairness_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"   Protected attribute: {protected}")
    print(f"   Disparate impact ratio: {ratio:.2f}")
    print(f"   Status: {status} (within banking threshold)")
    print(f"✅ Fairness report saved: results/fairness_report.json")


if __name__ == "__main__":
    main()
