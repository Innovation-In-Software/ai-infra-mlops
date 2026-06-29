"""Test container health and inference on EC2."""
import json
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import sample_features_for_model

from lab_paths import MODELS_DIR, VALIDATION_DIR, ensure_workspace

CONTAINER = "banking-ml-test"
IMAGE = "banking-ml-inference:latest"
PING_URL = "http://127.0.0.1:8080/ping"
INVOKE_URL = "http://127.0.0.1:8080/invocations"


def _container_running():
    result = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", CONTAINER],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() == "true"


def _container_logs():
    result = subprocess.run(
        ["docker", "logs", CONTAINER],
        capture_output=True,
        text=True,
    )
    return (result.stdout + result.stderr).strip()


def _wait_for_ping(timeout_sec=90):
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        if not _container_running():
            return False
        try:
            with urllib.request.urlopen(PING_URL, timeout=3) as resp:
                if resp.status == 200:
                    return True
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            time.sleep(1)
    return False


def _fail(message):
    logs = _container_logs()
    subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)
    print(f"   ❌ {message}")
    if logs:
        print("   --- docker logs ---")
        for line in logs.splitlines()[-20:]:
            print(f"   {line}")
    print("   Re-run Step 4 (build_container.sh) after fixing errors above.")
    sys.exit(1)


def main():
    ensure_workspace()
    print("🧪 Container Inference Test")
    print("=" * 60)

    if not shutil.which("docker"):
        print("   ❌ Docker not found — complete Lab 0 Step 19.")
        sys.exit(1)

    subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)
    run = subprocess.run(
        ["docker", "run", "-d", "-p", "8080:8080", "--name", CONTAINER, IMAGE],
        capture_output=True,
        text=True,
    )
    if run.returncode != 0:
        print(f"   ❌ Failed to start container: {run.stderr.strip()}")
        print("   Run Step 4 (build_container.sh) first.")
        sys.exit(1)

    print("   ... waiting for /ping (model load may take up to 60s)")
    if not _wait_for_ping():
        _fail("Health check timed out on /ping — container may have exited or model failed to load")

    model_path = MODELS_DIR / "best_model.pkl"
    if not model_path.exists():
        print(f"   ❌ Missing {model_path} — run Step 3 (prepare_artifacts.py) first.")
        sys.exit(1)
    sample = sample_features_for_model(model_path)
    print(f"   ... sample inference with {len(sample)} features (matches Lab 3 model)")

    req = urllib.request.Request(
        INVOKE_URL,
        data=json.dumps({"features": sample}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        _fail(f"Inference request failed: {exc}")

    risk = float(body.get("risk_score", 0))
    print("   ✅ Health check: 200 OK")
    print(f"   ✅ Sample prediction: risk_score={risk:.2f}")

    subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)

    result = {"health": 200, "sample_prediction": {"risk_score": round(risk, 4)}}
    with open(VALIDATION_DIR / "container_test.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print("✅ Container tests passed")


if __name__ == "__main__":
    main()
