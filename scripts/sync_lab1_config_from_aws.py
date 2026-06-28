"""Rebuild workspace/lab1/config/*.json from existing AWS resources (no creates)."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import boto3

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "lab1" / "scripts"))
from lab_paths import CONFIG_DIR, ensure_workspace  # noqa: E402

REGION = "us-west-2"
BUCKET_SUFFIXES = {
    "raw": {"classification": "Confidential", "retention_days": 2555},
    "processed": {"classification": "Confidential", "retention_days": 2555},
    "models": {"classification": "Restricted", "retention_days": 3650},
    "monitoring": {"classification": "Internal", "retention_days": 730},
    "governance": {"classification": "Restricted", "retention_days": 3650},
    "audit": {"classification": "Restricted", "retention_days": 2555},
}
ROLE_NAMES = {
    "data_scientist": "BankingDataScientistRole",
    "ml_engineer": "BankingMLEngineerRole",
    "compliance_officer": "BankingComplianceOfficerRole",
}


def main():
    ensure_workspace()
    sts = boto3.client("sts", region_name=REGION)
    account_id = sts.get_caller_identity()["Account"]
    prefix = f"bank-mlops-{account_id}-"

    s3 = boto3.client("s3", region_name=REGION)
    buckets = {}
    s3_key_id = None
    for suffix, meta in BUCKET_SUFFIXES.items():
        name = f"{prefix}{suffix}"
        try:
            s3.head_bucket(Bucket=name)
        except Exception:
            print(f"   ⚠️  Missing bucket: {name}")
            continue
        enc = s3.get_bucket_encryption(Bucket=name)
        rule = enc["ServerSideEncryptionConfiguration"]["Rules"][0][
            "ApplyServerSideEncryptionByDefault"
        ]
        if rule.get("SSEAlgorithm") == "aws:kms" and not s3_key_id:
            s3_key_id = rule.get("KMSMasterKeyID", "").split("/")[-1]
        buckets[suffix] = {"name": name, **meta}
        print(f"   ✅ {suffix}: {name}")

    if not buckets:
        print("❌ No Lab 1 buckets found — run Lab 1 first.")
        sys.exit(1)

    kms = boto3.client("kms", region_name=REGION)
    sm_key_id = None
    for key in kms.list_keys()["Keys"]:
        meta = kms.describe_key(KeyId=key["KeyId"])["KeyMetadata"]
        desc = meta.get("Description") or ""
        if "SageMaker" in desc and meta["KeyState"] == "Enabled":
            sm_key_id = meta["KeyId"]
            break

    if not s3_key_id or not sm_key_id:
        print("❌ Could not resolve KMS key IDs from AWS.")
        sys.exit(1)

    kms_info = {
        "s3_key_id": s3_key_id,
        "s3_key_arn": f"arn:aws:kms:{REGION}:{account_id}:key/{s3_key_id}",
        "sm_key_id": sm_key_id,
        "sm_key_arn": f"arn:aws:kms:{REGION}:{account_id}:key/{sm_key_id}",
        "account_id": account_id,
        "region": REGION,
        "synced_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(CONFIG_DIR / "kms_keys.json", "w", encoding="utf-8") as f:
        json.dump(kms_info, f, indent=2)
    with open(CONFIG_DIR / "buckets.json", "w", encoding="utf-8") as f:
        json.dump(buckets, f, indent=2)

    iam = boto3.client("iam")
    roles = {}
    for role_type, role_name in ROLE_NAMES.items():
        r = iam.get_role(RoleName=role_name)
        roles[role_type] = {"role_name": role_name, "arn": r["Role"]["Arn"]}
        print(f"   ✅ role {role_type}: {role_name}")
    with open(CONFIG_DIR / "iam_roles.json", "w", encoding="utf-8") as f:
        json.dump(roles, f, indent=2)

    sm = boto3.client("sagemaker", region_name=REGION)
    domain = None
    for d in sm.list_domains()["Domains"]:
        if d["DomainName"].startswith("banking-mlops"):
            domain = sm.describe_domain(DomainId=d["DomainId"])
            break
    if domain:
        cfg = {
            "domain_name": domain["DomainName"],
            "domain_id": domain["DomainId"],
            "domain_arn": domain["DomainArn"],
            "vpc_id": domain.get("VpcId", ""),
            "subnet_ids": domain.get("SubnetIds", []),
            "execution_role_arn": roles["data_scientist"]["arn"],
            "users": [],
            "synced_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(CONFIG_DIR / "sagemaker_studio.json", "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        print(f"   ✅ SageMaker domain: {domain['DomainId']}")

    print(f"\n✅ Synced Lab 1 config → {CONFIG_DIR}")


if __name__ == "__main__":
    print("🔄 Sync Lab 1 config from AWS")
    print("=" * 60)
    main()
