"""Upload Lab 3 train CSVs to S3 for SageMaker Training."""
import json
import sys
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from scripts.course_common import write_json

from lab_paths import CONFIG_DIR, LAB1_CONFIG, LAB3, ensure_workspace


def main():
    ensure_workspace()
    print("📤 Upload training data for SageMaker")
    print("=" * 60)

    for path, label in [
        (LAB3 / "data" / "X_train.csv", "X_train.csv"),
        (LAB3 / "data" / "y_train.csv", "y_train.csv"),
    ]:
        if not path.exists():
            print(f"   ❌ Missing {label} — complete Lab 3 Step 4 first.")
            sys.exit(1)

    with open(LAB1_CONFIG / "buckets.json", encoding="utf-8") as f:
        buckets = json.load(f)
    processed = buckets["processed"]["name"]
    prefix = "training/sagemaker-lab3b/"
    account_id = boto3.client("sts").get_caller_identity()["Account"]
    s3 = boto3.client("s3", region_name="us-west-2")

    uris = {}
    for name in ("X_train.csv", "y_train.csv"):
        src = LAB3 / "data" / name
        key = f"{prefix}{name}"
        s3.upload_file(str(src), processed, key)
        uri = f"s3://{processed}/{key}"
        uris[name] = uri
        print(f"   ✅ Uploaded: {uri}")

    config = {
        "account_id": account_id,
        "train_prefix": f"s3://{processed}/{prefix}",
        "X_train_uri": uris["X_train.csv"],
        "y_train_uri": uris["y_train.csv"],
    }
    write_json(CONFIG_DIR / "s3_training_data.json", config)
    print("✅ Training data ready in S3")


if __name__ == "__main__":
    main()
