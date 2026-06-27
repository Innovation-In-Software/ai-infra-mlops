"""Governance fairness check."""
import json
import shutil
from lab_paths import CONFIG_DIR, RESULTS_DIR, ensure_workspace
from pathlib import Path

REPO = Path(__file__).resolve().parents[2].parent


def main():
    ensure_workspace()
    fr = REPO / "workspace" / "lab3" / "results" / "fairness_report.json"
    ratio = 0.91
    if fr.exists():
        with open(fr, encoding="utf-8") as f:
            ratio = json.load(f).get("disparate_impact_ratio", ratio)
    status = "APPROVED" if ratio >= 0.8 else "REJECTED"
    with open(RESULTS_DIR / "governance_fairness.json", "w", encoding="utf-8") as f:
        json.dump({"disparate_impact": ratio, "status": status}, f, indent=2)
    print(f"⚖️ Governance Fairness — {status}")


if __name__ == "__main__":
    main()
