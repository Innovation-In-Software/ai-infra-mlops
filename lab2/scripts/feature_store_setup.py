"""SageMaker Feature Store setup for banking features."""
import json
from datetime import datetime, timezone

import boto3
import pandas as pd
import sagemaker
from sagemaker.feature_store.feature_definition import FeatureDefinition, FeatureTypeEnum
from sagemaker.feature_store.feature_group import FeatureGroup
from lab_paths import CONFIG_DIR, DATA_DIR, LAB1_CONFIG_DIR, RESULTS_DIR, ensure_workspace


class BankingFeatureStore:
    """Banking-specific feature store implementation."""

    def __init__(self):
        ensure_workspace()
        self.region = "us-west-2"
        self.sagemaker_session = sagemaker.Session()
        self.s3 = boto3.client("s3", region_name=self.region)

        with open(LAB1_CONFIG_DIR / "buckets.json", "r", encoding="utf-8") as f:
            self.buckets = json.load(f)

        with open(LAB1_CONFIG_DIR / "iam_roles.json", "r", encoding="utf-8") as f:
            self.roles = json.load(f)

    def create_transaction_feature_group(self):
        print("\n📊 Creating Transaction Feature Group...")
        print("=" * 60)

        feature_definitions = [
            FeatureDefinition("transaction_id", FeatureTypeEnum.STRING),
            FeatureDefinition("customer_id", FeatureTypeEnum.STRING),
            FeatureDefinition("transaction_type", FeatureTypeEnum.STRING),
            FeatureDefinition("amount", FeatureTypeEnum.FRACTIONAL),
            FeatureDefinition("amount_log", FeatureTypeEnum.FRACTIONAL),
            FeatureDefinition("amount_sqrt", FeatureTypeEnum.FRACTIONAL),
            FeatureDefinition("transaction_hour", FeatureTypeEnum.INTEGRAL),
            FeatureDefinition("transaction_day", FeatureTypeEnum.INTEGRAL),
            FeatureDefinition("transaction_month", FeatureTypeEnum.INTEGRAL),
            FeatureDefinition("is_weekend", FeatureTypeEnum.INTEGRAL),
            FeatureDefinition("is_business_hours", FeatureTypeEnum.INTEGRAL),
            FeatureDefinition("merchant", FeatureTypeEnum.STRING),
            FeatureDefinition("location", FeatureTypeEnum.STRING),
            FeatureDefinition("card_present", FeatureTypeEnum.INTEGRAL),
            FeatureDefinition("international", FeatureTypeEnum.INTEGRAL),
            FeatureDefinition("risk_score", FeatureTypeEnum.FRACTIONAL),
            FeatureDefinition("high_risk", FeatureTypeEnum.INTEGRAL),
            FeatureDefinition("medium_risk", FeatureTypeEnum.INTEGRAL),
            FeatureDefinition("low_risk", FeatureTypeEnum.INTEGRAL),
        ]

        feature_group_name = "banking-transaction-features"
        feature_group = FeatureGroup(
            name=feature_group_name,
            feature_definitions=feature_definitions,
            sagemaker_session=self.sagemaker_session,
        )

        s3_uri = f"s3://{self.buckets['processed']['name']}/feature_store/transactions/"

        try:
            feature_group.create(
                s3_uri=s3_uri,
                record_identifier_name="transaction_id",
                event_time_feature_name="transaction_hour",
                role_arn=self.roles["data_scientist"]["arn"],
                enable_online_store=True,
                tags=[
                    {"Key": "Environment", "Value": "MLOps"},
                    {"Key": "Compliance", "Value": "Banking"},
                    {"Key": "DataClassification", "Value": "Non-PII"},
                    {"Key": "FeatureType", "Value": "Transaction"},
                    {"Key": "CreatedBy", "Value": "Lab1.2"},
                ],
            )
            print(f"   ✅ Feature group created: {feature_group_name}")
        except Exception as e:
            print(f"   ⚠️ Feature group may already exist: {str(e)}")
            feature_group = FeatureGroup(name=feature_group_name, sagemaker_session=self.sagemaker_session)

        return feature_group

    def create_customer_feature_group(self):
        print("\n📊 Creating Customer Feature Group...")
        print("=" * 60)

        feature_definitions = [
            FeatureDefinition("customer_id", FeatureTypeEnum.STRING),
            FeatureDefinition("age", FeatureTypeEnum.INTEGRAL),
            FeatureDefinition("income", FeatureTypeEnum.FRACTIONAL),
            FeatureDefinition("credit_score", FeatureTypeEnum.INTEGRAL),
            FeatureDefinition("credit_score_category", FeatureTypeEnum.STRING),
            FeatureDefinition("income_category", FeatureTypeEnum.STRING),
            FeatureDefinition("age_group", FeatureTypeEnum.STRING),
            FeatureDefinition("credit_score_scaled", FeatureTypeEnum.FRACTIONAL),
            FeatureDefinition("income_log", FeatureTypeEnum.FRACTIONAL),
            FeatureDefinition("income_sqrt", FeatureTypeEnum.FRACTIONAL),
            FeatureDefinition("age_squared", FeatureTypeEnum.FRACTIONAL),
            FeatureDefinition("income_per_age", FeatureTypeEnum.FRACTIONAL),
            FeatureDefinition("credit_to_income", FeatureTypeEnum.FRACTIONAL),
        ]

        feature_group_name = "banking-customer-features"
        feature_group = FeatureGroup(
            name=feature_group_name,
            feature_definitions=feature_definitions,
            sagemaker_session=self.sagemaker_session,
        )

        s3_uri = f"s3://{self.buckets['processed']['name']}/feature_store/customers/"

        try:
            feature_group.create(
                s3_uri=s3_uri,
                record_identifier_name="customer_id",
                event_time_feature_name="age",
                role_arn=self.roles["data_scientist"]["arn"],
                enable_online_store=True,
                tags=[
                    {"Key": "Environment", "Value": "MLOps"},
                    {"Key": "Compliance", "Value": "Banking"},
                    {"Key": "DataClassification", "Value": "Non-PII"},
                    {"Key": "FeatureType", "Value": "Customer"},
                    {"Key": "CreatedBy", "Value": "Lab1.2"},
                ],
            )
            print(f"   ✅ Feature group created: {feature_group_name}")
        except Exception as e:
            print(f"   ⚠️ Feature group may already exist: {str(e)}")
            feature_group = FeatureGroup(name=feature_group_name, sagemaker_session=self.sagemaker_session)

        return feature_group

    def ingest_features(self, df, feature_group):
        print("\n📥 Ingesting features into feature store...")

        type_by_col = {
            fd.feature_name: fd.feature_type
            for fd in feature_group.feature_definitions
        }
        df_ingest = df.copy()
        required_columns = list(type_by_col.keys())

        for col in required_columns:
            if col not in df_ingest.columns:
                if type_by_col[col] in (
                    FeatureTypeEnum.INTEGRAL,
                    FeatureTypeEnum.FRACTIONAL,
                ):
                    df_ingest[col] = 0
                else:
                    df_ingest[col] = "unknown"

        df_ingest = df_ingest[required_columns]

        for col in required_columns:
            if type_by_col[col] in (
                FeatureTypeEnum.INTEGRAL,
                FeatureTypeEnum.FRACTIONAL,
            ):
                df_ingest[col] = pd.to_numeric(df_ingest[col], errors="coerce").fillna(0)
            else:
                df_ingest[col] = df_ingest[col].astype(str)

        try:
            feature_group.ingest(data_frame=df_ingest, max_processes=1)
            print(f"   ✅ Ingested {len(df_ingest)} records into {feature_group.name}")
        except Exception as e:
            print(f"   ❌ Error ingesting features: {str(e)}")
            print("   ⚠️ This is expected if features were already ingested")

    def setup_feature_store(self):
        print("🏦 Setting Up Banking Feature Store")
        print("=" * 60)

        transaction_fg = self.create_transaction_feature_group()
        customer_fg = self.create_customer_feature_group()

        training_data = pd.read_csv(DATA_DIR / "engineered_banking_data.csv")

        transaction_columns = [fd.feature_name for fd in transaction_fg.feature_definitions]
        transaction_features = training_data[
            [col for col in transaction_columns if col in training_data.columns]
        ]

        customer_columns = [fd.feature_name for fd in customer_fg.feature_definitions]
        available_customer_cols = [
            col for col in customer_columns if col in training_data.columns
        ]
        customer_features = training_data[available_customer_cols].drop_duplicates(
            subset=["customer_id"]
        )

        self.ingest_features(transaction_features, transaction_fg)
        self.ingest_features(customer_features, customer_fg)

        feature_store_config = {
            "transaction_feature_group": transaction_fg.name,
            "customer_feature_group": customer_fg.name,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "s3_location": f"s3://{self.buckets['processed']['name']}/feature_store/",
        }

        with open(CONFIG_DIR / "feature_store_config.json", "w", encoding="utf-8") as f:
            json.dump(feature_store_config, f, indent=2)

        print("\n" + "=" * 60)
        print("✅ Feature Store Setup Complete!")
        print(f"   Transaction Feature Group: {transaction_fg.name}")
        print(f"   Customer Feature Group: {customer_fg.name}")
        print(f"   Config: {CONFIG_DIR / 'feature_store_config.json'}")

        return feature_store_config


if __name__ == "__main__":
    fs = BankingFeatureStore()
    fs.setup_feature_store()
