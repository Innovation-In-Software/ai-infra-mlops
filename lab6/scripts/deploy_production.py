"""Production blue-green deployment on SageMaker."""
import argparse
import json
from datetime import datetime, timezone

from lab_paths import CONFIG_DIR, ensure_workspace
from sm_deploy import create_blue_green_endpoint, load_deployment_state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()

    state = load_deployment_state()
    suffix = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
    endpoint_name = f"{state['endpoint_prefix']}-{suffix}"
    endpoint_config_name = f"banking-epcfg-prod-{suffix}"
    blue_model = f"{state['blue_model_name']}-{suffix}"
    green_model = f"{state['green_model_name']}-{suffix}"

    report = create_blue_green_endpoint(
        endpoint_name=endpoint_name,
        blue_model_name=blue_model,
        green_model_name=green_model,
        endpoint_config_name=endpoint_config_name,
        image_uri=state["image_uri"],
        dry_run=args.dry_run,
    )
    report["dry_run"] = args.dry_run
    report["blue_model"] = blue_model
    report["green_model"] = green_model
    report["endpoint_config"] = endpoint_config_name

    with open(CONFIG_DIR / "production_deployment.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    p = "[dry-run] " if args.dry_run else ""
    print(f"   {p}✅ Production endpoint: {endpoint_name}")
    print("✅ Production deployment complete" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
