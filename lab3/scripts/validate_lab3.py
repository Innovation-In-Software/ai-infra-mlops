"""Validate Lab 3 prerequisites and outputs."""
import json
import sys

from lab_paths import CONFIG_DIR, DATA_DIR, MODELS_DIR, LAB2, RESULTS_DIR, ensure_workspace


def validate_lab3():
    ensure_workspace()
    print("Validate Lab 3")
    print("=" * 60)

    ok = True
    for name in (
        "engineered_banking_data.csv",
        "feature_metadata.json",
    ):
        path = LAB2 / ("data" if name.endswith(".csv") else "config") / name
        if path.exists():
            print(f"   ✅ Lab 2: {name}")
        else:
            print(f"   ❌ Missing Lab 2: {path}")
            ok = False

    checks = [
        (DATA_DIR / "X_train.csv", "data: X_train.csv"),
        (MODELS_DIR / "best_model.pkl", "models: best_model.pkl"),
        (RESULTS_DIR / "fairness_report.json", "results: fairness_report.json"),
        (RESULTS_DIR / "training_report_final.json", "results: training_report_final.json"),
        (CONFIG_DIR / "training_results.json", "config: training_results.json"),
    ]
    for path, label in checks:
        if path.exists():
            print(f"   ✅ {label}")
        else:
            print(f"   ⚠️ not yet created: {label.split(': ', 1)[1]}")

    (CONFIG_DIR / "lab3_validation.json").write_text(
        json.dumps({"lab": "3", "prerequisites_ok": ok}, indent=2),
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    if ok:
        print("Prerequisites OK — proceed to Lab 4")
    else:
        print("Complete Lab 2 first (lab2/STEPS.md).")
        sys.exit(1)


if __name__ == "__main__":
    validate_lab3()
