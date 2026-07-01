"""Push banking-ml-inference image to ECR (boto3 — no aws CLI required)."""
import base64
import json
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.course_common import REGION, docker_prefix, docker_run

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CONFIG = REPO_ROOT / "workspace" / "lab5" / "config" / "ecr_config.json"
IMAGE = "banking-ml-inference:latest"


def main():
    if not CONFIG.exists():
        print("   ❌ Run create_ecr_repo.py first")
        sys.exit(1)

    with open(CONFIG, encoding="utf-8") as f:
        uri = json.load(f)["uri"]
    target = f"{uri}:latest"

    print(f"   Logging in to ECR ({REGION})...")
    try:
        auth = boto3.client("ecr", region_name=REGION).get_authorization_token()
    except ClientError as exc:
        print(f"   ❌ ECR login failed: {exc}")
        sys.exit(1)

    data = auth["authorizationData"][0]
    registry = data["proxyEndpoint"].replace("https://", "")
    user_pass = base64.b64decode(data["authorizationToken"]).decode()
    username, password = user_pass.split(":", 1)

    docker_prefix()

    login = docker_run(
        ["login", "--username", username, "--password-stdin", registry],
        input=password.encode(),
        capture_output=True,
    )
    if login.returncode != 0:
        print(login.stderr.decode(errors="replace"))
        print("   ❌ docker login failed")
        sys.exit(1)

    docker_run(["tag", IMAGE, target], check=True)
    push = docker_run(["push", target], capture_output=True, text=True)
    if push.returncode != 0:
        print(push.stderr or push.stdout)
        print("   ❌ docker push failed")
        sys.exit(1)

    print("   ✅ Login to ECR succeeded")
    print(f"   ✅ Pushed: {target}")
    print("✅ Image push complete")


if __name__ == "__main__":
    main()
