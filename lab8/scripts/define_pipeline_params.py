"""Define SageMaker pipeline parameters and upload input data to S3."""
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION, load_buckets, write_json

from lab_paths import CONFIG_DIR, DATA_DIR, LAB2, ensure_workspace


def main():
    ensure_workspace()
    src = LAB2 / "data" / "engineered_banking_data.csv"
    if src.exists():
        shutil.copy2(src, DATA_DIR / "banking_data.csv")
        print("   ✅ Input data from Lab 2")
    elif not (DATA_DIR / "banking_data.csv").exists():
        print("   ❌ Missing Lab 2 engineered_banking_data.csv")
        sys.exit(1)

    buckets = load_buckets()
    bucket = buckets["processed"]["name"]
    key = "lab8-pipeline/input/banking_data.csv"
    input_s3_uri = f"s3://{bucket}/{key}"

    s3 = boto3.client("s3", region_name=REGION)
    s3.upload_file(str(DATA_DIR / "banking_data.csv"), bucket, key)
    print(f"   ✅ Uploaded input to {input_s3_uri}")

    params = {
        "region": REGION,
        "instance_type": "ml.t3.medium",
        "pipeline_name": "banking-ml-pipeline",
        "input_s3_uri": input_s3_uri,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    write_json(CONFIG_DIR / "pipeline_params.json", params)
    print("✅ Pipeline parameters defined")


if __name__ == "__main__":
    main()
