"""Validate Lab 5."""
import json
import sys
from lab_paths import CONFIG_DIR, MODELS_DIR, VALIDATION_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 5")
    print("=" * 60)
    ok = (MODELS_DIR / "best_model.pkl").exists()
    if ok:
        print("   ✅ models: best_model.pkl")
    if (VALIDATION_DIR / "container_deployment_manifest.json").exists():
        print("   ✅ Container compliance: PASS")
    print("Prerequisites OK — proceed to Lab 6" if ok else "Run prepare_artifacts first.")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
