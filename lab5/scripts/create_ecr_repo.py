"""Create ECR repository config."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import account_id, write_json

from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()
    acct = account_id(args.dry_run)
    print("📦 ECR Repository")
    print("=" * 60)
    repo_name = "banking-ml-inference"
    if not args.dry_run:
        import boto3

        ecr = boto3.client("ecr", region_name="us-west-2")
        try:
            ecr.create_repository(
                repositoryName=repo_name,
                imageScanningConfiguration={"scanOnPush": True},
                encryptionConfiguration={"encryptionType": "KMS"},
            )
            print(f"   ✅ Created ECR repository: {repo_name}")
        except ecr.exceptions.RepositoryAlreadyExistsException:
            print(f"   ✅ Repository already exists: {repo_name}")
    cfg = {
        "repository": "banking-ml-inference",
        "encryption": "KMS",
        "scan_on_push": True,
        "uri": f"{acct}.dkr.ecr.us-west-2.amazonaws.com/banking-ml-inference",
    }
    write_json(CONFIG_DIR / "ecr_config.json", cfg)
    print(f"   ✅ Repository: {cfg['repository']}")
    print("   ✅ Encryption: KMS")
    print("   ✅ Scan on push: enabled")
    print("✅ ECR repository ready")


if __name__ == "__main__":
    main()
