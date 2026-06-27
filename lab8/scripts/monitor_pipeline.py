"""Monitor pipeline step status."""
import argparse
import json
from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()
    steps = {
        "data-validation": "Succeeded",
        "xgboost-training": "Succeeded",
        "model-evaluation": "Succeeded",
        "model-registry": "Succeeded",
    }
    with open(CONFIG_DIR / "pipeline_monitor.json", "w", encoding="utf-8") as f:
        json.dump(steps, f, indent=2)
    for name, status in steps.items():
        print(f"   {name:<22} ✅ {status}")
    print("✅ All steps succeeded (simulated)")


if __name__ == "__main__":
    main()
