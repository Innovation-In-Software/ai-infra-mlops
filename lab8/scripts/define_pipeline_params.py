"""Define SageMaker pipeline parameters."""
import json
import shutil
from datetime import datetime, timezone

from lab_paths import CONFIG_DIR, DATA_DIR, LAB2, ensure_workspace


def main():
    ensure_workspace()
    src = LAB2 / "data" / "engineered_banking_data.csv"
    if src.exists():
        shutil.copy2(src, DATA_DIR / "banking_data.csv")
        print(f"   ✅ Input data from Lab 2")
    params = {
        "region": "us-west-2",
        "instance_type": "ml.m5.large",
        "pipeline_name": "banking-ml-pipeline",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(CONFIG_DIR / "pipeline_params.json", "w", encoding="utf-8") as f:
        json.dump(params, f, indent=2)
    print("✅ Pipeline parameters defined")


if __name__ == "__main__":
    main()
