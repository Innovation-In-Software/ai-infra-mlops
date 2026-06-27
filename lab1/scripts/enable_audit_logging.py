"""Enable comprehensive audit logging for banking compliance."""
import boto3
import json

from lab_paths import CONFIG_DIR, ensure_workspace


def enable_audit_logging():
    """
    Enable comprehensive audit logging for banking compliance
    Includes CloudTrail, S3 access logging, and CloudWatch
    """

    print("📝 Enabling Audit Logging for Banking Compliance")
    print("=" * 60)

    ensure_workspace()
    cloudtrail = boto3.client("cloudtrail", region_name="us-west-2")
    s3 = boto3.client("s3", region_name="us-west-2")
    logs = boto3.client("logs", region_name="us-west-2")
    account_id = boto3.client("sts").get_caller_identity()["Account"]

    with open(CONFIG_DIR / "buckets.json", "r", encoding="utf-8") as f:
        buckets = json.load(f)

    print("\n📋 Creating CloudWatch Log Group for CloudTrail...")

    log_group_name = f"/aws/cloudtrail/banking-mlops-{account_id}"

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
        logs.put_retention_policy(logGroupName=log_group_name, retentionInDays=2555)
        print("   ✅ Log retention set to 7 years")
    except logs.exceptions.ResourceAlreadyExistsException:
        print(f"   ⚠️ Log Group already exists: {log_group_name}")

    print("\n📋 Creating CloudTrail Trail for MLOps...")

    trail_name = f"BankingMLOpsAuditTrail-{account_id}"
    bucket_name = buckets["audit"]["name"]

    try:
        iam = boto3.client("iam")
        role_name = f"CloudTrailBankingRole-{account_id}"

        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "cloudtrail.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }

        try:
            iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description="CloudTrail role for banking MLOps audit",
            )
            print(f"   ✅ CloudTrail role created: {role_name}")
        except iam.exceptions.EntityAlreadyExistsException:
            print(f"   ⚠️ CloudTrail role already exists: {role_name}")

        role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"

        try:
            cloudtrail.create_trail(
                Name=trail_name,
                S3BucketName=bucket_name,
                S3KeyPrefix="cloudtrail",
                CloudWatchLogsLogGroupArn=f"arn:aws:logs:us-west-2:{account_id}:log-group:{log_group_name}",
                CloudWatchLogsRoleArn=role_arn,
                IncludeGlobalServiceEvents=True,
                IsMultiRegionTrail=False,
                EnableLogFileValidation=True,
                TagsList=[
                    {"Key": "Environment", "Value": "MLOps"},
                    {"Key": "Compliance", "Value": "Banking"},
                    {"Key": "Service", "Value": "CloudTrail"},
                    {"Key": "Owner", "Value": "DataScienceTeam"},
                ],
            )
            print(f"   ✅ CloudTrail trail created: {trail_name}")
            cloudtrail.start_logging(Name=trail_name)
            print("   ✅ Logging started")
        except cloudtrail.exceptions.TrailAlreadyExistsException:
            print(f"   ⚠️ Trail already exists: {trail_name}")

    except Exception as e:
        print(f"   ❌ Error creating CloudTrail: {str(e)}")

    print("\n📋 Enabling S3 Access Logging...")

    for bucket_type, bucket_info in buckets.items():
        bucket_name = bucket_info["name"]
        audit_bucket = buckets["audit"]["name"]

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

    try:
        trail = cloudtrail.get_trail(Name=trail_name)
        cloudtrail.update_trail(
            Name=trail_name,
            TrailARN=trail["TrailARN"],
            IncludeGlobalServiceEvents=True,
        )
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

    print("\n📋 Creating Audit Dashboard...")

    cloudwatch = boto3.client("cloudwatch", region_name="us-west-2")

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
                    "region": "us-west-2",
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
                    "region": "us-west-2",
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
                    "region": "us-west-2",
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
    print("✅ Audit Logging Enabled!")
    print(f"   CloudTrail Trail: {trail_name}")
    print(f"   Log Group: {log_group_name}")
    print(f"   Audit Bucket: {bucket_name}")
    print("\n📋 Audit Dashboard URL:")
    print(
        "   https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#dashboards:name=Banking-MLOps-Audit-Dashboard"
    )


if __name__ == "__main__":
    enable_audit_logging()
