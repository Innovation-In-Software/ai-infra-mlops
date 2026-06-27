"""Train baseline banking risk models."""
import json
from datetime import datetime, timezone

import joblib
import pandas as pd
from lab_paths import CONFIG_DIR, DATA_DIR, MODELS_DIR, ensure_workspace
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from xgboost import XGBClassifier


def _metrics(y_true, y_pred, y_prob):
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred)),
        "auc": float(roc_auc_score(y_true, y_prob)),
    }


def main():
    ensure_workspace()
    print("🏦 Training Banking Risk Models")
    print("=" * 60)

    X_train = pd.read_csv(DATA_DIR / "X_train.csv")
    y_train = pd.read_csv(DATA_DIR / "y_train.csv").iloc[:, 0]
    X_test = pd.read_csv(DATA_DIR / "X_test.csv")
    y_test = pd.read_csv(DATA_DIR / "y_test.csv").iloc[:, 0]

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(
            n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42, eval_metric="logloss"
        ),
    }

    all_results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        prob = model.predict_proba(X_test)[:, 1]
        pred = (prob >= 0.5).astype(int)
        metrics = _metrics(y_test, pred, prob)
        path = MODELS_DIR / f"{name.lower()}_model.pkl"
        joblib.dump(model, path)
        all_results[name] = {"metrics": metrics, "model_path": str(path)}
        print(f"   ✅ {name} — AUC: {metrics['auc']:.2f}")

    best = max(all_results.items(), key=lambda x: x[1]["metrics"]["auc"])[0]
    joblib.dump(joblib.load(MODELS_DIR / f"{best.lower()}_model.pkl"), MODELS_DIR / "best_model.pkl")

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "training_samples": len(X_train),
        "all_results": all_results,
        "best_by_auc": best,
    }
    with open(CONFIG_DIR / "training_results.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("✅ Model training complete")


if __name__ == "__main__":
    main()
