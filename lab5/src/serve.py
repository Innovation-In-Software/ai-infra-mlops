"""Minimal Flask inference service for banking model."""
import joblib
from flask import Flask, jsonify, request

app = Flask(__name__)
model = joblib.load("/app/model.pkl")


@app.get("/ping")
def ping():
    return jsonify({"status": "ok"})


@app.post("/invocations")
def invocations():
    payload = request.get_json(force=True)
    features = payload.get("features", [0.0] * 8)
    pred = model.predict([features])[0]
    prob = float(model.predict_proba([features])[0].max())
    return jsonify({"prediction": int(pred), "risk_score": prob})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
