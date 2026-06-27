"""Validate all components are correctly configured."""
import boto3
import json
from datetime import datetime

from lab_paths import CONFIG_DIR, RESULTS_DIR, ensure_workspace


def validate_environment():
    """
    Validate all components are correctly configured
    Generates compliance report
    """

    print("🔍 Validating Banking MLOps Environment")
    print("=" * 60)

    ensure_workspace()
    account_id = boto3.client("sts").get_caller_identity()["Account"]
    region = "us-west-2"

    validation_results = {
        "timestamp": datetime.utcnow().isoformat(),
        "account_id": account_id,
        "region": region,
        "checks": [],
    }

    def add_check(name, status, details):
        validation_results["checks"].append(
            {"name": name, "status": "PASS" if status else "FAIL", "details": details}
        )
        print(f"{'✅' if status else '❌'} {name}: {details}")

    print("\n📋 Validating KMS Keys...")
    try:
        kms = boto3.client("kms", region_name=region)
        with open(CONFIG_DIR / "kms_keys.json", "r", encoding="utf-8") as f:
            keys = json.load(f)

        for key_type in ["s3_key_id", "sm_key_id"]:
            key_id = keys.get(key_type)
            if key_id:
                response = kms.describe_key(KeyId=key_id)
                if response["KeyMetadata"]["KeyState"] == "Enabled":
                    add_check(f"KMS Key {key_type}", True, f"Enabled: {key_id}")
                else:
                    add_check(f"KMS Key {key_type}", False, f"Not enabled: {key_id}")
            else:
                add_check(f"KMS Key {key_type}", False, "Key ID not found")
    except Exception as e:
        add_check("KMS Keys", False, f"Error: {str(e)}")

    print("\n📋 Validating S3 Buckets...")
    try:
        s3 = boto3.client("s3", region_name=region)
        with open(CONFIG_DIR / "buckets.json", "r", encoding="utf-8") as f:
            buckets = json.load(f)

        for bucket_type, info in buckets.items():
            bucket_name = info["name"]
            try:
                s3.head_bucket(Bucket=bucket_name)
                encryption = s3.get_bucket_encryption(Bucket=bucket_name)
                algo = encryption["ServerSideEncryptionConfiguration"]["Rules"][0][
                    "ApplyServerSideEncryptionByDefault"
                ]["SSEAlgorithm"]
                if algo == "aws:kms":
                    add_check(
                        f"Bucket {bucket_type}",
                        True,
                        f"Exists and encrypted: {bucket_name}",
                    )
                else:
                    add_check(
                        f"Bucket {bucket_type}",
                        False,
                        f"Exists but not encrypted: {bucket_name}",
                    )
            except Exception as e:
                add_check(f"Bucket {bucket_type}", False, f"Not accessible: {str(e)}")
    except Exception as e:
        add_check("S3 Buckets", False, f"Error: {str(e)}")

    print("\n📋 Validating IAM Roles...")
    try:
        iam = boto3.client("iam")
        with open(CONFIG_DIR / "iam_roles.json", "r", encoding="utf-8") as f:
            roles = json.load(f)

        for role_type, info in roles.items():
            role_name = info["role_name"]
            try:
                iam.get_role(RoleName=role_name)
                add_check(f"Role {role_type}", True, f"Exists: {role_name}")
            except Exception as e:
                add_check(f"Role {role_type}", False, f"Not found: {str(e)}")
    except Exception as e:
        add_check("IAM Roles", False, f"Error: {str(e)}")

    print("\n📋 Validating SageMaker Studio...")
    try:
        sagemaker = boto3.client("sagemaker", region_name=region)
        with open(CONFIG_DIR / "sagemaker_studio.json", "r", encoding="utf-8") as f:
            studio = json.load(f)

        domain_id = studio.get("domain_id")
        if domain_id:
            response = sagemaker.describe_domain(DomainId=domain_id)
            if response["Status"] == "InService":
                add_check("SageMaker Studio", True, f"InService: {domain_id}")
            else:
                add_check("SageMaker Studio", False, f"Status: {response['Status']}")
        else:
            add_check("SageMaker Studio", False, "Domain ID not found")
    except Exception as e:
        add_check("SageMaker Studio", False, f"Error: {str(e)}")

    print("\n📋 Validating Audit Logging...")
    try:
        cloudtrail = boto3.client("cloudtrail", region_name=region)
        trails = cloudtrail.list_trails()
        trail_found = False
        for trail in trails["Trails"]:
            if "BankingMLOpsAuditTrail" in trail["Name"]:
                status = cloudtrail.get_trail_status(Name=trail["Name"])
                if status["IsLogging"]:
                    add_check("CloudTrail", True, f"Logging enabled: {trail['Name']}")
                    trail_found = True
                break
        if not trail_found:
            add_check("CloudTrail", False, "No banking audit trail found")
    except Exception as e:
        add_check("Audit Logging", False, f"Error: {str(e)}")

    print("\n📋 Generating Compliance Report...")

    total = len(validation_results["checks"])
    passes = sum(1 for check in validation_results["checks"] if check["status"] == "PASS")
    failures = total - passes
    compliance_score = (passes / total * 100) if total > 0 else 0

    validation_results["summary"] = {
        "total_checks": total,
        "passed": passes,
        "failed": failures,
        "compliance_score": compliance_score,
        "status": "COMPLIANT" if compliance_score == 100 else "PARTIALLY_COMPLIANT",
    }

    with open(RESULTS_DIR / "compliance_report.json", "w", encoding="utf-8") as f:
        json.dump(validation_results, f, indent=2)

    print("\n" + "=" * 60)
    print("📋 COMPLIANCE REPORT SUMMARY")
    print("=" * 60)
    print(f"Total Checks: {total}")
    print(f"Passed: {passes}")
    print(f"Failed: {failures}")
    print(f"Compliance Score: {compliance_score:.1f}%")
    print(f"Status: {validation_results['summary']['status']}")

    if failures > 0:
        print("\n❌ Failed Checks:")
        for check in validation_results["checks"]:
            if check["status"] == "FAIL":
                print(f"   - {check['name']}: {check['details']}")

    if compliance_score == 100:
        print("\n✅ ALL CHECKS PASSED! Environment is compliant.")
        print("   Proceed to Lab 1.2")
    else:
        print("\n⚠️ Some checks failed. Review and fix before proceeding.")
        print(f"   Check {RESULTS_DIR / 'compliance_report.json'} for details")

    return validation_results


if __name__ == "__main__":
    validate_environment()
