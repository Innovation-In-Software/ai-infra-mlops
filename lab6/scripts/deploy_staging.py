"""Deploy staging endpoint on SageMaker."""
import argparse
import json
from datetime import datetime, timezone

from lab_paths import CONFIG_DIR, ensure_workspace
from sm_deploy import create_single_variant_endpoint, load_deployment_state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_workspace()

    state = load_deployment_state()
    suffix = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
    endpoint_name = f"banking-endpoint-staging-{suffix}"
    model_name = f"banking-model-staging-{suffix}"
    endpoint_config_name = f"banking-epcfg-staging-{suffix}"

    result = create_single_variant_endpoint(
        endpoint_name=endpoint_name,
        model_name=model_name,
        endpoint_config_name=endpoint_config_name,
        image_uri=state["image_uri"],
        variant_name="staging",
        dry_run=args.dry_run,
    )
    cfg = {**result, "environment": "staging", "dry_run": args.dry_run}
    with open(CONFIG_DIR / "staging_deployment.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    p = "[dry-run] " if args.dry_run else ""
    print(f"   {p}✅ Staging endpoint: {endpoint_name}")
    print("✅ Staging deployment complete" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
