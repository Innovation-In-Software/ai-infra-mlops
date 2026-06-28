#!/usr/bin/env python3
"""Create EC2MLOpsLabRole + EC2MLOpsLabProfile for optional Lab 0 instance profile."""
from __future__ import annotations

import json
import sys
import time

import boto3
from botocore.exceptions import ClientError

ROLE_NAME = "EC2MLOpsLabRole"
PROFILE_NAME = "EC2MLOpsLabProfile"
MANAGED_POLICY = "arn:aws:iam::aws:policy/PowerUserAccess"

TRUST_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole",
        }
    ],
}


def main() -> int:
    iam = boto3.client("iam")
    account = boto3.client("sts").get_caller_identity()["Account"]
    print("EC2 lab instance profile setup")
    print("=" * 50)
    print(f"Account: {account}")

    try:
        iam.get_role(RoleName=ROLE_NAME)
        print(f"   Role exists: {ROLE_NAME}")
    except iam.exceptions.NoSuchEntityException:
        iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(TRUST_POLICY),
            Description="EC2 lab instance role for MLOps course",
        )
        print(f"   Created role: {ROLE_NAME}")

    try:
        iam.attach_role_policy(RoleName=ROLE_NAME, PolicyArn=MANAGED_POLICY)
        print(f"   Attached: PowerUserAccess")
    except ClientError as exc:
        if "EntityAlreadyExists" in str(exc) or "LimitExceeded" in str(exc):
            print(f"   Policy already attached (or limit): {ROLE_NAME}")
        else:
            raise

    try:
        iam.get_instance_profile(InstanceProfileName=PROFILE_NAME)
        print(f"   Instance profile exists: {PROFILE_NAME}")
    except iam.exceptions.NoSuchEntityException:
        iam.create_instance_profile(InstanceProfileName=PROFILE_NAME)
        print(f"   Created instance profile: {PROFILE_NAME}")
        time.sleep(10)

    profiles = iam.get_instance_profile(InstanceProfileName=PROFILE_NAME)
    roles = profiles["InstanceProfile"].get("Roles", [])
    if not any(r["RoleName"] == ROLE_NAME for r in roles):
        iam.add_role_to_instance_profile(
            InstanceProfileName=PROFILE_NAME,
            RoleName=ROLE_NAME,
        )
        print(f"   Linked {ROLE_NAME} -> {PROFILE_NAME}")
        time.sleep(10)
    else:
        print(f"   Role already linked to profile")

    print("\nDone. In EC2 Launch instance -> Advanced details -> IAM instance profile:")
    print(f"   Select: {PROFILE_NAME}")
    print("   Or leave None and use aws configure on EC2 (Step 17).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
