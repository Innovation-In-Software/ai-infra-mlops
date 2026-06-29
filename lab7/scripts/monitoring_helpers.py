"""Resolve monitoring endpoint from Lab 6 deployment configs."""
import json

from lab_paths import CONFIG_DIR, LAB6


def resolve_endpoint_name():
    for name in ("production_deployment.json", "staging_deployment.json"):
        path = LAB6 / "config" / name
        if path.exists():
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            endpoint = data.get("endpoint")
            if endpoint and not data.get("dry_run"):
                return endpoint, name.replace("_deployment.json", "")
    return None, None


def load_monitoring_state():
    path = CONFIG_DIR / "monitoring_state.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    endpoint, env = resolve_endpoint_name()
    if not endpoint:
        return None
    return {"endpoint_name": endpoint, "environment": env, "region": "us-west-2"}
