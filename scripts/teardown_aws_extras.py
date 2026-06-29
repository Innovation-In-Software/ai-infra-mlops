#!/usr/bin/env python3
"""Delete course AWS resources not covered by lab1/lab2 delete scripts."""
from __future__ import annotations

import json
import time
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

REPO = Path(__file__).resolve().parents[1]
REGION = "us-west-2"

BANKING_IAM_ROLES = (
    "BankingDataScientistRole",
    "BankingMLEngineerRole",
    "BankingComplianceOfficerRole",
    "BankingLab4bPipelineRole",
    "BankingLab4bCodeBuildRole",
    "EC2MLOpsLabRole",
)
INSTANCE_PROFILES = ("EC2MLOpsLabProfile",)
CLOUDWATCH_ALARMS = (
    "BankingDataDriftAlarm",
    "banking-ml-high-latency",
    "banking-ml-error-rate",
    "banking-ml-drift-severity",
)
CLOUDWATCH_DASHBOARDS = ("Banking-MLOps-Audit-Dashboard",)
SAGEMAKER_EXPERIMENTS = ("banking-risk-experiments",)
SAGEMAKER_PIPELINES = ("banking-ml-pipeline",)
ECR_REPOS = ("banking-ml-inference",)
EC2_KEY_PAIRS = ("ai-mlops-instructor", "mlops-lab-key")
EC2_SECURITY_GROUPS = ("mlops-lab-sg",)
SNS_TOPIC_SUFFIXES = ("banking-drift-alerts",)


def _ok(msg: str) -> None:
    print(f"   ✅ {msg}")


def _skip(msg: str) -> None:
    print(f"   ⚠️ {msg}")


def _dry(msg: str, dry_run: bool) -> None:
    prefix = "   would " if dry_run else "   "
    print(f"{prefix}{msg}")


def delete_iam_role(iam, role_name: str, dry_run: bool = False) -> None:
    if dry_run:
        _dry(f"delete IAM role: {role_name}", True)
        return
    try:
        for policy in iam.list_attached_role_policies(RoleName=role_name).get(
            "AttachedPolicies", []
        ):
            iam.detach_role_policy(RoleName=role_name, PolicyArn=policy["PolicyArn"])
        for policy_name in iam.list_role_policies(RoleName=role_name).get(
            "PolicyNames", []
        ):
            iam.delete_role_policy(RoleName=role_name, PolicyName=policy_name)
        iam.delete_role(RoleName=role_name)
        _ok(f"Deleted IAM role: {role_name}")
    except iam.exceptions.NoSuchEntityException:
        _skip(f"IAM role not found: {role_name}")
    except Exception as exc:
        _skip(f"IAM role {role_name}: {exc}")


def delete_instance_profile(iam, profile_name: str, dry_run: bool = False) -> None:
    if dry_run:
        _dry(f"delete instance profile: {profile_name}", True)
        return
    try:
        roles = iam.get_instance_profile(InstanceProfileName=profile_name)[
            "InstanceProfile"
        ]["Roles"]
        for role in roles:
            iam.remove_role_from_instance_profile(
                InstanceProfileName=profile_name, RoleName=role["RoleName"]
            )
        iam.delete_instance_profile(InstanceProfileName=profile_name)
        _ok(f"Deleted instance profile: {profile_name}")
    except iam.exceptions.NoSuchEntityException:
        _skip(f"Instance profile not found: {profile_name}")
    except Exception as exc:
        _skip(f"Instance profile {profile_name}: {exc}")


def delete_cloudwatch_alarms(cw, dry_run: bool = False) -> None:
    existing = {
        a["AlarmName"]
        for a in cw.describe_alarms().get("MetricAlarms", [])
    }
    to_delete = [name for name in CLOUDWATCH_ALARMS if name in existing]
    # Also catch any alarm starting with Banking or banking-ml
    for name in sorted(existing):
        if name.startswith(("Banking", "banking-ml")) and name not in to_delete:
            to_delete.append(name)
    if not to_delete:
        _skip("No CloudWatch alarms to delete")
        return
    if dry_run:
        for name in to_delete:
            _dry(f"delete alarm: {name}", True)
        return
    cw.delete_alarms(AlarmNames=to_delete)
    _ok(f"Deleted CloudWatch alarms: {', '.join(to_delete)}")


def delete_cloudwatch_dashboards(cw, dry_run: bool = False) -> None:
    for name in CLOUDWATCH_DASHBOARDS:
        if dry_run:
            _dry(f"delete dashboard: {name}", True)
            continue
        try:
            cw.delete_dashboards(DashboardNames=[name])
            _ok(f"Deleted dashboard: {name}")
        except Exception as exc:
            _skip(f"Dashboard {name}: {exc}")


def delete_sagemaker_experiment(sm, experiment_name: str, dry_run: bool = False) -> None:
    try:
        sm.describe_experiment(ExperimentName=experiment_name)
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ResourceNotFound":
            _skip(f"Experiment not found: {experiment_name}")
            return
        raise

    trials = sm.list_trials(ExperimentName=experiment_name).get("TrialSummaries", [])
    for trial in trials:
        trial_name = trial["TrialName"]
        components = sm.list_trial_components(TrialName=trial_name).get(
            "TrialComponentSummaries", []
        )
        for comp in components:
            cname = comp["TrialComponentName"]
            if dry_run:
                _dry(f"delete trial component: {cname}", True)
                continue
            try:
                sm.disassociate_trial_component(
                    TrialComponentName=cname, TrialName=trial_name
                )
            except ClientError:
                pass
            try:
                sm.delete_trial_component(TrialComponentName=cname)
            except ClientError as exc:
                _skip(f"Trial component {cname}: {exc}")
        if dry_run:
            _dry(f"delete trial: {trial_name}", True)
        else:
            try:
                sm.delete_trial(TrialName=trial_name)
            except ClientError as exc:
                _skip(f"Trial {trial_name}: {exc}")

    if dry_run:
        _dry(f"delete experiment: {experiment_name}", True)
    else:
        sm.delete_experiment(ExperimentName=experiment_name)
        _ok(f"Deleted experiment: {experiment_name}")


def delete_sagemaker_endpoints(sm, dry_run: bool = False) -> None:
    names = [
        e["EndpointName"]
        for e in sm.list_endpoints().get("Endpoints", [])
        if e["EndpointName"].startswith("banking-")
    ]
    if not names:
        _skip("No banking SageMaker endpoints")
        return
    for name in names:
        if dry_run:
            _dry(f"delete endpoint: {name}", True)
            continue
        try:
            sm.delete_endpoint(EndpointName=name)
            _ok(f"Deleted endpoint: {name}")
        except ClientError as exc:
            _skip(f"Endpoint {name}: {exc}")


def delete_sagemaker_pipelines(sm, dry_run: bool = False) -> None:
    for pipeline_name in SAGEMAKER_PIPELINES:
        try:
            sm.describe_pipeline(PipelineName=pipeline_name)
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceNotFound":
                _skip(f"Pipeline not found: {pipeline_name}")
                continue
            raise
        if dry_run:
            _dry(f"delete pipeline: {pipeline_name}", True)
            continue
        try:
            sm.delete_pipeline(PipelineName=pipeline_name)
            _ok(f"Deleted pipeline: {pipeline_name}")
        except ClientError as exc:
            _skip(f"Pipeline {pipeline_name}: {exc}")


def delete_ecr_repos(ecr, dry_run: bool = False) -> None:
    for repo in ECR_REPOS:
        if dry_run:
            _dry(f"delete ECR repo: {repo}", True)
            continue
        try:
            ecr.delete_repository(repositoryName=repo, force=True)
            _ok(f"Deleted ECR repository: {repo}")
        except ecr.exceptions.RepositoryNotFoundException:
            _skip(f"ECR repo not found: {repo}")
        except Exception as exc:
            _skip(f"ECR {repo}: {exc}")


def delete_sns_topics(sns, account_id: str, dry_run: bool = False) -> None:
    topics = sns.list_topics().get("Topics", [])
    for topic in topics:
        arn = topic["TopicArn"]
        name = arn.split(":")[-1]
        if not any(name.endswith(s) or s in name for s in SNS_TOPIC_SUFFIXES):
            if not name.startswith("banking"):
                continue
        if dry_run:
            _dry(f"delete SNS topic: {name}", True)
            continue
        try:
            sns.delete_topic(TopicArn=arn)
            _ok(f"Deleted SNS topic: {name}")
        except Exception as exc:
            _skip(f"SNS {name}: {exc}")


def _kms_key_ids_from_workspace() -> set[str]:
    ids: set[str] = set()
    config = REPO / "workspace" / "lab1" / "config" / "kms_keys.json"
    if config.exists():
        with open(config, encoding="utf-8") as f:
            data = json.load(f)
        for key in ("s3_key_id", "sm_key_id"):
            if data.get(key):
                ids.add(data[key])
    return ids


def delete_kms_keys(kms, pending_days: int = 7, dry_run: bool = False) -> None:
    key_ids = _kms_key_ids_from_workspace()
    paginator = kms.get_paginator("list_keys")
    for page in paginator.paginate():
        for item in page["Keys"]:
            kid = item["KeyId"]
            try:
                meta = kms.describe_key(KeyId=kid)["KeyMetadata"]
            except ClientError:
                continue
            if meta.get("KeyManager") != "CUSTOMER":
                continue
            desc = meta.get("Description") or ""
            if kid not in key_ids and "Banking" not in desc:
                continue
            state = meta.get("KeyState")
            if state == "PendingDeletion":
                _skip(f"KMS key already pending deletion: {kid}")
                continue
            if dry_run:
                _dry(f"schedule KMS key deletion ({pending_days}d): {kid}", True)
                continue
            for alias in kms.list_aliases(KeyId=kid).get("Aliases", []):
                aname = alias["AliasName"]
                if aname.startswith("alias/aws/"):
                    continue
                try:
                    kms.delete_alias(AliasName=aname)
                except ClientError:
                    pass
            try:
                kms.schedule_key_deletion(
                    KeyId=kid, PendingWindowInDays=pending_days
                )
                _ok(f"Scheduled KMS key deletion ({pending_days}d): {kid}")
            except ClientError as exc:
                _skip(f"KMS {kid}: {exc}")


def delete_ec2_key_pairs(ec2, dry_run: bool = False) -> None:
    existing = {k["KeyName"] for k in ec2.describe_key_pairs().get("KeyPairs", [])}
    for name in EC2_KEY_PAIRS:
        if name not in existing:
            continue
        if dry_run:
            _dry(f"delete key pair: {name}", True)
            continue
        ec2.delete_key_pair(KeyName=name)
        _ok(f"Deleted key pair: {name}")
    for name in sorted(existing):
        if "mlops" in name.lower() and name not in EC2_KEY_PAIRS:
            if dry_run:
                _dry(f"delete key pair: {name}", True)
            else:
                ec2.delete_key_pair(KeyName=name)
                _ok(f"Deleted key pair: {name}")


def delete_security_groups(ec2, dry_run: bool = False) -> None:
    for sg_name in EC2_SECURITY_GROUPS:
        try:
            resp = ec2.describe_security_groups(
                Filters=[{"Name": "group-name", "Values": [sg_name]}]
            )
            groups = resp.get("SecurityGroups", [])
        except ClientError as exc:
            _skip(f"Security group lookup {sg_name}: {exc}")
            continue
        if not groups:
            _skip(f"Security group not found: {sg_name}")
            continue
        sg_id = groups[0]["GroupId"]
        if dry_run:
            _dry(f"delete security group: {sg_name} ({sg_id})", True)
            continue
        try:
            ec2.delete_security_group(GroupId=sg_id)
            _ok(f"Deleted security group: {sg_name}")
        except ClientError as exc:
            _skip(f"Security group {sg_name}: {exc}")


def terminate_lab_ec2_instances(ec2, dry_run: bool = False) -> None:
    """Terminate running/stopped instances tagged or named *mlops*."""
    instances = []
    for state in ("running", "stopped", "pending", "stopping"):
        resp = ec2.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": [state]}]
        )
        for res in resp.get("Reservations", []):
            for inst in res.get("Instances", []):
                name = ""
                for tag in inst.get("Tags", []):
                    if tag["Key"] == "Name":
                        name = tag["Value"]
                        break
                if "mlops" in name.lower():
                    instances.append((inst["InstanceId"], name, state))

    if not instances:
        _skip("No running/stopped mlops EC2 instances to terminate")
        return
    for iid, name, state in instances:
        if dry_run:
            _dry(f"terminate instance: {name} ({iid}, {state})", True)
            continue
        ec2.terminate_instances(InstanceIds=[iid])
        _ok(f"Terminating instance: {name} ({iid})")


def cleanup_aws_extras(
    *,
    region: str = REGION,
    dry_run: bool = False,
    terminate_ec2: bool = False,
    kms_pending_days: int = 7,
) -> None:
    """Run extended AWS cleanup for all course labs."""
    print("\n📋 Extended AWS cleanup (IAM, KMS, alarms, SageMaker, EC2, …)")
    print("=" * 60)

    session = boto3.Session(region_name=region)
    account_id = session.client("sts").get_caller_identity()["Account"]
    iam = session.client("iam")
    cw = session.client("cloudwatch", region_name=region)
    sm = session.client("sagemaker", region_name=region)
    ecr = session.client("ecr", region_name=region)
    sns = session.client("sns", region_name=region)
    kms = session.client("kms", region_name=region)
    ec2 = session.client("ec2", region_name=region)

    delete_cloudwatch_alarms(cw, dry_run=dry_run)
    delete_cloudwatch_dashboards(cw, dry_run=dry_run)

    for experiment in SAGEMAKER_EXPERIMENTS:
        delete_sagemaker_experiment(sm, experiment, dry_run=dry_run)

    delete_sagemaker_endpoints(sm, dry_run=dry_run)
    delete_sagemaker_pipelines(sm, dry_run=dry_run)
    delete_ecr_repos(ecr, dry_run=dry_run)
    delete_sns_topics(sns, account_id, dry_run=dry_run)

    for profile in INSTANCE_PROFILES:
        delete_instance_profile(iam, profile, dry_run=dry_run)
    for role in BANKING_IAM_ROLES:
        delete_iam_role(iam, role, dry_run=dry_run)

    delete_kms_keys(kms, pending_days=kms_pending_days, dry_run=dry_run)
    delete_ec2_key_pairs(ec2, dry_run=dry_run)
    delete_security_groups(ec2, dry_run=dry_run)

    if terminate_ec2:
        terminate_lab_ec2_instances(ec2, dry_run=dry_run)

    print("\n" + "=" * 60)
    if dry_run:
        print("Dry run — no extended AWS resources deleted.")
    else:
        print("✅ Extended AWS cleanup complete.")
        print(
            f"   KMS keys scheduled for deletion in {kms_pending_days} days "
            "(AWS minimum pending window)."
        )
        if not terminate_ec2:
            print(
                "   EC2 instances were kept. Re-run with --terminate-ec2 to "
                "terminate *mlops* instances."
            )


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Extended MLOps course AWS cleanup")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--terminate-ec2",
        action="store_true",
        help="Terminate running/stopped EC2 instances with 'mlops' in the Name tag",
    )
    parser.add_argument(
        "--kms-pending-days",
        type=int,
        default=7,
        choices=range(7, 31),
        metavar="N",
        help="KMS pending deletion window (7–30 days, default 7)",
    )
    parser.add_argument("--region", default=REGION)
    args = parser.parse_args()
    cleanup_aws_extras(
        region=args.region,
        dry_run=args.dry_run,
        terminate_ec2=args.terminate_ec2,
        kms_pending_days=args.kms_pending_days,
    )


if __name__ == "__main__":
    main()
