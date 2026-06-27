"""PII detection and anonymization for banking datasets."""
import json
import re
from datetime import datetime, timezone

import boto3
import pandas as pd
from lab_paths import CONFIG_DIR, DATA_DIR, LAB1_CONFIG_DIR, RESULTS_DIR, ensure_workspace


class BankingPIIHandler:
    """Banking-specific PII detection and anonymization."""

    def __init__(self):
        self.region = "us-west-2"
        self.account_id = boto3.client("sts").get_caller_identity()["Account"]
        self.comprehend = boto3.client("comprehend", region_name=self.region)
        self.s3 = boto3.client("s3", region_name=self.region)

        self.pii_patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "account_number": r"\b\d{8,12}\b",
            "routing_number": r"\b\d{9}\b",
            "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
            "address": r"\b\d{1,5}\s\w+\s(?:St|Ave|Blvd|Rd|Ln|Dr|Way|Pl)\b",
            "zip_code": r"\b\d{5}(?:-\d{4})?\b",
        }

    def detect_pii_with_comprehend(self, text):
        try:
            if not text or len(str(text)) < 2:
                return []
            response = self.comprehend.detect_pii_entities(
                Text=str(text)[:5000], LanguageCode="en"
            )
            return response["Entities"]
        except Exception as e:
            print(f"   ⚠️ Comprehend error: {str(e)}")
            return []

    def detect_pii_patterns(self, text):
        if not text or len(str(text)) < 2:
            return []

        detected = []
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, str(text))
            for match in matches:
                detected.append({"Type": pii_type.upper(), "Text": match, "Score": 0.9})
        return detected

    def anonymize_text(self, text, pii_entities):
        if not text or len(str(text)) < 2:
            return text

        text = str(text)
        entities = sorted(
            pii_entities, key=lambda x: len(str(x.get("Text", ""))), reverse=True
        )

        for entity in entities:
            if "Text" in entity:
                pii_type = entity.get("Type", "PII")
                replacement = f"[REDACTED_{pii_type}]"
                text = text.replace(str(entity["Text"]), replacement)

        return text

    def detect_and_anonymize_dataframe(self, df, columns_to_scan=None):
        print("\n🔍 Detecting PII in Banking Dataset")
        print("=" * 60)

        if columns_to_scan is None:
            string_columns = df.select_dtypes(include=["object"]).columns
            columns_to_scan = [
                col
                for col in string_columns
                if col.lower()
                in [
                    "first_name", "last_name", "email", "phone", "ssn",
                    "account_number", "routing_number", "address", "zip_code", "name",
                ]
            ]

        print(f"📋 Scanning columns: {', '.join(columns_to_scan)}")

        pii_report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "columns_scanned": columns_to_scan,
            "pii_found": {},
            "anonymized_count": 0,
        }

        anonymized_df = df.copy()

        for col in columns_to_scan:
            print(f"\n🔎 Scanning column: {col}")
            pii_in_column = []

            for idx, value in df[col].items():
                if pd.isna(value) or value == "":
                    continue

                comprehend_entities = self.detect_pii_with_comprehend(str(value))

                if comprehend_entities:
                    anonymized_val = self.anonymize_text(str(value), comprehend_entities)
                    if anonymized_val != str(value):
                        anonymized_df.at[idx, col] = anonymized_val
                        pii_in_column.append(
                            {
                                "row": idx,
                                "original": str(value)[:50],
                                "anonymized": anonymized_val[:50],
                                "entities": [
                                    {"Type": e["Type"], "Score": e.get("Score", 1)}
                                    for e in comprehend_entities
                                ],
                            }
                        )
                        pii_report["anonymized_count"] += 1
                else:
                    pattern_entities = self.detect_pii_patterns(str(value))
                    if pattern_entities:
                        anonymized_val = self.anonymize_text(str(value), pattern_entities)
                        if anonymized_val != str(value):
                            anonymized_df.at[idx, col] = anonymized_val
                            pii_in_column.append(
                                {
                                    "row": idx,
                                    "original": str(value)[:50],
                                    "anonymized": anonymized_val[:50],
                                    "entities": [
                                        {"Type": e["Type"], "Score": e["Score"]}
                                        for e in pattern_entities
                                    ],
                                }
                            )
                            pii_report["anonymized_count"] += 1

            if pii_in_column:
                pii_report["pii_found"][col] = {
                    "count": len(pii_in_column),
                    "examples": pii_in_column[:5],
                }
                print(f"   ✅ Found and anonymized {len(pii_in_column)} PII instances in {col}")
            else:
                print(f"   ✅ No PII detected in {col}")

        with open(CONFIG_DIR / "pii_report.json", "w", encoding="utf-8") as f:
            json.dump(pii_report, f, indent=2)

        print("\n" + "=" * 60)
        print("✅ PII Detection and Anonymization Complete!")
        print(f"   Total PII Instances Anonymized: {pii_report['anonymized_count']}")

        return anonymized_df, pii_report

    def generate_pii_compliance_report(self, pii_report):
        compliance_report = {
            "institution": "Banking Institution",
            "report_type": "PII Compliance Report",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data_classification": "CONFIDENTIAL",
            "pii_handling": {
                "detection_method": "AWS Comprehend + Pattern Matching",
                "anonymized_instances": pii_report.get("anonymized_count", 0),
                "columns_affected": list(pii_report.get("pii_found", {}).keys()),
            },
            "compliance_standards_met": [
                "GDPR - Article 5 (Data Minimization)",
                "GDPR - Article 25 (Data Protection by Design)",
                "NYDFS - 23 NYCRR 500",
                "GLBA - Privacy and Data Protection",
                "PCI-DSS - Requirement 3 (Protect Stored Cardholder Data)",
            ],
            "data_retention_policy": "7 Years (2555 days)",
            "audit_trail": {
                "performed_by": "MLOps-Banking-Lab",
                "review_date": datetime.now(timezone.utc).isoformat(),
                "approval_status": "PENDING_COMPLIANCE_REVIEW",
            },
            "recommendations": [
                "Implement automated PII scanning on all new data ingestion",
                "Establish regular (quarterly) PII audit reviews",
                "Consider implementing data masking for non-production environments",
            ],
        }

        with open(CONFIG_DIR / "pii_compliance_report.json", "w", encoding="utf-8") as f:
            json.dump(compliance_report, f, indent=2)

        s3_key = f"compliance/pii_report_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
        self.s3.put_object(
            Bucket=f"bank-mlops-{self.account_id}-governance",
            Key=s3_key,
            Body=json.dumps(compliance_report, indent=2),
        )
        print(f"   📋 Compliance report uploaded to S3: {s3_key}")

        return compliance_report


def process_banking_data():
    ensure_workspace()
    print("🏦 Processing Banking Data with PII Protection")
    print("=" * 60)

    print("\n📂 Loading banking datasets...")
    customers_df = pd.read_csv(DATA_DIR / "customers.csv")
    transactions_df = pd.read_csv(DATA_DIR / "transactions.csv")
    print(f"   ✅ Loaded {len(customers_df)} customer records")
    print(f"   ✅ Loaded {len(transactions_df)} transaction records")

    pii_handler = BankingPIIHandler()

    print("\n📋 Processing Customer Data...")
    anonymized_customers, customer_pii_report = pii_handler.detect_and_anonymize_dataframe(
        customers_df,
        columns_to_scan=[
            "first_name", "last_name", "email", "phone", "ssn",
            "account_number", "routing_number", "address", "zip_code",
        ],
    )

    print("\n📋 Processing Transaction Data...")
    anonymized_transactions, transaction_pii_report = pii_handler.detect_and_anonymize_dataframe(
        transactions_df,
        columns_to_scan=["first_name", "last_name", "email", "phone", "account_number", "merchant"],
    )

    print("\n💾 Saving Anonymized Data...")
    anonymized_customers.to_csv(DATA_DIR / "anonymized_customers.csv", index=False)
    anonymized_transactions.to_csv(DATA_DIR / "anonymized_transactions.csv", index=False)
    print(f"   ✅ {DATA_DIR / 'anonymized_customers.csv'}")
    print(f"   ✅ {DATA_DIR / 'anonymized_transactions.csv'}")

    print("\n📋 Generating Compliance Report...")
    combined_pii_report = {
        "anonymized_count": customer_pii_report["anonymized_count"]
        + transaction_pii_report["anonymized_count"],
        "pii_found": {
            **customer_pii_report.get("pii_found", {}),
            **transaction_pii_report.get("pii_found", {}),
        },
        "customer_pii": customer_pii_report,
        "transaction_pii": transaction_pii_report,
    }

    compliance_report = pii_handler.generate_pii_compliance_report(combined_pii_report)

    print("\n" + "=" * 60)
    print("✅ Banking Data Processing Complete!")
    print(f"   Total PII Anonymized: {combined_pii_report['anonymized_count']}")
    print(f"   Compliance Report: {CONFIG_DIR / 'pii_compliance_report.json'}")

    return anonymized_customers, anonymized_transactions, compliance_report


if __name__ == "__main__":
    process_banking_data()
