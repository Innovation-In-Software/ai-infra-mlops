"""Load Lab 2 artifacts and prepare train/test splits."""
import json
import shutil
from datetime import datetime, timezone

import joblib
import pandas as pd
from lab_paths import CONFIG_DIR, DATA_DIR, LAB2, ensure_workspace
from sklearn.model_selection import train_test_split

TARGET = "high_risk"
EXCLUDE = {
    "transaction_id",
    "customer_id",
    "transaction_date",
    "first_name",
    "last_name",
    "email",
    "phone",
    "ssn",
    "address",
    "account_number",
    "routing_number",
    "medium_risk",
    "low_risk",
}


def _copy_lab2_artifacts():
    copies = [
        (LAB2 / "data" / "engineered_banking_data.csv", DATA_DIR / "engineered_banking_data.csv"),
        (LAB2 / "data" / "anonymized_customers.csv", DATA_DIR / "anonymized_customers.csv"),
        (LAB2 / "data" / "anonymized_transactions.csv", DATA_DIR / "anonymized_transactions.csv"),
        (LAB2 / "config" / "feature_metadata.json", CONFIG_DIR / "feature_metadata.json"),
        (LAB2 / "config" / "preprocessor.pkl", CONFIG_DIR / "preprocessor.pkl"),
    ]
    for src, dst in copies:
        if not src.exists():
            raise FileNotFoundError(f"Missing Lab 2 artifact: {src}. Complete Lab 2 first.")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"   ✅ Copied: {src.name}")


def main():
    ensure_workspace()
    print("📂 Loading Lab 2 Training Data")
    print("=" * 60)
    _copy_lab2_artifacts()

    df = pd.read_csv(DATA_DIR / "engineered_banking_data.csv")
    if TARGET not in df.columns:
        raise ValueError(f"Target column '{TARGET}' not found in engineered data")

    feature_cols = [
        c
        for c in df.columns
        if c not in EXCLUDE and c != TARGET and df[c].dtype in ("int64", "float64", "bool")
    ]
    X = df[feature_cols].astype(float)
    y = df[TARGET].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    X_train.to_csv(DATA_DIR / "X_train.csv", index=False)
    X_test.to_csv(DATA_DIR / "X_test.csv", index=False)
    y_train.to_csv(DATA_DIR / "y_train.csv", index=False)
    y_test.to_csv(DATA_DIR / "y_test.csv", index=False)

    with open(CONFIG_DIR / "feature_names.json", "w", encoding="utf-8") as f:
        json.dump(feature_cols, f, indent=2)

    meta = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "records": len(df),
        "features": len(feature_cols),
        "target": TARGET,
        "training_samples": len(X_train),
        "test_samples": len(X_test),
    }
    with open(CONFIG_DIR / "training_data_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"\n   Records: {len(df)}")
    print(f"   Features: {len(feature_cols)}")
    print(f"   Train: {len(X_train)} / Test: {len(X_test)}")
    print("✅ Training data prepared")


if __name__ == "__main__":
    main()
