"""Enable comprehensive audit logging for banking compliance."""
import json
import time

import boto3
from botocore.exceptions import ClientError

from lab_paths import CONFIG_DIR, ensure_workspace

# CloudWatch accepts discrete retention values only; 2557 days ≈ 7 years
LOG_RETENTION_DAYS = 2557
LOGS_POLICY_NAME = "BankingMLOpsCloudTrailLogsPolicy"
ROLE_POLICY_NAME = "CloudTrailCloudWatchLogsPolicy"
IAM_PROPAGATION_WAIT_SEC = 12
CREATE_TRAIL_RETRIES = 5


def log_group_arn_base(region: str, account_id: str, log_group_name: str) -> str:
    """Base CloudWatch log group ARN (no :* suffix)."""
    return f"arn:aws:logs:{region}:{account_id}:log-group:{log_group_name}"


def log_group_arn_for_trail(region: str, account_id: str, log_group_name: str) -> str:
    """ARN for CreateTrail/UpdateTrail CloudWatchLogsLogGroupArn (requires :* suffix)."""
    return f"{log_group_arn_base(region, account_id, log_group_name)}:*"


def cloudtrail_role_policy(region: str, account_id: str, log_group_name: str) -> dict:
    """IAM role policy per AWS CloudTrail + CloudWatch Logs integration docs."""
    log_group_arn = log_group_arn_base(region, account_id, log_group_name)
    stream_prefix = f"{account_id}_CloudTrail_{region}"
    stream_arn = f"{log_group_arn}:log-stream:{stream_prefix}*"
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailCreateLogStream",
                "Effect": "Allow",
                "Action": ["logs:CreateLogStream"],
                "Resource": [stream_arn],
            },
            {
                "Sid": "AWSCloudTrailPutLogEvents",
                "Effect": "Allow",
                "Action": ["logs:PutLogEvents"],
                "Resource": [stream_arn],
            },
        ],
    }


def ensure_cloudtrail_role(iam, account_id, role_name, log_group_name, region):
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAssumeRole",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    }

    created = False
    try:
        iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="CloudTrail role for banking MLOps audit",
        )
        print(f"   ✅ CloudTrail role created: {role_name}")
        created = True
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"   ⚠️ CloudTrail role already exists: {role_name}")
        iam.update_assume_role_policy(
            RoleName=role_name,
            PolicyDocument=json.dumps(trust_policy),
        )

    iam.put_role_policy(
        RoleName=role_name,
        PolicyName=ROLE_POLICY_NAME,
        PolicyDocument=json.dumps(cloudtrail_role_policy(region, account_id, log_group_name)),
    )
    print("   ✅ CloudTrail role policy attached for CloudWatch Logs")

    if created:
        print(f"   ⏳ Waiting {IAM_PROPAGATION_WAIT_SEC}s for IAM role propagation...")
        time.sleep(IAM_PROPAGATION_WAIT_SEC)

    return f"arn:aws:iam::{account_id}:role/{role_name}"


def ensure_audit_bucket_policy(s3, account_id, audit_bucket, region):
    from create_banking_buckets import audit_bucket_policy

    policy = audit_bucket_policy(account_id, audit_bucket, region)
    s3.put_bucket_policy(Bucket=audit_bucket, Policy=json.dumps(policy))
    print(f"   ✅ Audit bucket policy applied: {audit_bucket}")


def ensure_log_group_policy(logs, account_id, region, log_group_name, trail_name):
    trail_arn = f"arn:aws:cloudtrail:{region}:{account_id}:trail/{trail_name}"
    log_group_arn = log_group_arn_base(region, account_id, log_group_name)

    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailCreateLogStream",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "logs:CreateLogStream",
                "Resource": f"{log_group_arn}:log-stream:*",
                "Condition": {"StringEquals": {"AWS:SourceArn": trail_arn}},
            },
            {
                "Sid": "AWSCloudTrailPutLogEvents",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "logs:PutLogEvents",
                "Resource": f"{log_group_arn}:log-stream:*",
                "Condition": {"StringEquals": {"AWS:SourceArn": trail_arn}},
            },
        ],
    }

    logs.put_resource_policy(
        policyName=f"{LOGS_POLICY_NAME}-{account_id}",
        policyDocument=json.dumps(policy_document),
    )
    print("   ✅ CloudWatch Logs resource policy configured for CloudTrail")


def create_or_start_trail(
    cloudtrail,
    trail_name: str,
    audit_bucket: str,
    log_group_arn: str,
    role_arn: str,
    account_id: str,
) -> bool:
    """Create trail (with retries) or update existing trail with CloudWatch Logs."""
    tags = [
        {"Key": "Environment", "Value": "MLOps"},
        {"Key": "Compliance", "Value": "Banking"},
        {"Key": "Service", "Value": "CloudTrail"},
        {"Key": "Owner", "Value": "DataScienceTeam"},
    ]
    trail_kwargs = {
        "Name": trail_name,
        "S3BucketName": audit_bucket,
        "S3KeyPrefix": "cloudtrail",
        "CloudWatchLogsLogGroupArn": log_group_arn,
        "CloudWatchLogsRoleArn": role_arn,
        "IncludeGlobalServiceEvents": True,
        "IsMultiRegionTrail": False,
        "EnableLogFileValidation": True,
        "TagsList": tags,
    }

    for attempt in range(1, CREATE_TRAIL_RETRIES + 1):
        try:
            cloudtrail.create_trail(**trail_kwargs)
            print(f"   ✅ CloudTrail trail created: {trail_name}")
            cloudtrail.start_logging(Name=trail_name)
            print("   ✅ Logging started")
            return True
        except cloudtrail.exceptions.TrailAlreadyExistsException:
            print(f"   ⚠️ Trail already exists: {trail_name} — updating CloudWatch Logs")
            cloudtrail.update_trail(
                Name=trail_name,
                CloudWatchLogsLogGroupArn=log_group_arn,
                CloudWatchLogsRoleArn=role_arn,
            )
            cloudtrail.start_logging(Name=trail_name)
            print("   ✅ Trail updated and logging started")
            return True
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code == "InvalidCloudWatchLogsRoleArnException" and attempt < CREATE_TRAIL_RETRIES:
                wait = IAM_PROPAGATION_WAIT_SEC * attempt
                print(
                    f"   ⏳ IAM role not ready yet (attempt {attempt}/{CREATE_TRAIL_RETRIES}) "
                    f"— retrying in {wait}s..."
                )
                time.sleep(wait)
                continue
            raise

    return False


def enable_audit_logging():
    """
    Enable comprehensive audit logging for banking compliance
    Includes CloudTrail, S3 access logging, and CloudWatch
    """

    print("📝 Enabling Audit Logging for Banking Compliance")
    print("=" * 60)

    ensure_workspace()
    region = "us-west-2"
    cloudtrail = boto3.client("cloudtrail", region_name=region)
    s3 = boto3.client("s3", region_name=region)
    logs = boto3.client("logs", region_name=region)
    iam = boto3.client("iam")
    account_id = boto3.client("sts").get_caller_identity()["Account"]

    with open(CONFIG_DIR / "buckets.json", "r", encoding="utf-8") as f:
        buckets = json.load(f)

    trail_name = f"BankingMLOpsAuditTrail-{account_id}"
    role_name = f"CloudTrailBankingRole-{account_id}"
    log_group_name = f"/aws/cloudtrail/banking-mlops-{account_id}"
    audit_bucket = buckets["audit"]["name"]
    log_group_arn = log_group_arn_for_trail(region, account_id, log_group_name)

    cloudtrail_ok = False

    print("\n📋 Creating CloudWatch Log Group for CloudTrail...")

    try:
        logs.create_log_group(
            logGroupName=log_group_name,
            tags={
                "Environment": "MLOps",
                "Compliance": "Banking",
                "Service": "CloudTrail",
                "Owner": "DataScienceTeam",
            },
        )
        print(f"   ✅ CloudWatch Log Group created: {log_group_name}")
    except logs.exceptions.ResourceAlreadyExistsException:
        print(f"   ⚠️ Log Group already exists: {log_group_name}")

    logs.put_retention_policy(logGroupName=log_group_name, retentionInDays=LOG_RETENTION_DAYS)
    print(f"   ✅ Log retention set to {LOG_RETENTION_DAYS} days (~7 years)")

    print("\n📋 Creating CloudTrail Trail for MLOps...")

    try:
        ensure_audit_bucket_policy(s3, account_id, audit_bucket, region)
        role_arn = ensure_cloudtrail_role(
            iam, account_id, role_name, log_group_name, region
        )
        ensure_log_group_policy(logs, account_id, region, log_group_name, trail_name)

        cloudtrail_ok = create_or_start_trail(
            cloudtrail,
            trail_name,
            audit_bucket,
            log_group_arn,
            role_arn,
            account_id,
        )
    except Exception as e:
        print(f"   ❌ Error creating CloudTrail: {str(e)}")
        print(
            "   💡 CloudTrail errors: wait 60s and re-run "
            "python3 scripts/enable_audit_logging.py"
        )
        print(
            "      RoleArnException = IAM propagation; LogGroupArnException = "
            "git pull for latest script fix"
        )

    print("\n📋 Enabling S3 Access Logging...")

    for bucket_type, bucket_info in buckets.items():
        bucket_name = bucket_info["name"]

        try:
            if bucket_type != "audit":
                s3.put_bucket_logging(
                    Bucket=bucket_name,
                    BucketLoggingStatus={
                        "LoggingEnabled": {
                            "TargetBucket": audit_bucket,
                            "TargetPrefix": f"access_logs/{bucket_type}/",
                        }
                    },
                )
                print(f"   ✅ Access logging enabled for {bucket_name}")
        except Exception as e:
            print(f"   ❌ Error enabling logging for {bucket_name}: {str(e)}")

    print("\n📋 Enabling S3 Object-Level Logging...")

    if cloudtrail_ok:
        try:
            cloudtrail.put_event_selectors(
                TrailName=trail_name,
                EventSelectors=[
                    {
                        "ReadWriteType": "All",
                        "IncludeManagementEvents": True,
                        "DataResources": [
                            {
                                "Type": "AWS::S3::Object",
                                "Values": [
                                    f"arn:aws:s3:::{buckets['processed']['name']}/",
                                    f"arn:aws:s3:::{buckets['models']['name']}/",
                                    f"arn:aws:s3:::{buckets['governance']['name']}/",
                                ],
                            }
                        ],
                    }
                ],
            )
            print("   ✅ S3 object-level logging enabled for data buckets")
        except Exception as e:
            print(f"   ❌ Error enabling S3 object-level logging: {str(e)}")
    else:
        print("   ⚠️ Skipped — CloudTrail trail was not created")

    print("\n📋 Creating Audit Dashboard...")

    cloudwatch = boto3.client("cloudwatch", region_name=region)

    dashboard_body = {
        "widgets": [
            {
                "type": "metric",
                "x": 0,
                "y": 0,
                "width": 12,
                "height": 6,
                "properties": {
                    "metrics": [["CloudTrail", "EventCount", {"stat": "Sum"}]],
                    "period": 300,
                    "stat": "Sum",
                    "region": region,
                    "title": "CloudTrail Events (Last 24h)",
                },
            },
            {
                "type": "metric",
                "x": 12,
                "y": 0,
                "width": 12,
                "height": 6,
                "properties": {
                    "metrics": [["AWS/S3", "NumberOfObjects", {"stat": "Average"}]],
                    "period": 300,
                    "stat": "Average",
                    "region": region,
                    "title": "S3 Objects by Bucket",
                },
            },
            {
                "type": "metric",
                "x": 0,
                "y": 6,
                "width": 24,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/SageMaker", "EndpointInvocations", {"stat": "Sum"}],
                        ["AWS/SageMaker", "EndpointLatency", {"stat": "Average"}],
                    ],
                    "period": 300,
                    "stat": "Average",
                    "region": region,
                    "title": "SageMaker Activity",
                },
            },
        ]
    }

    try:
        cloudwatch.put_dashboard(
            DashboardName="Banking-MLOps-Audit-Dashboard",
            DashboardBody=json.dumps(dashboard_body),
        )
        print("   ✅ Audit dashboard created")
    except Exception as e:
        print(f"   ⚠️ Error creating dashboard: {str(e)}")

    print("\n" + "=" * 60)
    if cloudtrail_ok:
        print("✅ Audit Logging Enabled!")
    else:
        print("⚠️ Audit logging partially enabled — CloudTrail failed; check errors above")
    print(f"   CloudTrail Trail: {trail_name}")
    print(f"   Log Group: {log_group_name}")
    print(f"   Audit Bucket: {audit_bucket}")
    print("\n📋 Audit Dashboard URL:")
    print(
        "   https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#dashboards:name=Banking-MLOps-Audit-Dashboard"
    )
    print("\n📋 Copy the dashboard URL above before closing the terminal.")


if __name__ == "__main__":
    enable_audit_logging()
