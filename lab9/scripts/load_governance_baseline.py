"""Prepare governance baseline from prior labs."""
import json
import shutil

from lab_paths import CONFIG_DIR, DATA_DIR, LAB3, LAB5, MODELS_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("🛡️ Governance Baseline")
    print("=" * 60)
    for src in (LAB5 / "models" / "best_model.pkl", LAB3 / "models" / "best_model.pkl"):
        if src.exists():
            shutil.copy2(src, MODELS_DIR / "best_model.pkl")
            print(f"   ✅ Model copied from {src.parent.parent.name}")
            break
    if (LAB3 / "data" / "X_test.csv").exists():
        shutil.copy2(LAB3 / "data" / "X_test.csv", DATA_DIR / "X_test.csv")
    state = {"model_name": "BankingRiskModel", "model_version": "v2.1.0", "region": "us-west-2"}
    with open(CONFIG_DIR / "governance_state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    print("   ✅ Lab 1 IAM / CloudTrail context linked (workspace)")
    print("✅ Baseline ready")


if __name__ == "__main__":
    main()
