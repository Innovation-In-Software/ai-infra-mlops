"""Create S3 buckets with banking compliance settings."""
import boto3
import json
from datetime import datetime, timezone

from lab_paths import CONFIG_DIR, LOGS_DIR, ensure_workspace


def _bucket_exists(s3, bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        return True
    except s3.exceptions.ClientError:
        return False


def create_banking_buckets():
    """
    Create S3 buckets with banking compliance settings
    Includes encryption, versioning, lifecycle, logging, and classification
    """

    print("📦 Creating Banking-Compliant S3 Buckets")
    print("=" * 60)

    ensure_workspace()
    s3 = boto3.client("s3", region_name="us-west-2")
    account_id = boto3.client("sts").get_caller_identity()["Account"]

    with open(CONFIG_DIR / "kms_keys.json", "r", encoding="utf-8") as f:
        keys = json.load(f)

    buckets_config = {
        "raw": {
            "classification": "PII",
            "retention_days": 365,
            "description": "Raw banking data - PII must be removed before processing",
        },
        "processed": {
            "classification": "Non-PII",
            "retention_days": 2555,
            "description": "Processed banking data - PII removed, ready for ML",
        },
        "models": {
            "classification": "Confidential",
            "retention_days": 2555,
            "description": "Model artifacts with confidential business logic",
        },
        "monitoring": {
            "classification": "Confidential",
            "retention_days": 730,
            "description": "Model monitoring data for compliance",
        },
        "governance": {
            "classification": "Public",
            "retention_days": 2555,
            "description": "Governance, audit trails, and compliance reports",
        },
        "audit": {
            "classification": "Public",
            "retention_days": 2555,
            "description": "Audit logs for regulatory compliance",
        },
    }

    folders = {
        "raw": ["raw_data/", "metadata/", "validation_reports/"],
        "processed": ["training/", "validation/", "test/", "feature_store/"],
        "models": ["models/", "best_models/", "experiments/", "model_metadata/"],
        "monitoring": ["baseline/", "reports/", "drift_detection/", "performance/"],
        "governance": ["approvals/", "compliance/", "audit_reports/", "explainability/"],
        "audit": ["cloudtrail/", "access_logs/", "ml_audits/", "regulatory/"],
    }

    created_buckets = {}

    for bucket_type, config in buckets_config.items():
        bucket_name = f"bank-mlops-{account_id}-{bucket_type}"

        print(f"\n📋 Creating {bucket_type.upper()} Bucket: {bucket_name}")
        print(f"   Classification: {config['classification']}")
        print(f"   Retention: {config['retention_days']} days")

        try:
            if _bucket_exists(s3, bucket_name):
                print("   ⚠️ Bucket already exists — applying configuration")
            else:
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": "us-west-2"},
                )
                print("   ✅ Bucket created")

            s3.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={"Status": "Enabled"},
            )
            print("   ✅ Versioning enabled")

            s3.put_bucket_encryption(
                Bucket=bucket_name,
                ServerSideEncryptionConfiguration={
                    "Rules": [
                        {
                            "ApplyServerSideEncryptionByDefault": {
                                "SSEAlgorithm": "aws:kms",
                                "KMSMasterKeyID": keys["s3_key_id"],
                            }
                        }
                    ]
                },
            )
            print("   ✅ Encryption configured")

            lifecycle_rules = {
                "Rules": [
                    {
                        "ID": "ComplianceRetention",
                        "Status": "Enabled",
                        "Filter": {"Prefix": ""},
                        "Expiration": {"Days": config["retention_days"]},
                        "NoncurrentVersionExpiration": {"NoncurrentDays": 30},
                    }
                ]
            }

            if config["retention_days"] > 730:
                lifecycle_rules["Rules"].append(
                    {
                        "ID": "TransitionToGlacier",
                        "Status": "Enabled",
                        "Filter": {"Prefix": ""},
                        "Transitions": [
                            {"Days": 365, "StorageClass": "STANDARD_IA"},
                            {"Days": 730, "StorageClass": "GLACIER"},
                        ],
                    }
                )

            s3.put_bucket_lifecycle_configuration(
                Bucket=bucket_name, LifecycleConfiguration=lifecycle_rules
            )
            print("   ✅ Lifecycle rules configured")

            s3.put_bucket_tagging(
                Bucket=bucket_name,
                Tagging={
                    "TagSet": [
                        {"Key": "DataClassification", "Value": config["classification"]},
                        {"Key": "ComplianceStandard", "Value": "Banking-Regulated"},
                        {"Key": "Environment", "Value": "MLOps"},
                        {"Key": "Region", "Value": "us-west-2"},
                        {"Key": "RetentionDays", "Value": str(config["retention_days"])},
                        {"Key": "Service", "Value": "SageMaker"},
                        {"Key": "Owner", "Value": "DataScienceTeam"},
                        {"Key": "CreatedBy", "Value": "Lab1.1"},
                    ]
                },
            )
            print("   ✅ Classification tags applied")

            for folder in folders.get(bucket_type, []):
                s3.put_object(Bucket=bucket_name, Key=folder)
            print(f"   ✅ Folder structure created: {', '.join(folders.get(bucket_type, []))}")

            if bucket_type != "audit":
                bucket_policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "DenyInsecureConnections",
                            "Effect": "Deny",
                            "Principal": "*",
                            "Action": "s3:*",
                            "Resource": [
                                f"arn:aws:s3:::{bucket_name}",
                                f"arn:aws:s3:::{bucket_name}/*",
                            ],
                            "Condition": {"Bool": {"aws:SecureTransport": "false"}},
                        },
                    ],
                }
                s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
                print("   ✅ Security policy applied")

            created_buckets[bucket_type] = {
                "name": bucket_name,
                "classification": config["classification"],
                "retention_days": config["retention_days"],
            }
            print(f"   ✅ Bucket {bucket_name} fully configured")

        except Exception as e:
            print(f"   ❌ Error creating bucket: {str(e)}")
            with open(LOGS_DIR / "errors.log", "a", encoding="utf-8") as f:
                f.write(
                    f"[{datetime.now(timezone.utc).isoformat()}] Error creating {bucket_type}: {str(e)}\n"
                )

    with open(CONFIG_DIR / "buckets.json", "w", encoding="utf-8") as f:
        json.dump(created_buckets, f, indent=2)

    print("\n" + "=" * 60)
    if len(created_buckets) == len(buckets_config):
        print("✅ All Banking-Compliant Buckets Created!")
    else:
        print(f"⚠️ Completed {len(created_buckets)}/{len(buckets_config)} buckets — see errors above")
    print("\n📋 Bucket Summary:")
    for bucket_type, info in created_buckets.items():
        print(f"   {bucket_type.upper()}: {info['name']}")
        print(f"      Classification: {info['classification']}")
        print(f"      Retention: {info['retention_days']} days")

    return created_buckets


if __name__ == "__main__":
    create_banking_buckets()
