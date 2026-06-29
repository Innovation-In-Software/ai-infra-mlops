"""Validate Lab 6."""
import json
import sys

from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 6")
    print("=" * 60)
    ok = True
    required = [
        "deployment_state.json",
        "blue_green_plan.json",
        "staging_deployment.json",
        "test_staging.json",
        "production_deployment.json",
        "deployment_report.json",
    ]
    for name in required:
        p = CONFIG_DIR / name
        if p.exists():
            print(f"   ✅ config: {name}")
        else:
            print(f"   ❌ Missing: {name}")
            ok = False

    staging_path = CONFIG_DIR / "staging_deployment.json"
    if staging_path.exists():
        staging = json.loads(staging_path.read_text(encoding="utf-8"))
        if staging.get("dry_run"):
            print("   ❌ Staging was dry-run only — re-run deploy_staging.py without --dry-run")
            ok = False
        elif staging.get("endpoint_status") != "InService" and not staging.get("reused"):
            print(f"   ❌ Staging endpoint status: {staging.get('endpoint_status', 'UNKNOWN')}")
            ok = False

    test_path = CONFIG_DIR / "test_staging.json"
    if test_path.exists():
        test = json.loads(test_path.read_text(encoding="utf-8"))
        if test.get("source") != "sagemaker-runtime" and not test.get("dry_run"):
            print("   ❌ Staging test did not invoke SageMaker runtime")
            ok = False

    print("\n" + "=" * 60)
    if ok:
        print("Prerequisites OK — proceed to Lab 7")
    else:
        print("Complete Lab 6 steps (lab6/STEPS.md).")
        sys.exit(1)


if __name__ == "__main__":
    main()
