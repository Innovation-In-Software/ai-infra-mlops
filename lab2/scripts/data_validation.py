"""Banking data validation for compliance."""
import json
from datetime import datetime, timezone

import boto3
import pandas as pd
from lab_paths import CONFIG_DIR, DATA_DIR, LAB1_CONFIG_DIR, RESULTS_DIR, ensure_workspace


class BankingDataValidator:
    """Banking-specific data validation for compliance."""

    def __init__(self):
        self.validation_rules = {
            "amount": {"min": 0, "max": 1000000, "type": "float", "required": True},
            "risk_score": {"min": 0, "max": 100, "type": "float", "required": True},
            "credit_score": {"min": 300, "max": 850, "type": "int", "required": False},
            "age": {"min": 18, "max": 120, "type": "int", "required": False},
            "income": {"min": 0, "max": 10000000, "type": "float", "required": False},
        }

        self.patterns = {
            "account_number": r"^\d{8,12}$",
            "routing_number": r"^\d{9}$",
            "zip_code": r"^\d{5}(-\d{4})?$",
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "phone": r"^\d{3}-\d{3}-\d{4}$",
        }

    def validate_dataframe(self, df, table_name):
        print(f"\n📋 Validating {table_name} Data...")
        print("=" * 60)

        validation_results = {
            "table_name": table_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_rows": len(df),
            "checks": {},
            "issues": [],
            "summary": {},
        }

        print("\n🔍 Checking for Null Values...")
        null_counts = df.isnull().sum()
        null_columns = null_counts[null_counts > 0]

        if not null_columns.empty:
            validation_results["checks"]["null_values"] = {
                "status": "WARNING",
                "details": null_columns.to_dict(),
            }
            for col, count in null_columns.items():
                validation_results["issues"].append(
                    {
                        "type": "NULL_VALUE",
                        "column": col,
                        "count": count,
                        "percentage": (count / len(df)) * 100,
                    }
                )
        else:
            validation_results["checks"]["null_values"] = {
                "status": "PASS",
                "details": "No null values found",
            }

        print("🔍 Checking for Duplicates...")
        duplicates = df.duplicated().sum()

        if duplicates > 0:
            validation_results["checks"]["duplicates"] = {
                "status": "WARNING",
                "details": f"{duplicates} duplicate rows found",
            }
            validation_results["issues"].append(
                {
                    "type": "DUPLICATE",
                    "count": duplicates,
                    "percentage": (duplicates / len(df)) * 100,
                }
            )
        else:
            validation_results["checks"]["duplicates"] = {
                "status": "PASS",
                "details": "No duplicates found",
            }

        print("🔍 Validating Data Types...")
        for col, dtype in df.dtypes.items():
            if col in self.validation_rules:
                expected_type = self.validation_rules[col]["type"]
                actual_type = dtype.name
                if expected_type not in actual_type:
                    validation_results["checks"][f"type_{col}"] = {
                        "status": "FAIL",
                        "details": f"Expected {expected_type}, got {actual_type}",
                    }
                    validation_results["issues"].append(
                        {
                            "type": "DATA_TYPE_MISMATCH",
                            "column": col,
                            "expected": expected_type,
                            "actual": actual_type,
                        }
                    )
                else:
                    validation_results["checks"][f"type_{col}"] = {
                        "status": "PASS",
                        "details": f"Correct type: {actual_type}",
                    }

        print("🔍 Validating Value Ranges...")
        for col, rules in self.validation_rules.items():
            if col in df.columns and "min" in rules and "max" in rules:
                invalid = df[(df[col] < rules["min"]) | (df[col] > rules["max"])][col]
                if not invalid.empty:
                    validation_results["checks"][f"range_{col}"] = {
                        "status": "WARNING",
                        "details": f"{len(invalid)} values outside range [{rules['min']}, {rules['max']}]",
                    }
                    validation_results["issues"].append(
                        {
                            "type": "OUT_OF_RANGE",
                            "column": col,
                            "count": len(invalid),
                            "percentage": (len(invalid) / len(df)) * 100,
                            "min": invalid.min(),
                            "max": invalid.max(),
                        }
                    )
                else:
                    validation_results["checks"][f"range_{col}"] = {
                        "status": "PASS",
                        "details": f"All values in range [{rules['min']}, {rules['max']}]",
                    }

        print("🔍 Validating Patterns...")
        for col, pattern in self.patterns.items():
            if col in df.columns:
                invalid = df[~df[col].astype(str).str.match(pattern)][col]
                if not invalid.empty:
                    validation_results["checks"][f"pattern_{col}"] = {
                        "status": "WARNING",
                        "details": f"{len(invalid)} values don't match pattern",
                    }
                    validation_results["issues"].append(
                        {
                            "type": "PATTERN_MISMATCH",
                            "column": col,
                            "count": len(invalid),
                            "percentage": (len(invalid) / len(df)) * 100,
                        }
                    )
                else:
                    validation_results["checks"][f"pattern_{col}"] = {
                        "status": "PASS",
                        "details": "All values match pattern",
                    }

        print("🔍 Verifying PII Anonymization...")
        pii_patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "account": r"\b\d{8,12}\b",
        }

        pii_found = []
        for col in df.select_dtypes(include=["object"]).columns:
            for pii_type, pattern in pii_patterns.items():
                matches = df[col].astype(str).str.contains(pattern, regex=True)
                if matches.any():
                    pii_found.append({"column": col, "type": pii_type, "count": int(matches.sum())})

        if pii_found:
            validation_results["checks"]["pii_anonymization"] = {
                "status": "FAIL",
                "details": f"PII still found: {pii_found}",
            }
            validation_results["issues"].append({"type": "PII_FOUND", "details": pii_found})
        else:
            validation_results["checks"]["pii_anonymization"] = {
                "status": "PASS",
                "details": "No PII detected",
            }

        total_checks = len(validation_results["checks"])
        passed = sum(1 for c in validation_results["checks"].values() if c["status"] == "PASS")
        warnings = sum(1 for c in validation_results["checks"].values() if c["status"] == "WARNING")
        failed = sum(1 for c in validation_results["checks"].values() if c["status"] == "FAIL")

        validation_results["summary"] = {
            "total_checks": total_checks,
            "passed": passed,
            "warnings": warnings,
            "failed": failed,
            "data_quality_score": (passed / total_checks * 100) if total_checks > 0 else 0,
            "recommendation": "APPROVE_FOR_TRAINING" if passed / total_checks >= 0.8 else "REVIEW_REQUIRED",
        }

        print("\n" + "=" * 60)
        print(f"📊 Validation Summary for {table_name}:")
        print(f"   Total Checks: {total_checks}")
        print(f"   Passed: {passed}")
        print(f"   Warnings: {warnings}")
        print(f"   Failed: {failed}")
        print(f"   Quality Score: {validation_results['summary']['data_quality_score']:.1f}%")
        print(f"   Recommendation: {validation_results['summary']['recommendation']}")

        return validation_results

    def generate_quality_report(self, results, table_name):
        quality_report = {
            "report_type": "Data Quality Compliance Report",
            "table_name": table_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "validation_results": results,
            "compliance_standards": [
                "BCBS 239 - Data Quality Requirements",
                "GDPR - Data Accuracy",
                "NYDFS - Data Integrity",
                "FISMA - Data Quality",
            ],
            "action_items": [
                "Review failed validations immediately",
                "Address warnings in next data update",
                "Document all data quality issues for audit",
            ],
        }

        with open(CONFIG_DIR / f"data_quality_report_{table_name}.json", "w", encoding="utf-8") as f:
            json.dump(quality_report, f, indent=2)

        account_id = boto3.client("sts").get_caller_identity()["Account"]
        s3 = boto3.client("s3", region_name="us-west-2")
        s3_key = f"data_quality/{table_name}_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
        s3.put_object(
            Bucket=f"bank-mlops-{account_id}-monitoring",
            Key=s3_key,
            Body=json.dumps(quality_report, indent=2),
        )

        return quality_report


def validate_all_data():
    ensure_workspace()
    print("🔍 Validating All Banking Data")
    print("=" * 60)

    customers_df = pd.read_csv(DATA_DIR / "anonymized_customers.csv")
    transactions_df = pd.read_csv(DATA_DIR / "anonymized_transactions.csv")

    validator = BankingDataValidator()

    customer_results = validator.validate_dataframe(customers_df, "customers")
    validator.generate_quality_report(customer_results, "customers")

    transaction_results = validator.validate_dataframe(transactions_df, "transactions")
    validator.generate_quality_report(transaction_results, "transactions")

    print("\n" + "=" * 60)
    print("✅ Data Validation Complete!")
    print(f"   Customer Quality Score: {customer_results['summary']['data_quality_score']:.1f}%")
    print(f"   Transaction Quality Score: {transaction_results['summary']['data_quality_score']:.1f}%")

    return customer_results, transaction_results


if __name__ == "__main__":
    validate_all_data()
