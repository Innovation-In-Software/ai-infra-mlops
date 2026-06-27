"""Run all Lab 2 steps in sequence."""
from data_drift_detection import main_drift_detection
from data_validation import validate_all_data
from download_banking_data import generate_banking_dataset
from feature_engineering import main_feature_engineering
from feature_store_setup import BankingFeatureStore
from generate_compliance_doc import generate_comprehensive_compliance_report
from pii_detection_anonymization import process_banking_data


def run_lab2():
    steps = [
        ("Banking dataset", generate_banking_dataset),
        ("PII protection", process_banking_data),
        ("Data validation", validate_all_data),
        ("Feature engineering", main_feature_engineering),
        ("Feature Store", lambda: BankingFeatureStore().setup_feature_store()),
        ("Drift detection", main_drift_detection),
        ("Compliance report", generate_comprehensive_compliance_report),
    ]

    print("Lab 2 — Banking Data Management & PII Protection")
    print("=" * 60)

    for name, fn in steps:
        print(f"\n▶ {name}")
        fn()

    print("\n" + "=" * 60)
    print("Lab 2 complete.")


if __name__ == "__main__":
    run_lab2()
