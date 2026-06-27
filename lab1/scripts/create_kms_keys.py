"""Create KMS keys for banking compliance."""
import boto3
import json
from datetime import datetime

from lab_paths import CONFIG_DIR, ensure_workspace


def create_banking_kms_keys():
    """
    Create KMS keys for banking compliance
    Based on Financial Services encryption requirements
    """

    print("🔐 Creating KMS Keys for Banking Compliance")
    print("=" * 60)

    ensure_workspace()
    print(f"   Config: {CONFIG_DIR}")

    kms = boto3.client("kms", region_name="us-west-2")
    account_id = boto3.client("sts").get_caller_identity()["Account"]

    print("\n📋 Creating KMS Key for S3 Data Encryption...")

    s3_key_response = kms.create_key(
        Description=f"Banking S3 Encryption Key - Account {account_id}",
        KeyUsage="ENCRYPT_DECRYPT",
        CustomerMasterKeySpec="SYMMETRIC_DEFAULT",
        Origin="AWS_KMS",
        Tags=[
            {"TagKey": "Environment", "TagValue": "MLOps"},
            {"TagKey": "Compliance", "TagValue": "Banking-Regulated"},
            {"TagKey": "DataClassification", "TagValue": "Confidential"},
            {"TagKey": "Service", "TagValue": "S3"},
            {"TagKey": "Region", "TagValue": "us-west-2"},
            {"TagKey": "Owner", "TagValue": "DataScienceTeam"},
        ],
    )

    s3_key_id = s3_key_response["KeyMetadata"]["KeyId"]
    s3_key_arn = s3_key_response["KeyMetadata"]["Arn"]
    print(f"✅ S3 KMS Key Created: {s3_key_id}")
    print(f"   ARN: {s3_key_arn}")

    print("\n📋 Creating KMS Key for SageMaker...")

    sm_key_response = kms.create_key(
        Description=f"Banking SageMaker Encryption Key - Account {account_id}",
        KeyUsage="ENCRYPT_DECRYPT",
        CustomerMasterKeySpec="SYMMETRIC_DEFAULT",
        Origin="AWS_KMS",
        Tags=[
            {"TagKey": "Environment", "TagValue": "MLOps"},
            {"TagKey": "Compliance", "TagValue": "Banking-Regulated"},
            {"TagKey": "DataClassification", "TagValue": "Confidential"},
            {"TagKey": "Service", "TagValue": "SageMaker"},
            {"TagKey": "Region", "TagValue": "us-west-2"},
            {"TagKey": "Owner", "TagValue": "DataScienceTeam"},
        ],
    )

    sm_key_id = sm_key_response["KeyMetadata"]["KeyId"]
    sm_key_arn = sm_key_response["KeyMetadata"]["Arn"]
    print(f"✅ SageMaker KMS Key Created: {sm_key_id}")
    print(f"   ARN: {sm_key_arn}")

    print("\n📋 Configuring Key Policies for Banking Compliance...")

    s3_key_policy = {
        "Version": "2012-10-17",
        "Id": f"banking-s3-key-policy-{account_id}",
        "Statement": [
            {
                "Sid": "Enable IAM User Permissions",
                "Effect": "Allow",
                "Principal": {"AWS": f"arn:aws:iam::{account_id}:root"},
                "Action": "kms:*",
                "Resource": "*",
            },
            {
                "Sid": "Allow S3 Service Access",
                "Effect": "Allow",
                "Principal": {"Service": "s3.amazonaws.com"},
                "Action": ["kms:GenerateDataKey", "kms:Decrypt"],
                "Resource": "*",
                "Condition": {"StringEquals": {"aws:SourceAccount": account_id}},
            },
            {
                "Sid": "Deny Access Outside us-west-2",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "kms:*",
                "Resource": "*",
                "Condition": {
                    "StringNotEquals": {"aws:RequestedRegion": "us-west-2"}
                },
            },
        ],
    }

    kms.put_key_policy(
        KeyId=s3_key_id, PolicyName="default", Policy=json.dumps(s3_key_policy)
    )
    print("✅ S3 Key Policy Applied")

    keys_info = {
        "s3_key_id": s3_key_id,
        "s3_key_arn": s3_key_arn,
        "sm_key_id": sm_key_id,
        "sm_key_arn": sm_key_arn,
        "account_id": account_id,
        "region": "us-west-2",
        "created_at": datetime.utcnow().isoformat(),
    }

    with open(CONFIG_DIR / "kms_keys.json", "w", encoding="utf-8") as f:
        json.dump(keys_info, f, indent=2)

    print("\n" + "=" * 60)
    print("✅ KMS Key Creation Complete!")
    print(f"S3 Key ID: {s3_key_id}")
    print(f"SageMaker Key ID: {sm_key_id}")

    return keys_info


if __name__ == "__main__":
    create_banking_kms_keys()
