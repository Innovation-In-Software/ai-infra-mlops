"""Delete Lab 1.1 SageMaker Studio domain so you can re-run create_sagemaker_studio.py."""
import argparse
import json
import time

import boto3

from lab_paths import CONFIG_DIR, ensure_workspace

USERS = (
    "DataScientist01",
    "DataScientist02",
    "MLEngineer01",
    "ComplianceOfficer01",
)


def find_domain_by_name(sagemaker, domain_name):
    token = None
    while True:
        params = {"MaxResults": 50}
        if token:
            params["NextToken"] = token
        response = sagemaker.list_domains(**params)
        for domain in response.get("Domains", []):
            if domain.get("DomainName") == domain_name:
                return domain
        token = response.get("NextToken")
        if not token:
            break
    return None


def load_domain_name():
    config_path = CONFIG_DIR / "sagemaker_studio.json"
    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("domain_name"):
            return data["domain_name"]

    account_id = boto3.client("sts").get_caller_identity()["Account"]
    return f"banking-mlops-domain-{account_id}"


def delete_user_apps(sagemaker, domain_id, user_name, dry_run=False):
    token = None
    while True:
        params = {
            "DomainIdEquals": domain_id,
            "UserProfileNameEquals": user_name,
            "MaxResults": 50,
        }
        if token:
            params["NextToken"] = token
        response = sagemaker.list_apps(**params)
        for app in response.get("Apps", []):
            app_type = app["AppType"]
            app_name = app["AppName"]
            status = app.get("Status", "")
            if dry_run:
                print(f"      would delete app: {user_name}/{app_type}/{app_name} ({status})")
                continue
            if status in ("Deleted", "Failed"):
                continue
            print(f"      deleting app: {user_name}/{app_type}/{app_name} ({status})")
            sagemaker.delete_app(
                DomainId=domain_id,
                UserProfileName=user_name,
                AppType=app_type,
                AppName=app_name,
            )
        token = response.get("NextToken")
        if not token:
            break


def wait_for_apps_gone(sagemaker, domain_id, user_name, max_wait=300, interval=10):
    wait_time = 0
    while wait_time < max_wait:
        response = sagemaker.list_apps(
            DomainIdEquals=domain_id,
            UserProfileNameEquals=user_name,
            MaxResults=50,
        )
        active = [
            a
            for a in response.get("Apps", [])
            if a.get("Status") not in ("Deleted", "Failed")
        ]
        if not active:
            return True
        time.sleep(interval)
        wait_time += interval
    return False


def list_user_profile_names(sagemaker, domain_id):
    names = []
    token = None
    while True:
        params = {"DomainIdEquals": domain_id, "MaxResults": 50}
        if token:
            params["NextToken"] = token
        response = sagemaker.list_user_profiles(**params)
        names.extend(p["UserProfileName"] for p in response.get("UserProfiles", []))
        token = response.get("NextToken")
        if not token:
            break
    return names


def wait_for_user_profiles_gone(sagemaker, domain_id, max_wait=900, interval=15):
    print("   waiting for user profiles to finish deleting...")
    wait_time = 0
    while wait_time < max_wait:
        remaining = list_user_profile_names(sagemaker, domain_id)
        if not remaining:
            print("   all user profiles removed")
            return True
        print(f"   still deleting: {', '.join(remaining)}... waiting {interval}s")
        time.sleep(interval)
        wait_time += interval
    print("   timed out waiting for user profile deletion")
    return False


def delete_domain_with_retry(sagemaker, domain_id, max_attempts=40, interval=15):
    for attempt in range(1, max_attempts + 1):
        try:
            sagemaker.delete_domain(
                DomainId=domain_id,
                RetentionPolicy={"HomeEfsFileSystem": "Delete"},
            )
            return True
        except sagemaker.exceptions.ResourceInUse:
            if attempt == max_attempts:
                raise
            print(
                f"   domain still in use, waiting {interval}s "
                f"({attempt}/{max_attempts})"
            )
            time.sleep(interval)
    return False


def delete_sagemaker_studio(dry_run=False):
    ensure_workspace()
    sagemaker = boto3.client("sagemaker", region_name="us-west-2")
    domain_name = load_domain_name()

    print("Delete Lab 1.1 SageMaker Studio")
    print("=" * 60)
    print(f"   domain name: {domain_name}")

    existing = find_domain_by_name(sagemaker, domain_name)
    if not existing:
        print("   skip (domain not found)")
        if not dry_run:
            config_path = CONFIG_DIR / "sagemaker_studio.json"
            if config_path.exists():
                config_path.write_text("{}\n", encoding="utf-8")
                print(f"   cleared: {config_path}")
        print("\n" + "=" * 60)
        print("Nothing to delete. Re-run: python scripts\\create_sagemaker_studio.py")
        return False

    domain_id = existing["DomainId"]
    print(f"   domain id: {domain_id}")

    profile_names = sorted(
        set(list_user_profile_names(sagemaker, domain_id) + list(USERS))
    )

    for user in profile_names:
        if dry_run:
            print(f"   would delete user profile: {user}")
            delete_user_apps(sagemaker, domain_id, user, dry_run=True)
            continue

        print(f"   cleaning apps for: {user}")
        delete_user_apps(sagemaker, domain_id, user)
        wait_for_apps_gone(sagemaker, domain_id, user)
        try:
            sagemaker.delete_user_profile(DomainId=domain_id, UserProfileName=user)
            print(f"   delete requested: {user}")
        except sagemaker.exceptions.ResourceNotFound:
            print(f"   skip (user not found): {user}")

    if dry_run:
        print(f"   would delete domain: {domain_id}")
        print("\n" + "=" * 60)
        print("Dry run — no resources deleted.")
        print("Re-run without --dry-run, then: python scripts\\create_sagemaker_studio.py")
        return True

    if not wait_for_user_profiles_gone(sagemaker, domain_id):
        print("\n" + "=" * 60)
        print("User profiles still deleting — wait a few minutes and re-run this script.")
        return False

    print(f"   deleting domain: {domain_id}")
    delete_domain_with_retry(sagemaker, domain_id)

    print("   waiting for domain deletion (up to 15 minutes)...")
    wait_time = 0
    max_wait = 900
    interval = 15
    while wait_time < max_wait:
        try:
            status = sagemaker.describe_domain(DomainId=domain_id)
            state = status.get("Status", "Unknown")
            if state in ("Deleted", "Failed"):
                break
            print(f"   status: {state}... waiting {interval}s")
        except sagemaker.exceptions.ResourceNotFound:
            print("   domain removed")
            break
        time.sleep(interval)
        wait_time += interval

    config_path = CONFIG_DIR / "sagemaker_studio.json"
    if config_path.exists():
        config_path.write_text("{}\n", encoding="utf-8")
        print(f"   cleared: {config_path}")

    print("\n" + "=" * 60)
    print("Done — SageMaker Studio deleted.")
    print("Re-run: python scripts\\create_sagemaker_studio.py")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Delete Lab 1.1 SageMaker Studio domain and user profiles"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted")
    args = parser.parse_args()
    delete_sagemaker_studio(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
