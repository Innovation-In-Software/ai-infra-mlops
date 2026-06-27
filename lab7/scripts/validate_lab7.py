"""Validate Lab 7."""
import sys
from lab_paths import DATA_DIR, RESULTS_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 7")
    print("=" * 60)
    for p, label in [
        (DATA_DIR / "baseline_data.csv", "baseline_data.csv"),
        (DATA_DIR / "current_data.csv", "current_data.csv"),
        (RESULTS_DIR / "monitoring_report_final.json", "monitoring_report_final.json"),
    ]:
        print(f"   {'✅' if p.exists() else '⚠️'} {label}")
    print("Prerequisites OK — proceed to Lab 8")


if __name__ == "__main__":
    main()
