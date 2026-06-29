"""Minimal Flask inference service for banking model."""
import sys

import joblib
from flask import Flask, jsonify, request

app = Flask(__name__)
_model = None


def get_model():
    global _model
    if _model is None:
        _model = joblib.load("/app/model.pkl")
    return _model


@app.get("/ping")
def ping():
    try:
        get_model()
        return jsonify({"status": "ok"})
    except Exception as exc:
        print(f"ping failed: {exc}", file=sys.stderr, flush=True)
        return jsonify({"status": "error", "detail": str(exc)}), 503


@app.post("/invocations")
def invocations():
    payload = request.get_json(force=True)
    model = get_model()
    n_features = int(model.n_features_in_)
    features = payload.get("features")
    if features is None:
        features = [0.0] * n_features
    if len(features) != n_features:
        return (
            jsonify(
                {
                    "error": f"Expected {n_features} features (Lab 3 trained model), got {len(features)}",
                }
            ),
            400,
        )
    pred = model.predict([features])[0]
    prob = float(model.predict_proba([features])[0].max())
    return jsonify({"prediction": int(pred), "risk_score": prob})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)
