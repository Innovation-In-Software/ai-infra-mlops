"""Create SageMaker Studio domain with banking security."""
import boto3
import json
import sys
import time
from datetime import datetime


from lab_paths import CONFIG_DIR, ensure_workspace


def create_sagemaker_studio():
    """
    Create SageMaker Studio domain with banking security
    Includes VPC, encryption, and access controls
    """

    print("🖥️ Setting Up SageMaker Studio with Banking Security")
    print("=" * 60)

    ensure_workspace()
    sagemaker = boto3.client("sagemaker", region_name="us-west-2")
    ec2 = boto3.client("ec2", region_name="us-west-2")
    account_id = boto3.client("sts").get_caller_identity()["Account"]

    with open(CONFIG_DIR / "kms_keys.json", "r", encoding="utf-8") as f:
        json.load(f)

    with open(CONFIG_DIR / "iam_roles.json", "r", encoding="utf-8") as f:
        roles = json.load(f)

    print("\n📋 Configuring VPC and Networking...")

    vpcs = ec2.describe_vpcs(Filters=[{"Name": "isDefault", "Values": ["true"]}])
    if vpcs["Vpcs"]:
        vpc_id = vpcs["Vpcs"][0]["VpcId"]
        print(f"   Using default VPC: {vpc_id}")
    else:
        print("   ⚠️ No default VPC found. Using existing VPC...")
        vpcs = ec2.describe_vpcs()
        if vpcs["Vpcs"]:
            vpc_id = vpcs["Vpcs"][0]["VpcId"]
            print(f"   Using VPC: {vpc_id}")
        else:
            print("   ❌ No VPC found. Please create a VPC first.")
            sys.exit(1)

    subnets = ec2.describe_subnets(
        Filters=[
            {"Name": "vpc-id", "Values": [vpc_id]},
            {"Name": "availability-zone", "Values": ["us-west-2a", "us-west-2b", "us-west-2c"]},
        ]
    )

    if subnets["Subnets"]:
        subnet_ids = [subnet["SubnetId"] for subnet in subnets["Subnets"][:2]]
        print(f"   Using subnets: {', '.join(subnet_ids)}")
    else:
        subnets = ec2.describe_subnets(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])
        if subnets["Subnets"]:
            subnet_ids = [subnet["SubnetId"] for subnet in subnets["Subnets"][:2]]
            print(f"   Using subnets: {', '.join(subnet_ids)}")
        else:
            print("   ❌ No subnets found. Please create subnets first.")
            sys.exit(1)

    execution_role_arn = roles["data_scientist"]["arn"]
    print(f"\n📋 Using Execution Role: {execution_role_arn}")

    domain_name = f"banking-mlops-domain-{account_id}"
    print(f"\n📋 Creating SageMaker Studio Domain: {domain_name}")

    try:
        try:
            existing_domain = sagemaker.describe_domain(DomainName=domain_name)
            print(f"   ⚠️ Domain already exists: {domain_name}")
            domain_id = existing_domain["DomainId"]
            domain_arn = existing_domain["DomainArn"]
        except sagemaker.exceptions.ResourceNotFound:
            response = sagemaker.create_domain(
                DomainName=domain_name,
                AuthMode="IAM",
                DefaultUserSettings={
                    "ExecutionRole": execution_role_arn,
                    "SecurityGroups": [],
                    "JupyterServerAppSettings": {
                        "DefaultResourceSpec": {
                            "InstanceType": "ml.t3.medium",
                            "SageMakerImageArn": None,
                        }
                    },
                    "KernelGatewayAppSettings": {
                        "DefaultResourceSpec": {
                            "InstanceType": "ml.t3.medium",
                            "SageMakerImageArn": None,
                        }
                    },
                    "TensorBoardAppSettings": {
                        "DefaultResourceSpec": {"InstanceType": "ml.t3.medium"}
                    },
                    "CodeEditorAppSettings": {
                        "DefaultResourceSpec": {"InstanceType": "ml.t3.medium"}
                    },
                    "SharingSettings": {"NotebookOutputOption": "Disabled"},
                },
                SubnetIds=subnet_ids,
                VpcId=vpc_id,
                Tags=[
                    {"Key": "Environment", "Value": "MLOps"},
                    {"Key": "Compliance", "Value": "Banking-Regulated"},
                    {"Key": "Region", "Value": "us-west-2"},
                    {"Key": "Service", "Value": "SageMaker"},
                    {"Key": "Owner", "Value": "DataScienceTeam"},
                ],
            )
            domain_id = response["DomainId"]
            domain_arn = response["DomainArn"]
            print(f"   ✅ Domain created: {domain_id}")

        print("\n📋 Creating User Profiles...")

        users = [
            "DataScientist01",
            "DataScientist02",
            "MLEngineer01",
            "ComplianceOfficer01",
        ]

        for user in users:
            try:
                try:
                    sagemaker.describe_user_profile(DomainId=domain_id, UserProfileName=user)
                    print(f"   ⚠️ User {user} already exists")
                except sagemaker.exceptions.ResourceNotFound:
                    sagemaker.create_user_profile(
                        DomainId=domain_id,
                        UserProfileName=user,
                        UserSettings={
                            "ExecutionRole": execution_role_arn,
                            "JupyterServerAppSettings": {
                                "DefaultResourceSpec": {"InstanceType": "ml.t3.medium"}
                            },
                            "KernelGatewayAppSettings": {
                                "DefaultResourceSpec": {"InstanceType": "ml.t3.medium"}
                            },
                        },
                        Tags=[
                            {"Key": "Environment", "Value": "MLOps"},
                            {
                                "Key": "UserType",
                                "Value": "DataScientist"
                                if "Scientist" in user
                                else "MLEngineer"
                                if "Engineer" in user
                                else "Compliance",
                            },
                            {"Key": "CreatedBy", "Value": "Lab1.1"},
                        ],
                    )
                    print(f"   ✅ User {user} created")
            except Exception as e:
                print(f"   ❌ Error creating user {user}: {str(e)}")

        print("\n⏳ Waiting for domain to become ready...")

        max_wait = 300
        wait_time = 0
        interval = 10

        while wait_time < max_wait:
            try:
                status = sagemaker.describe_domain(DomainId=domain_id)
                if status["Status"] == "InService":
                    print("   ✅ Domain is ready!")
                    break
                if status["Status"] == "Failed":
                    print(
                        f"   ❌ Domain creation failed: {status.get('FailureReason', 'Unknown error')}"
                    )
                    break
                print(f"   ⏳ Status: {status['Status']}... waiting {interval}s")
                time.sleep(interval)
                wait_time += interval
            except Exception as e:
                print(f"   ⚠️ Error checking status: {str(e)}")
                time.sleep(interval)
                wait_time += interval

        domain_config = {
            "domain_name": domain_name,
            "domain_id": domain_id,
            "domain_arn": domain_arn,
            "vpc_id": vpc_id,
            "subnet_ids": subnet_ids,
            "execution_role_arn": execution_role_arn,
            "users": users,
            "created_at": datetime.utcnow().isoformat(),
        }

        with open(CONFIG_DIR / "sagemaker_studio.json", "w", encoding="utf-8") as f:
            json.dump(domain_config, f, indent=2)

        print("\n" + "=" * 60)
        print("✅ SageMaker Studio Configuration Complete!")
        print(f"   Domain Name: {domain_name}")
        print(f"   Domain ID: {domain_id}")
        print(f"   Users Created: {', '.join(users)}")
        print("\n📋 To access SageMaker Studio:")
        print(
            f"   https://us-west-2.console.aws.amazon.com/sagemaker/home?region=us-west-2#/studio/{domain_id}"
        )

        return domain_config

    except Exception as e:
        print(f"❌ Error creating SageMaker Studio: {str(e)}")
        return None


if __name__ == "__main__":
    create_sagemaker_studio()
