# SageMaker training entry point (Random Forest on Lab 3 features)
import argparse
import os
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def _read_train_dir(train_dir: Path):
    x_path = train_dir / "X_train.csv"
    y_path = train_dir / "y_train.csv"
    if not x_path.exists():
        raise FileNotFoundError(f"Missing {x_path}")
    if not y_path.exists():
        raise FileNotFoundError(f"Missing {y_path}")
    X = pd.read_csv(x_path)
    y = pd.read_csv(y_path).iloc[:, 0]
    return X, y


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR", "/opt/ml/model"))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN", "/opt/ml/input/data/train"))
    args = parser.parse_args()

    X, y = _read_train_dir(Path(args.train))
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X, y)
    out = Path(args.model_dir)
    out.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out / "model.joblib")
    print(f"Model saved to {out / 'model.joblib'} ({len(X)} rows)")
