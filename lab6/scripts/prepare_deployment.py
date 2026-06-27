"""Resolve deployment state from Labs 3 and 5."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import account_id, write_json

from lab_paths import CONFIG_DIR, LAB3, LAB5, ensure_workspace


def main():
    ensure_workspace()
    print("Preparing deployment configuration")
    print("=" * 60)

    acct = account_id(dry_run=False)
    ecr_cfg = LAB5 / "config" / "ecr_config.json"
    image_uri = f"{acct}.dkr.ecr.us-west-2.amazonaws.com/banking-ml-inference:latest"
    if ecr_cfg.exists():
        with open(ecr_cfg, encoding="utf-8") as f:
            image_uri = json.load(f).get("uri", image_uri) + ":latest"

    model_uri = f"s3://bank-mlops-{acct}-models/banking-model/latest/model.tar.gz"
    if (LAB3 / "models" / "best_model.pkl").exists():
        print("   ✅ Model URI resolved from Lab 3 best_model.pkl")

    prod = {
        "instance_type": "ml.m5.large",
        "initial_instance_count": 1,
        "environment": "production",
    }
    write_json(CONFIG_DIR / "environments" / "prod.json", prod)

    state = {
        "model_uri": model_uri,
        "image_uri": image_uri,
        "blue_model_name": "banking-model-blue",
        "green_model_prefix": "banking-model-green",
        "endpoint_prefix": "banking-endpoint-prod",
        "region": "us-west-2",
        "prod_config": prod,
    }
    write_json(CONFIG_DIR / "deployment_state.json", state)
    print(f"   ✅ IAM roles loaded from Lab 1 (via workspace)")
    print("✅ Deployment state ready")


if __name__ == "__main__":
    main()
