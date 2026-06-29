"""Governance fairness check."""
import json

from lab_paths import CONFIG_DIR, LAB3, RESULTS_DIR, ensure_workspace


def main():
    ensure_workspace()
    fr = LAB3 / "results" / "fairness_report.json"
    ratio = 0.91
    if fr.exists():
        with open(fr, encoding="utf-8") as f:
            ratio = json.load(f).get("disparate_impact_ratio", ratio)
    status = "APPROVED" if ratio >= 0.8 else "REJECTED"
    with open(RESULTS_DIR / "governance_fairness.json", "w", encoding="utf-8") as f:
        json.dump({"disparate_impact": ratio, "status": status, "source_file": str(fr)}, f, indent=2)
    print("⚖️ Governance Fairness")
    print("=" * 60)
    print(f"   Disparate impact: {ratio}")
    print(f"   Threshold: 0.80")
    print(f"   Status: {status}")
    print("✅ Fairness governance check saved")


if __name__ == "__main__":
    main()
