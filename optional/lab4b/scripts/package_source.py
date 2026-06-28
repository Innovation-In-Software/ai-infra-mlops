"""Zip Lab 4b source and upload to S3 for CodePipeline."""
import json
import sys
import zipfile
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from scripts.course_common import write_json

from lab_paths import CONFIG_DIR, LAB1_CONFIG, ROOT, ensure_workspace


def main():
    ensure_workspace()
    print("📦 Package pipeline source for S3")
    print("=" * 60)

    with open(LAB1_CONFIG / "buckets.json", encoding="utf-8") as f:
        buckets = json.load(f)
    models_bucket = buckets["models"]["name"]
    key = "cicd/lab4b/source.zip"
    zip_path = CONFIG_DIR / "source.zip"
    source_dir = ROOT / "source"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in source_dir.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(source_dir).as_posix())

    s3 = boto3.client("s3", region_name="us-west-2")
    s3.upload_file(str(zip_path), models_bucket, key)
    uri = f"s3://{models_bucket}/{key}"
    print(f"   ✅ Uploaded: {uri}")

    write_json(
        CONFIG_DIR / "pipeline_source.json",
        {"bucket": models_bucket, "key": key, "uri": uri},
    )
    print("✅ Source artifact ready for CodePipeline")


if __name__ == "__main__":
    main()
