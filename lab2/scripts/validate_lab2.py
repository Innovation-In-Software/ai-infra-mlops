"""Validate Lab 2 prerequisites and outputs."""
import json
import sys
from pathlib import Path

from lab_paths import CONFIG_DIR, DATA_DIR, LAB1_CONFIG_DIR, ensure_workspace


def validate_lab2():
    ensure_workspace()
    print("Validate Lab 2")
    print("=" * 60)

    ok = True

    for name in ("buckets.json", "iam_roles.json"):
        path = LAB1_CONFIG_DIR / name
        if path.exists():
            print(f"   ✅ Lab 1 config: {name}")
        else:
            print(f"   ❌ Missing Lab 1 config: {path}")
            ok = False

    expected_data = (
        "customers.csv",
        "transactions.csv",
        "anonymized_customers.csv",
        "anonymized_transactions.csv",
        "engineered_banking_data.csv",
        "compliance_report_final.json",
    )
    for name in expected_data:
        path = DATA_DIR / name
        if path.exists():
            print(f"   ✅ data: {name}")
        else:
            print(f"   ⚠️ not yet created: {name}")

    for name in (
        "dataset_metadata.json",
        "pii_report.json",
        "pii_compliance_report.json",
        "feature_metadata.json",
        "feature_store_config.json",
        "drift_report.json",
    ):
        path = CONFIG_DIR / name
        if path.exists():
            print(f"   ✅ config: {name}")
        else:
            print(f"   ⚠️ not yet created: {name}")

    for path in sorted(CONFIG_DIR.glob("data_quality_report_*.json")):
        print(f"   ✅ config: {path.name}")

    report = CONFIG_DIR / "lab2_validation.json"
    report.write_text(
        json.dumps({"lab": "2", "prerequisites_ok": ok}, indent=2),
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    if ok:
        print("Prerequisites OK — run lab2 scripts in STEPS.md order.")
    else:
        print("Complete Lab 1 first (lab1/STEPS.md).")
        sys.exit(1)


if __name__ == "__main__":
    validate_lab2()
