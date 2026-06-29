"""SageMaker endpoint helpers for Lab 6."""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION, load_iam_role, wait_for_status, write_json

from lab_paths import CONFIG_DIR, ensure_workspace

INSTANCE_TYPE = "ml.m5.large"
SAMPLE_FEATURES = [0.12, 0.45, 0.33, 0.08, 0.91, 0.27, 0.55, 0.19]


def load_deployment_state():
    path = CONFIG_DIR / "deployment_state.json"
    if not path.exists():
        print("   ❌ Missing deployment_state.json — run prepare_deployment.py first.")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _endpoint_in_service(sm, endpoint_name):
    try:
        resp = sm.describe_endpoint(EndpointName=endpoint_name)
        return resp.get("EndpointStatus") == "InService", resp
    except ClientError:
        return False, None


def create_single_variant_endpoint(
    *,
    endpoint_name,
    model_name,
    endpoint_config_name,
    image_uri,
    variant_name,
    dry_run=False,
    initial_weight=1,
):
    ensure_workspace()
    if dry_run:
        return {
            "endpoint": endpoint_name,
            "model": model_name,
            "endpoint_config": endpoint_config_name,
            "variant": variant_name,
            "dry_run": True,
        }

    in_service, existing = _endpoint_in_service(boto3.client("sagemaker", region_name=REGION), endpoint_name)
    if in_service:
        print(f"   ✅ Endpoint already InService: {endpoint_name}")
        return {
            "endpoint": endpoint_name,
            "endpoint_arn": existing["EndpointArn"],
            "endpoint_status": "InService",
            "reused": True,
        }

    role_arn = load_iam_role("ml_engineer")
    sm = boto3.client("sagemaker", region_name=REGION)

    try:
        sm.describe_model(ModelName=model_name)
        print(f"   ✅ Model exists: {model_name}")
    except ClientError:
        sm.create_model(
            ModelName=model_name,
            PrimaryContainer={"Image": image_uri},
            ExecutionRoleArn=role_arn,
        )
        print(f"   ✅ Created model: {model_name}")

    try:
        sm.describe_endpoint_config(EndpointConfigName=endpoint_config_name)
        print(f"   ✅ Endpoint config exists: {endpoint_config_name}")
    except ClientError:
        sm.create_endpoint_config(
            EndpointConfigName=endpoint_config_name,
            ProductionVariants=[
                {
                    "VariantName": variant_name,
                    "ModelName": model_name,
                    "InitialInstanceCount": 1,
                    "InstanceType": INSTANCE_TYPE,
                    "InitialVariantWeight": initial_weight,
                }
            ],
        )
        print(f"   ✅ Created endpoint config: {endpoint_config_name}")

    try:
        sm.describe_endpoint(EndpointName=endpoint_name)
        print(f"   ... endpoint {endpoint_name} exists; waiting for InService")
    except ClientError:
        sm.create_endpoint(EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name)
        print(f"   ✅ Creating endpoint: {endpoint_name} (typically 5–10 min)")

    resp = wait_for_status(
        lambda: sm.describe_endpoint(EndpointName=endpoint_name),
        "EndpointStatus",
        {"InService"},
        timeout_sec=1200,
        label=f"endpoint {endpoint_name}",
    )
    return {
        "endpoint": endpoint_name,
        "endpoint_arn": resp["EndpointArn"],
        "endpoint_status": resp["EndpointStatus"],
        "model": model_name,
        "endpoint_config": endpoint_config_name,
        "variant": variant_name,
        "instance_type": INSTANCE_TYPE,
        "region": REGION,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def create_blue_green_endpoint(
    *,
    endpoint_name,
    blue_model_name,
    green_model_name,
    endpoint_config_name,
    image_uri,
    dry_run=False,
):
    ensure_workspace()
    if dry_run:
        return {
            "endpoint": endpoint_name,
            "variants": [blue_model_name, green_model_name],
            "dry_run": True,
        }

    sm = boto3.client("sagemaker", region_name=REGION)
    in_service, existing = _endpoint_in_service(sm, endpoint_name)
    if in_service:
        print(f"   ✅ Production endpoint already InService: {endpoint_name}")
        return {
            "endpoint": endpoint_name,
            "endpoint_arn": existing["EndpointArn"],
            "endpoint_status": "InService",
            "variants": ["banking-model-blue", "banking-model-green"],
            "reused": True,
        }

    role_arn = load_iam_role("ml_engineer")
    for model_name in (blue_model_name, green_model_name):
        try:
            sm.describe_model(ModelName=model_name)
        except ClientError:
            sm.create_model(
                ModelName=model_name,
                PrimaryContainer={"Image": image_uri},
                ExecutionRoleArn=role_arn,
            )
            print(f"   ✅ Created model: {model_name}")

    try:
        sm.describe_endpoint_config(EndpointConfigName=endpoint_config_name)
    except ClientError:
        sm.create_endpoint_config(
            EndpointConfigName=endpoint_config_name,
            ProductionVariants=[
                {
                    "VariantName": "banking-model-blue",
                    "ModelName": blue_model_name,
                    "InitialInstanceCount": 1,
                    "InstanceType": INSTANCE_TYPE,
                    "InitialVariantWeight": 100,
                },
                {
                    "VariantName": "banking-model-green",
                    "ModelName": green_model_name,
                    "InitialInstanceCount": 1,
                    "InstanceType": INSTANCE_TYPE,
                    "InitialVariantWeight": 0,
                },
            ],
        )
        print(f"   ✅ Created blue-green endpoint config: {endpoint_config_name}")

    try:
        sm.describe_endpoint(EndpointName=endpoint_name)
    except ClientError:
        sm.create_endpoint(EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name)
        print(f"   ✅ Creating production endpoint: {endpoint_name}")

    resp = wait_for_status(
        lambda: sm.describe_endpoint(EndpointName=endpoint_name),
        "EndpointStatus",
        {"InService"},
        timeout_sec=1200,
        label=f"endpoint {endpoint_name}",
    )
    return {
        "endpoint": endpoint_name,
        "endpoint_arn": resp["EndpointArn"],
        "endpoint_status": resp["EndpointStatus"],
        "variants": ["banking-model-blue", "banking-model-green"],
        "autoscaling": False,
        "instance_type": INSTANCE_TYPE,
        "region": REGION,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def invoke_endpoint(endpoint_name, dry_run=False):
    if dry_run:
        return {"health": "PASS", "latency_ms": 45, "error_rate": 0.0, "dry_run": True}

    runtime = boto3.client("sagemaker-runtime", region_name=REGION)
    payload = json.dumps({"features": SAMPLE_FEATURES})
    start = time.time()
    try:
        runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="application/json",
            Body=payload,
        )
    except Exception as exc:
        print(f"   ❌ Invoke failed: {exc}")
        sys.exit(1)
    latency_ms = round((time.time() - start) * 1000, 1)
    return {
        "health": "PASS",
        "latency_ms": latency_ms,
        "error_rate": 0.0,
        "endpoint": endpoint_name,
        "source": "sagemaker-runtime",
    }


def update_traffic_weights(endpoint_name, blue_weight, green_weight, dry_run=False):
    if dry_run:
        return {"blue": blue_weight, "green": green_weight, "dry_run": True}
    sm = boto3.client("sagemaker", region_name=REGION)
    sm.update_endpoint_weights(
        EndpointName=endpoint_name,
        DesiredWeightsAndCapacities=[
            {"VariantName": "banking-model-blue", "DesiredWeight": int(blue_weight)},
            {"VariantName": "banking-model-green", "DesiredWeight": int(green_weight)},
        ],
    )
    return {"blue": blue_weight, "green": green_weight, "endpoint": endpoint_name}
