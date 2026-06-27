"""Copy model artifacts from Lab 3 for container build."""
import json
import shutil

import joblib
import numpy as np
import pandas as pd
from lab_paths import CONFIG_DIR, LAB3, MODELS_DIR, ensure_workspace
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


def main():
    ensure_workspace()
    print("Preparing container artifacts from Lab 3")
    print("=" * 60)

    src_model = LAB3 / "models" / "best_model.pkl"
    if src_model.exists():
        shutil.copy2(src_model, MODELS_DIR / "best_model.pkl")
        for name in ("preprocessor.pkl", "feature_names.json"):
            src = LAB3 / "config" / name
            if src.exists():
                shutil.copy2(src, MODELS_DIR / name if name.endswith(".pkl") else CONFIG_DIR / name)
        print(f"   ✅ Copied: best_model.pkl")
    else:
        print("   Lab 3 model not found; creating demo model.")
        rng = np.random.default_rng(42)
        X = pd.DataFrame({f"f{i}": rng.uniform(0, 1, 200) for i in range(8)})
        y = (X.mean(axis=1) > 0.5).astype(int)
        scaler = StandardScaler()
        model = RandomForestClassifier(n_estimators=30, random_state=42)
        model.fit(scaler.fit_transform(X), y)
        joblib.dump(model, MODELS_DIR / "best_model.pkl")
        joblib.dump(scaler, MODELS_DIR / "preprocessor.pkl")
        with open(CONFIG_DIR / "feature_names.json", "w", encoding="utf-8") as f:
            json.dump(list(X.columns), f, indent=2)

    print("\nArtifacts ready for Docker build.")


if __name__ == "__main__":
    main()
