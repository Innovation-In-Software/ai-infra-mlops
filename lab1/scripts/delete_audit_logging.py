"""Delete Lab 1.1 audit logging so you can re-run enable_audit_logging.py."""
import argparse
import json

import boto3

from lab_paths import CONFIG_DIR, ensure_workspace

DASHBOARD_NAME = "Banking-MLOps-Audit-Dashboard"
LOGS_POLICY_NAME = "BankingMLOpsCloudTrailLogsPolicy"
ROLE_POLICY_NAME = "CloudTrailCloudWatchLogsPolicy"


def load_bucket_names():
    config_path = CONFIG_DIR / "buckets.json"
    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            data = json.load(f)
        if data:
            return {k: v["name"] for k, v in data.items() if v.get("name")}

    account_id = boto3.client("sts").get_caller_identity()["Account"]
    types = ("raw", "processed", "models", "monitoring", "governance", "audit")
    return {t: f"bank-mlops-{account_id}-{t}" for t in types}


def delete_audit_logging(dry_run=False):
    ensure_workspace()
    account_id = boto3.client("sts").get_caller_identity()["Account"]
    region = "us-west-2"

    trail_name = f"BankingMLOpsAuditTrail-{account_id}"
    role_name = f"CloudTrailBankingRole-{account_id}"
    log_group_name = f"/aws/cloudtrail/banking-mlops-{account_id}"
    logs_policy_name = f"{LOGS_POLICY_NAME}-{account_id}"

    cloudtrail = boto3.client("cloudtrail", region_name=region)
    s3 = boto3.client("s3", region_name=region)
    logs = boto3.client("logs", region_name=region)
    iam = boto3.client("iam")
    cloudwatch = boto3.client("cloudwatch", region_name=region)
    buckets = load_bucket_names()

    print("Delete Lab 1.1 audit logging")
    print("=" * 60)

    try:
        if dry_run:
            print(f"   would stop and delete trail: {trail_name}")
        else:
            try:
                cloudtrail.stop_logging(Name=trail_name)
                print(f"   stopped logging: {trail_name}")
            except cloudtrail.exceptions.TrailNotFoundException:
                print(f"   skip (trail not found): {trail_name}")
            else:
                cloudtrail.delete_trail(Name=trail_name)
                print(f"   deleted trail: {trail_name}")
    except Exception as e:
        print(f"   ⚠️ trail cleanup: {e}")

    for bucket_type, bucket_name in buckets.items():
        if bucket_type == "audit":
            continue
        if dry_run:
            print(f"   would disable access logging: {bucket_name}")
            continue
        try:
            s3.put_bucket_logging(Bucket=bucket_name, BucketLoggingStatus={})
            print(f"   disabled access logging: {bucket_name}")
        except Exception as e:
            print(f"   ⚠️ {bucket_name}: {e}")

    if dry_run:
        print(f"   would delete dashboard: {DASHBOARD_NAME}")
    else:
        try:
            cloudwatch.delete_dashboards(DashboardNames=[DASHBOARD_NAME])
            print(f"   deleted dashboard: {DASHBOARD_NAME}")
        except Exception as e:
            print(f"   ⚠️ dashboard: {e}")

    if dry_run:
        print(f"   would delete log group: {log_group_name}")
        print(f"   would delete IAM role: {role_name}")
    else:
        try:
            logs.delete_log_group(logGroupName=log_group_name)
            print(f"   deleted log group: {log_group_name}")
        except logs.exceptions.ResourceNotFoundException:
            print(f"   skip (log group not found): {log_group_name}")
        except Exception as e:
            print(f"   ⚠️ log group: {e}")

        try:
            logs.delete_resource_policy(policyName=logs_policy_name)
            print(f"   deleted logs resource policy: {logs_policy_name}")
        except logs.exceptions.ResourceNotFoundException:
            pass
        except Exception as e:
            print(f"   ⚠️ logs resource policy: {e}")

        try:
            iam.delete_role_policy(RoleName=role_name, PolicyName=ROLE_POLICY_NAME)
        except iam.exceptions.NoSuchEntityException:
            pass
        try:
            iam.delete_role(RoleName=role_name)
            print(f"   deleted IAM role: {role_name}")
        except iam.exceptions.NoSuchEntityException:
            print(f"   skip (role not found): {role_name}")
        except Exception as e:
            print(f"   ⚠️ role: {e}")

    print("\n" + "=" * 60)
    if dry_run:
        print("Dry run — no resources deleted.")
    else:
        print("Done — audit logging removed.")
    print("Re-run: python scripts\\enable_audit_logging.py")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Delete Lab 1.1 CloudTrail, log group, and S3 access logging"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted")
    args = parser.parse_args()
    delete_audit_logging(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
