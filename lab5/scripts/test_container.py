"""Test container health and inference on EC2."""
import json
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

from lab_paths import VALIDATION_DIR, ensure_workspace

CONTAINER = "banking-ml-test"
IMAGE = "banking-ml-inference:latest"


def _wait_for_ping(timeout_sec=30):
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        try:
            with urllib.request.urlopen("http://localhost:8080/ping", timeout=1) as resp:
                if resp.status == 200:
                    return True
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.5)
    return False


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

    if not _wait_for_ping():
        subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)
        print("   ❌ Health check timed out on http://localhost:8080/ping")
        sys.exit(1)

    req = urllib.request.Request(
        "http://localhost:8080/invocations",
        data=json.dumps({"features": [0.1] * 8}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        body = json.loads(resp.read().decode())

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
