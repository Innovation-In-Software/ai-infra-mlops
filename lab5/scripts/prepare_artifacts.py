"""Copy model artifacts from Lab 3 for container build."""
import shutil
import sys

from lab_paths import CONFIG_DIR, LAB3, MODELS_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("📦 Preparing container artifacts from Lab 3")
    print("=" * 60)

    src_model = LAB3 / "models" / "best_model.pkl"
    if not src_model.exists():
        print("   ❌ Lab 3 model not found — complete Lab 3 Step 8 first.")
        sys.exit(1)

    shutil.copy2(src_model, MODELS_DIR / "best_model.pkl")
    print("   ✅ Copied: best_model.pkl")
    for src_name, dst in [
        ("preprocessor.pkl", MODELS_DIR / "preprocessor.pkl"),
        ("feature_metadata.json", CONFIG_DIR / "feature_metadata.json"),
    ]:
        src = LAB3 / "config" / src_name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"   ✅ Copied: {src_name}")
        else:
            print(f"   ❌ Missing Lab 3 config: {src_name}")
            sys.exit(1)

    print("✅ Artifacts ready for Docker build")


if __name__ == "__main__":
    main()
