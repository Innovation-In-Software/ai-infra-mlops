"""Resolve deployment state from Labs 1, 3, and 5."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION, load_buckets, load_iam_role, write_json

from lab_paths import CONFIG_DIR, LAB3, LAB5, ensure_workspace


def main():
    ensure_workspace()
    print("Preparing deployment configuration")
    print("=" * 60)

    role_arn = load_iam_role("ml_engineer")
    buckets = load_buckets()
    models_bucket = buckets["models"]["name"]

    ecr_cfg_path = LAB5 / "config" / "ecr_config.json"
    image_uri = None
    if ecr_cfg_path.exists():
        with open(ecr_cfg_path, encoding="utf-8") as f:
            base = json.load(f).get("uri", "")
            image_uri = base if base.endswith(":latest") else f"{base}:latest"
    if not image_uri:
        print("   ❌ Missing Lab 5 ecr_config.json — complete Lab 5 Steps 6–7 first.")
        sys.exit(1)

    if not (LAB3 / "models" / "best_model.pkl").exists():
        print("   ❌ Missing Lab 3 best_model.pkl")
        sys.exit(1)
    print("   ✅ Model artifact found in Lab 3 workspace")

    model_uri = f"s3://{models_bucket}/banking-model/latest/model.tar.gz"
    prod = {
        "instance_type": "ml.m5.large",
        "initial_instance_count": 1,
        "environment": "production",
    }
    write_json(CONFIG_DIR / "environments" / "prod.json", prod)

    state = {
        "model_uri": model_uri,
        "image_uri": image_uri,
        "execution_role_arn": role_arn,
        "blue_model_name": "banking-model-blue",
        "green_model_name": "banking-model-green",
        "endpoint_prefix": "banking-endpoint-prod",
        "region": REGION,
        "prod_config": prod,
        "models_bucket": models_bucket,
    }
    write_json(CONFIG_DIR / "deployment_state.json", state)
    print(f"   ✅ IAM role: {role_arn}")
    print(f"   ✅ Image URI: {image_uri}")
    print("✅ Deployment state ready")


if __name__ == "__main__":
    main()
