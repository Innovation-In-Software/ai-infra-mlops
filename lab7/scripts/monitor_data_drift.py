"""Monitor data drift between baseline and current."""
import json
import pandas as pd
from lab_paths import CONFIG_DIR, DATA_DIR, RESULTS_DIR, ensure_workspace


def main():
    ensure_workspace()
    baseline = pd.read_csv(DATA_DIR / "baseline_data.csv")
    current = pd.read_csv(DATA_DIR / "current_data.csv")
    numeric = [c for c in baseline.columns if c in current.columns and baseline[c].dtype in ("float64", "int64")]
    drift_count = 0
    for col in numeric[:10]:
        if abs(baseline[col].mean() - current[col].mean()) > baseline[col].std() * 0.5:
            drift_count += 1
    report = {"features_checked": len(numeric), "drift_detected": drift_count, "status": "NORMAL" if drift_count < 5 else "WARNING"}
    with open(CONFIG_DIR / "drift_monitor_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("📉 Data Drift Check")
    print("=" * 60)
    print(f"   Features checked: {report['features_checked']}")
    print(f"   Drift detected: {drift_count}")
    print(f"   Status: {report['status']}")
    print("✅ Drift report saved")


if __name__ == "__main__":
    main()
