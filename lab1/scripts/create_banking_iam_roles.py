"""Create IAM roles with banking-specific permissions."""
import boto3
import json

from lab_paths import CONFIG_DIR, ensure_workspace


def create_banking_iam_roles():
    """
    Create IAM roles with banking-specific permissions
    Implements least privilege and separation of duties
    """

    print("🔑 Creating Banking-Compliant IAM Roles")
    print("=" * 60)

    ensure_workspace()
    iam = boto3.client("iam")
    account_id = boto3.client("sts").get_caller_identity()["Account"]

    with open(CONFIG_DIR / "buckets.json", "r", encoding="utf-8") as f:
        buckets = json.load(f)

    kms_key_arn = None
    kms_path = CONFIG_DIR / "kms_keys.json"
    if kms_path.exists():
        with open(kms_path, "r", encoding="utf-8") as f:
            kms_key_arn = json.load(f).get("s3_key_arn")

    print("\n📋 Creating Data Scientist Role...")

    data_scientist_trust = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "sagemaker.amazonaws.com"},
                "Action": "sts:AssumeRole",
                "Condition": {"StringEquals": {"aws:SourceAccount": account_id}},
            }
        ],
    }

    data_scientist_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket",
                    "s3:GetBucketAcl",
                    "s3:GetBucketLocation",
                ],
                "Resource": [
                    f"arn:aws:s3:::{buckets['raw']['name']}/*",
                    f"arn:aws:s3:::{buckets['processed']['name']}/*",
                    f"arn:aws:s3:::{buckets['raw']['name']}",
                    f"arn:aws:s3:::{buckets['processed']['name']}",
                ],
            },
            {
                "Effect": "Allow",
                "Action": ["s3:PutObject", "s3:DeleteObject"],
                "Resource": [
                    f"arn:aws:s3:::{buckets['processed']['name']}/training/*",
                    f"arn:aws:s3:::{buckets['processed']['name']}/validation/*",
                    f"arn:aws:s3:::{buckets['processed']['name']}/test/*",
                    f"arn:aws:s3:::{buckets['processed']['name']}/feature_store/*",
                    f"arn:aws:s3:::{buckets['models']['name']}/experiments/*",
                ],
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:ListBucket",
                    "s3:GetBucketLocation",
                ],
                "Resource": [
                    f"arn:aws:s3:::{buckets['models']['name']}",
                    f"arn:aws:s3:::{buckets['models']['name']}/*",
                    f"arn:aws:s3:::sagemaker-us-west-2-{account_id}",
                    f"arn:aws:s3:::sagemaker-us-west-2-{account_id}/*",
                ],
            },
            {
                "Effect": "Allow",
                "Action": [
                    "sagemaker:*Notebook*",
                    "sagemaker:*Experiment*",
                    "sagemaker:*Trial*",
                    "sagemaker:CreateProcessingJob",
                    "sagemaker:DescribeProcessingJob",
                    "sagemaker:ListProcessingJobs",
                    "sagemaker:CreateTrainingJob",
                    "sagemaker:DescribeTrainingJob",
                    "sagemaker:ListTrainingJobs",
                    "sagemaker:CreateHyperParameterTuningJob",
                    "sagemaker:DescribeHyperParameterTuningJob",
                    "sagemaker:ListHyperParameterTuningJobs",
                    "sagemaker:StopHyperParameterTuningJob",
                    "sagemaker:CreateFeatureGroup",
                    "sagemaker:DescribeFeatureGroup",
                    "sagemaker:ListFeatureGroups",
                    "sagemaker:PutRecord",
                    "sagemaker:BatchPutRecord",
                    "sagemaker:DeleteRecord",
                ],
                "Resource": "*",
            },
            {
                "Effect": "Allow",
                "Action": [
                    "ecr:GetAuthorizationToken",
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchGetImage",
                    "ecr:BatchCheckLayerAvailability",
                ],
                "Resource": "*",
            },
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                    "logs:DescribeLogGroups",
                    "logs:DescribeLogStreams",
                ],
                "Resource": "*",
            },
        ],
    }

    if kms_key_arn:
        data_scientist_policy["Statement"].append(
            {
                "Effect": "Allow",
                "Action": [
                    "kms:GenerateDataKey",
                    "kms:Decrypt",
                    "kms:DescribeKey",
                ],
                "Resource": kms_key_arn,
            }
        )

    try:
        iam.create_role(
            RoleName="BankingDataScientistRole",
            AssumeRolePolicyDocument=json.dumps(data_scientist_trust),
            Description="Data Scientist role with banking compliance - read-only for sensitive data",
            Tags=[
                {"Key": "Environment", "Value": "MLOps"},
                {"Key": "Compliance", "Value": "Banking"},
                {"Key": "Team", "Value": "DataScience"},
                {"Key": "RoleType", "Value": "DataScientist"},
            ],
        )
        print("   ✅ Data Scientist role created")
    except Exception as e:
        print(f"   ⚠️ Role may already exist: {str(e)}")

    iam.put_role_policy(
        RoleName="BankingDataScientistRole",
        PolicyName="DataScientistBankingPolicy",
        PolicyDocument=json.dumps(data_scientist_policy),
    )
    print("   ✅ Data Scientist policy attached")

    print("\n📋 Creating ML Engineer Role...")

    ml_engineer_trust = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "sagemaker.amazonaws.com"},
                "Action": "sts:AssumeRole",
                "Condition": {"StringEquals": {"aws:SourceAccount": account_id}},
            },
            {
                "Effect": "Allow",
                "Principal": {"Service": "codepipeline.amazonaws.com"},
                "Action": "sts:AssumeRole",
                "Condition": {"StringEquals": {"aws:SourceAccount": account_id}},
            },
            {
                "Effect": "Allow",
                "Principal": {"Service": "codebuild.amazonaws.com"},
                "Action": "sts:AssumeRole",
                "Condition": {"StringEquals": {"aws:SourceAccount": account_id}},
            },
        ],
    }

    ml_engineer_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:ListBucket",
                ],
                "Resource": [
                    f"arn:aws:s3:::{buckets['models']['name']}",
                    f"arn:aws:s3:::{buckets['models']['name']}/*",
                ],
            },
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:ListBucket"],
                "Resource": [
                    f"arn:aws:s3:::{buckets['processed']['name']}/test/*",
                    f"arn:aws:s3:::{buckets['processed']['name']}/validation/*",
                ],
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:ListBucket",
                    "s3:GetBucketLocation",
                ],
                "Resource": [
                    f"arn:aws:s3:::{buckets['processed']['name']}",
                    f"arn:aws:s3:::{buckets['processed']['name']}/lab8-pipeline/*",
                    f"arn:aws:s3:::sagemaker-us-west-2-{account_id}",
                    f"arn:aws:s3:::sagemaker-us-west-2-{account_id}/*",
                ],
            },
            {
                "Effect": "Allow",
                "Action": [
                    "sagemaker:CreateEndpoint",
                    "sagemaker:DescribeEndpoint",
                    "sagemaker:UpdateEndpoint",
                    "sagemaker:UpdateEndpointWeightsAndCapacities",
                    "sagemaker:DeleteEndpoint",
                    "sagemaker:CreateEndpointConfig",
                    "sagemaker:DescribeEndpointConfig",
                    "sagemaker:UpdateEndpointConfig",
                    "sagemaker:DeleteEndpointConfig",
                    "sagemaker:CreateModel",
                    "sagemaker:DescribeModel",
                    "sagemaker:ListModels",
                    "sagemaker:DeleteModel",
                    "sagemaker:CreateModelPackage",
                    "sagemaker:DescribeModelPackage",
                    "sagemaker:ListModelPackages",
                    "sagemaker:DeleteModelPackage",
                    "sagemaker:CreateModelPackageGroup",
                    "sagemaker:DescribeModelPackageGroup",
                    "sagemaker:ListModelPackageGroups",
                    "sagemaker:DeleteModelPackageGroup",
                    "sagemaker:CreateMonitoringSchedule",
                    "sagemaker:DescribeMonitoringSchedule",
                    "sagemaker:ListMonitoringSchedules",
                    "sagemaker:UpdateMonitoringSchedule",
                    "sagemaker:DeleteMonitoringSchedule",
                    "sagemaker:CreateProcessingJob",
                    "sagemaker:DescribeProcessingJob",
                    "sagemaker:ListProcessingJobs",
                    "sagemaker:StopProcessingJob",
                    "sagemaker:CreatePipeline",
                    "sagemaker:UpdatePipeline",
                    "sagemaker:DescribePipeline",
                    "sagemaker:DeletePipeline",
                    "sagemaker:ListPipelines",
                    "sagemaker:StartPipelineExecution",
                    "sagemaker:DescribePipelineExecution",
                    "sagemaker:ListPipelineExecutions",
                    "sagemaker:ListPipelineExecutionSteps",
                    "sagemaker:StopPipelineExecution",
                    "sagemaker:AddTags",
                    "sagemaker:DeleteTags",
                    "sagemaker:ListTags",
                ],
                "Resource": "*",
            },
            {
                "Effect": "Allow",
                "Action": "iam:PassRole",
                "Resource": f"arn:aws:iam::{account_id}:role/BankingMLEngineerRole",
                "Condition": {
                    "StringEquals": {
                        "iam:PassedToService": "sagemaker.amazonaws.com",
                    }
                },
            },
            {
                "Effect": "Allow",
                "Action": [
                    "ecr:GetAuthorizationToken",
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchGetImage",
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:PutImage",
                    "ecr:InitiateLayerUpload",
                    "ecr:UploadLayerPart",
                    "ecr:CompleteLayerUpload",
                ],
                "Resource": "*",
            },
            {
                "Effect": "Allow",
                "Action": [
                    "cloudwatch:PutMetricData",
                    "cloudwatch:GetMetricData",
                    "cloudwatch:ListMetrics",
                    "cloudwatch:PutDashboard",
                    "cloudwatch:GetDashboard",
                    "cloudwatch:PutMetricAlarm",
                    "cloudwatch:DescribeAlarms",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                    "logs:DescribeLogGroups",
                    "logs:DescribeLogStreams",
                ],
                "Resource": "*",
            },
        ],
    }

    try:
        iam.create_role(
            RoleName="BankingMLEngineerRole",
            AssumeRolePolicyDocument=json.dumps(ml_engineer_trust),
            Description="ML Engineer role with banking compliance - deployment and CI/CD",
            Tags=[
                {"Key": "Environment", "Value": "MLOps"},
                {"Key": "Compliance", "Value": "Banking"},
                {"Key": "Team", "Value": "MLEngineering"},
                {"Key": "RoleType", "Value": "MLEngineer"},
            ],
        )
        print("   ✅ ML Engineer role created")
    except Exception as e:
        print(f"   ⚠️ Role may already exist: {str(e)}")

    iam.put_role_policy(
        RoleName="BankingMLEngineerRole",
        PolicyName="MLEngineerBankingPolicy",
        PolicyDocument=json.dumps(ml_engineer_policy),
    )
    print("   ✅ ML Engineer policy attached")

    print("\n📋 Creating Compliance Officer Role...")

    compliance_trust = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "sagemaker.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    }

    compliance_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:ListBucket"],
                "Resource": [
                    f"arn:aws:s3:::{buckets['governance']['name']}",
                    f"arn:aws:s3:::{buckets['governance']['name']}/*",
                    f"arn:aws:s3:::{buckets['audit']['name']}",
                    f"arn:aws:s3:::{buckets['audit']['name']}/*",
                    f"arn:aws:s3:::{buckets['monitoring']['name']}",
                    f"arn:aws:s3:::{buckets['monitoring']['name']}/*",
                ],
            },
            {
                "Effect": "Allow",
                "Action": ["sagemaker:Describe*", "sagemaker:List*", "sagemaker:Get*"],
                "Resource": "*",
            },
            {
                "Effect": "Allow",
                "Action": [
                    "cloudtrail:LookupEvents",
                    "cloudtrail:DescribeTrails",
                    "cloudtrail:GetTrailStatus",
                ],
                "Resource": "*",
            },
            {
                "Effect": "Allow",
                "Action": [
                    "kms:DescribeKey",
                    "kms:GetKeyPolicy",
                    "kms:ListKeys",
                    "kms:ListKeyPolicies",
                ],
                "Resource": "*",
            },
        ],
    }

    try:
        iam.create_role(
            RoleName="BankingComplianceOfficerRole",
            AssumeRolePolicyDocument=json.dumps(compliance_trust),
            Description="Compliance Officer role with banking compliance - read-only audit access",
            Tags=[
                {"Key": "Environment", "Value": "MLOps"},
                {"Key": "Compliance", "Value": "Banking"},
                {"Key": "Team", "Value": "Compliance"},
                {"Key": "RoleType", "Value": "ComplianceOfficer"},
            ],
        )
        print("   ✅ Compliance Officer role created")
    except Exception as e:
        print(f"   ⚠️ Role may already exist: {str(e)}")

    iam.put_role_policy(
        RoleName="BankingComplianceOfficerRole",
        PolicyName="ComplianceOfficerBankingPolicy",
        PolicyDocument=json.dumps(compliance_policy),
    )
    print("   ✅ Compliance Officer policy attached")

    print("\n📋 Creating Service Control Policy for Region Restriction...")

    region_restriction_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Deny",
                "Action": "*",
                "Resource": "*",
                "Condition": {"StringNotEquals": {"aws:RequestedRegion": "us-west-2"}},
            }
        ],
    }

    with open(CONFIG_DIR / "region_restriction_policy.json", "w", encoding="utf-8") as f:
        json.dump(region_restriction_policy, f, indent=2)
    print("   ✅ Region restriction policy saved for reference")

    roles = {
        "data_scientist": {
            "role_name": "BankingDataScientistRole",
            "arn": f"arn:aws:iam::{account_id}:role/BankingDataScientistRole",
        },
        "ml_engineer": {
            "role_name": "BankingMLEngineerRole",
            "arn": f"arn:aws:iam::{account_id}:role/BankingMLEngineerRole",
        },
        "compliance_officer": {
            "role_name": "BankingComplianceOfficerRole",
            "arn": f"arn:aws:iam::{account_id}:role/BankingComplianceOfficerRole",
        },
    }

    with open(CONFIG_DIR / "iam_roles.json", "w", encoding="utf-8") as f:
        json.dump(roles, f, indent=2)

    print("\n" + "=" * 60)
    print("✅ Banking IAM Roles Created!")
    print("\n📋 Role Summary:")
    for role_type, info in roles.items():
        print(f"   {role_type.upper()}: {info['arn']}")

    return roles


if __name__ == "__main__":
    create_banking_iam_roles()
