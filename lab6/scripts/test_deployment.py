"""Test deployed SageMaker endpoint."""
import argparse
import json

from lab_paths import CONFIG_DIR, ensure_workspace
from sm_deploy import invoke_endpoint


def _load_endpoint(environment):
    if environment == "staging":
        path = CONFIG_DIR / "staging_deployment.json"
    else:
        path = CONFIG_DIR / "production_deployment.json"
    if not path.exists():
        print(f"   ❌ Missing {path.name} — deploy {environment} first.")
        raise SystemExit(1)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    endpoint = data.get("endpoint")
    if not endpoint:
        print(f"   ❌ No endpoint name in {path.name}")
        raise SystemExit(1)
    return endpoint, data.get("dry_run", False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--environment", default="staging")
    args = parser.parse_args()
    ensure_workspace()
    print(f"🧪 Endpoint Tests ({args.environment})")
    print("=" * 60)

    endpoint_name, cfg_dry = _load_endpoint(args.environment)
    dry_run = args.dry_run or cfg_dry
    results = invoke_endpoint(endpoint_name, dry_run=dry_run)
    results["environment"] = args.environment
    results["dry_run"] = dry_run

    with open(CONFIG_DIR / f"test_{args.environment}.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"   ✅ Health: {results['health']}")
    print(f"   ✅ Sample transaction latency: {results['latency_ms']}ms")
    print(f"   ✅ Error rate: {results.get('error_rate', 0)}%")
    print("✅ Staging tests passed" if args.environment == "staging" else "✅ Tests passed")


if __name__ == "__main__":
    main()
