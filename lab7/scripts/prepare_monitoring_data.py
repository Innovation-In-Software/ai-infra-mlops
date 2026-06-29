"""Prepare monitoring baseline and current sample data."""
import json

import numpy as np
import pandas as pd

from lab_paths import CONFIG_DIR, DATA_DIR, LAB3, ensure_workspace
from monitoring_helpers import resolve_endpoint_name


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

    endpoint, env = resolve_endpoint_name()
    if not endpoint:
        print("   ❌ No Lab 6 endpoint found — complete Lab 6 deploy steps first.")
        raise SystemExit(1)

    state = {"endpoint_name": endpoint, "environment": env, "region": "us-west-2", "source": "lab6"}
    with open(CONFIG_DIR / "monitoring_state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    print(f"   ✅ Monitoring endpoint: {endpoint} ({env})")
    print("   ✅ baseline_data.csv / current_data.csv")
    print("✅ Monitoring data ready")


if __name__ == "__main__":
    main()
