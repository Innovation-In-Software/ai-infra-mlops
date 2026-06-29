"""Validate Lab 8."""
import json
import sys

from lab_paths import CONFIG_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 8")
    print("=" * 60)
    ok = True
    required = [
        "pipeline_params.json",
        "pipeline_registration.json",
        "pipeline_execution.json",
        "pipeline_monitor.json",
        "model_registry.json",
    ]
    for name in required:
        p = CONFIG_DIR / name
        if p.exists():
            print(f"   ✅ config: {name}")
        else:
            print(f"   ❌ Missing: {name}")
            ok = False

    exec_path = CONFIG_DIR / "pipeline_execution.json"
    if exec_path.exists():
        data = json.loads(exec_path.read_text(encoding="utf-8"))
        if data.get("source") == "sagemaker" and data.get("status") != "Succeeded":
            print(f"   ❌ Pipeline status: {data.get('status')}")
            ok = False
        if data.get("dry_run"):
            print("   ❌ Pipeline was dry-run only")
            ok = False

    reg = CONFIG_DIR / "model_registry.json"
    if reg.exists():
        data = json.loads(reg.read_text(encoding="utf-8"))
        if not data.get("model_package_arn") and not data.get("dry_run"):
            print("   ❌ Model package not registered in SageMaker")
            ok = False

    print("\n" + "=" * 60)
    if ok:
        print("Prerequisites OK — proceed to Lab 9")
    else:
        print("Complete Lab 8 steps (lab8/STEPS.md).")
        sys.exit(1)


if __name__ == "__main__":
    main()
