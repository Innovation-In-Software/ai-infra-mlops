"""Prepare monitoring baseline and current sample data."""
import json
import shutil

import numpy as np
import pandas as pd
from lab_paths import CONFIG_DIR, DATA_DIR, LAB3, LAB6, ensure_workspace


def main():
    ensure_workspace()
    print("Preparing monitoring data and configuration")
    print("=" * 60)

    src = LAB3 / "data" / "X_train.csv"
    if src.exists():
        baseline = pd.read_csv(src)
        print(f"   ✅ Baseline data loaded from Lab 3: {len(baseline)} rows")
    else:
        rng = np.random.default_rng(42)
        baseline = pd.DataFrame({f"f{i}": rng.uniform(0, 1, 500) for i in range(8)})
        print(f"   ✅ Generated synthetic baseline: {len(baseline)} rows")

    current = baseline.copy()
    if "f0" in current.columns:
        current["f0"] = current["f0"] + np.random.default_rng(99).normal(0.05, 0.02, len(current))

    baseline.to_csv(DATA_DIR / "baseline_data.csv", index=False)
    current.to_csv(DATA_DIR / "current_data.csv", index=False)

    endpoint = "banking-endpoint-prod-demo"
    state_path = LAB6 / "config" / "deployment_state.json"
    if state_path.exists():
        with open(state_path, encoding="utf-8") as f:
            endpoint = json.load(f).get("endpoint_prefix", endpoint) + "-demo"

    state = {"endpoint_name": endpoint, "region": "us-west-2"}
    with open(CONFIG_DIR / "monitoring_state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    print(f"   ✅ baseline_data.csv / current_data.csv")
    print("✅ Monitoring data ready")


if __name__ == "__main__":
    main()
