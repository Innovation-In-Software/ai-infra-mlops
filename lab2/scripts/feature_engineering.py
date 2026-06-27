"""Banking feature engineering pipeline."""
import json
from datetime import datetime, timezone

import boto3
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from lab_paths import CONFIG_DIR, DATA_DIR, LAB1_CONFIG_DIR, RESULTS_DIR, ensure_workspace


class BankingFeatureEngineer:
    """Banking-specific feature engineering pipeline."""

    def __init__(self):
        self.feature_metadata = {
            "numeric_features": [],
            "categorical_features": [],
            "datetime_features": [],
            "target_feature": "total_amount",
        }

    def engineer_transaction_features(self, df):
        df = df.copy()

        if "transaction_date" in df.columns:
            df["transaction_date"] = pd.to_datetime(df["transaction_date"])
            df["transaction_hour"] = df["transaction_date"].dt.hour
            df["transaction_day"] = df["transaction_date"].dt.dayofweek
            df["transaction_month"] = df["transaction_date"].dt.month
            df["transaction_quarter"] = df["transaction_date"].dt.quarter
            df["is_weekend"] = df["transaction_day"].isin([5, 6]).astype(int)
            df["is_business_hours"] = df["transaction_hour"].between(9, 17).astype(int)

        if "amount" in df.columns:
            df["amount_log"] = np.log1p(df["amount"])
            df["amount_sqrt"] = np.sqrt(df["amount"])
            df["amount_squared"] = df["amount"] ** 2

        if "customer_id" in df.columns:
            transaction_count = df.groupby("customer_id").size().reset_index(name="transaction_count")
            df = df.merge(transaction_count, on="customer_id", how="left")

            avg_amount = df.groupby("customer_id")["amount"].mean().reset_index(name="avg_transaction_amount")
            df = df.merge(avg_amount, on="customer_id", how="left")

            max_amount = df.groupby("customer_id")["amount"].max().reset_index(name="max_transaction_amount")
            df = df.merge(max_amount, on="customer_id", how="left")

            std_amount = df.groupby("customer_id")["amount"].std().reset_index(name="std_transaction_amount")
            df = df.merge(std_amount, on="customer_id", how="left")
            df["std_transaction_amount"] = df["std_transaction_amount"].fillna(0)

        if "risk_score" in df.columns:
            df["risk_category"] = pd.cut(
                df["risk_score"],
                bins=[0, 25, 50, 75, 100],
                labels=["Low", "Medium", "High", "Critical"],
            )

        if "merchant" in df.columns:
            merchant_count = df.groupby("merchant").size().reset_index(name="merchant_transaction_count")
            df = df.merge(merchant_count, on="merchant", how="left")
            merchant_risk = df.groupby("merchant")["risk_score"].mean().reset_index(name="merchant_avg_risk")
            df = df.merge(merchant_risk, on="merchant", how="left")

        if "location" in df.columns:
            df["location_online"] = (df["location"] == "Online").astype(int)
            df["location_atm"] = (df["location"] == "ATM").astype(int)

        if "card_present" in df.columns:
            df["card_present"] = df["card_present"].astype(int)

        if "international" in df.columns:
            df["international"] = df["international"].astype(int)

        if "risk_score" in df.columns:
            df["high_risk"] = (df["risk_score"] > 75).astype(int)
            df["medium_risk"] = ((df["risk_score"] > 50) & (df["risk_score"] <= 75)).astype(int)
            df["low_risk"] = (df["risk_score"] <= 50).astype(int)

        return df

    def engineer_customer_features(self, df):
        df = df.copy()

        if "credit_score" in df.columns:
            df["credit_score_category"] = pd.cut(
                df["credit_score"],
                bins=[300, 580, 669, 739, 799, 850],
                labels=["Very Poor", "Poor", "Fair", "Good", "Excellent"],
            )
            df["credit_score_scaled"] = (df["credit_score"] - 300) / (850 - 300)

        if "income" in df.columns:
            df["income_log"] = np.log1p(df["income"])
            df["income_sqrt"] = np.sqrt(df["income"])
            df["income_category"] = pd.cut(
                df["income"],
                bins=[0, 50000, 100000, 150000, 200000, float("inf")],
                labels=["Low", "Lower-Middle", "Middle", "Upper-Middle", "High"],
            )

        if "age" in df.columns:
            df["age_group"] = pd.cut(
                df["age"],
                bins=[18, 25, 35, 45, 55, 65, 85],
                labels=["Young Adult", "Adult", "Early Career", "Mid Career", "Late Career", "Retirement"],
            )
            df["age_squared"] = df["age"] ** 2

        if "income" in df.columns and "age" in df.columns:
            df["income_per_age"] = df["income"] / (df["age"] + 1)

        if "credit_score" in df.columns and "income" in df.columns:
            df["credit_to_income"] = df["credit_score"] / (df["income"] / 1000 + 1)

        return df

    def create_feature_pipeline(self, df, target_column=None):
        self.feature_metadata["numeric_features"] = df.select_dtypes(
            include=["int64", "float64"]
        ).columns.tolist()

        self.feature_metadata["categorical_features"] = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        if target_column and target_column in self.feature_metadata["numeric_features"]:
            self.feature_metadata["numeric_features"].remove(target_column)
            self.feature_metadata["target_feature"] = target_column

        numeric_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )

        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
                ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
            ]
        )

        return ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, self.feature_metadata["numeric_features"]),
                ("cat", categorical_transformer, self.feature_metadata["categorical_features"]),
            ]
        )

    def save_feature_metadata(self, df):
        feature_metadata = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "total_features": len(df.columns),
            "feature_names": df.columns.tolist(),
            "feature_types": df.dtypes.astype(str).to_dict(),
            "numeric_features": self.feature_metadata["numeric_features"],
            "categorical_features": self.feature_metadata["categorical_features"],
            "target_feature": self.feature_metadata.get("target_feature"),
            "data_classification": "NON_PII",
            "lineage": {
                "source_tables": ["customers", "transactions"],
                "processing_script": "feature_engineering.py",
                "version": "1.0",
            },
        }

        with open(CONFIG_DIR / "feature_metadata.json", "w", encoding="utf-8") as f:
            json.dump(feature_metadata, f, indent=2)

        account_id = boto3.client("sts").get_caller_identity()["Account"]
        s3 = boto3.client("s3", region_name="us-west-2")
        s3_key = f"feature_metadata/feature_metadata_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
        s3.put_object(
            Bucket=f"bank-mlops-{account_id}-processed",
            Key=s3_key,
            Body=json.dumps(feature_metadata, indent=2),
        )

        return feature_metadata


def main_feature_engineering():
    ensure_workspace()
    print("🔧 Engineering Banking Features")
    print("=" * 60)

    print("\n📂 Loading data...")
    customers_df = pd.read_csv(DATA_DIR / "anonymized_customers.csv")
    transactions_df = pd.read_csv(DATA_DIR / "anonymized_transactions.csv")
    print(f"   Customers: {len(customers_df)} records")
    print(f"   Transactions: {len(transactions_df)} records")

    engineer = BankingFeatureEngineer()

    print("\n📊 Engineering transaction features...")
    transactions_engineered = engineer.engineer_transaction_features(transactions_df)
    print(f"   Transaction features: {len(transactions_engineered.columns)}")

    print("\n📊 Engineering customer features...")
    customers_engineered = engineer.engineer_customer_features(customers_df)
    print(f"   Customer features: {len(customers_engineered.columns)}")

    print("\n🔗 Merging datasets for ML...")
    training_data = transactions_engineered.merge(
        customers_engineered, on="customer_id", how="left", suffixes=("", "_customer")
    )
    duplicate_cols = [col for col in training_data.columns if "_customer" in col]
    training_data = training_data.drop(columns=duplicate_cols)
    print(f"   Training dataset: {len(training_data)} records, {len(training_data.columns)} features")

    print("\n💾 Saving engineered data...")
    training_data.to_csv(DATA_DIR / "engineered_banking_data.csv", index=False)
    print(f"   ✅ {DATA_DIR / 'engineered_banking_data.csv'}")

    preprocessor = None
    print("\n🔧 Creating feature pipeline...")
    if "amount" in training_data.columns:
        drop_cols = [c for c in ["amount", "transaction_id", "customer_id", "transaction_date"] if c in training_data.columns]
        X = training_data.drop(drop_cols, axis=1)
        preprocessor = engineer.create_feature_pipeline(X)
        joblib.dump(preprocessor, CONFIG_DIR / "preprocessor.pkl")
        print(f"   ✅ Pipeline saved: {CONFIG_DIR / 'preprocessor.pkl'}")

    print("\n📋 Saving feature metadata...")
    feature_metadata = engineer.save_feature_metadata(training_data)
    print(f"   ✅ Metadata saved: {feature_metadata['total_features']} features")

    print("\n" + "=" * 60)
    print("✅ Feature Engineering Complete!")
    print(f"   Training Data: {DATA_DIR / 'engineered_banking_data.csv'}")
    print(f"   Feature Pipeline: {CONFIG_DIR / 'preprocessor.pkl'}")
    print(f"   Feature Metadata: {CONFIG_DIR / 'feature_metadata.json'}")

    return training_data, preprocessor


if __name__ == "__main__":
    main_feature_engineering()
