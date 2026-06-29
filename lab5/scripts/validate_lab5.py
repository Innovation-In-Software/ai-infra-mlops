"""Validate Lab 5."""
import json
import sys

from lab_paths import CONFIG_DIR, LAB3, MODELS_DIR, VALIDATION_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 5")
    print("=" * 60)
    ok = True

    prerequisites = [
        (LAB3 / "models" / "best_model.pkl", "Lab 3 best_model.pkl"),
    ]
    outputs = [
        (MODELS_DIR / "best_model.pkl", "models: best_model.pkl"),
        (MODELS_DIR / "preprocessor.pkl", "models: preprocessor.pkl"),
        (CONFIG_DIR / "ecr_config.json", "config: ecr_config.json"),
        (CONFIG_DIR / "scan_report.json", "config: scan_report.json"),
        (VALIDATION_DIR / "container_deployment_manifest.json", "validation: container_deployment_manifest.json"),
        (VALIDATION_DIR / "container_test.json", "validation: container_test.json"),
    ]

    for path, label in prerequisites:
        if path.exists():
            print(f"   ✅ {label}")
        else:
            print(f"   ❌ Missing: {label}")
            ok = False

    for path, label in outputs:
        if path.exists():
            print(f"   ✅ {label}")
        else:
            print(f"   ❌ Missing: {label}")
            ok = False

    manifest = VALIDATION_DIR / "container_deployment_manifest.json"
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        compliance = data.get("compliance", "UNKNOWN")
        print(f"   ✅ Container compliance: {compliance}")
        if compliance not in ("PASS", "REVIEW"):
            print("   ❌ Run Step 8 (scan_container.py) until scan completes")
            ok = False

    scan_path = CONFIG_DIR / "scan_report.json"
    if scan_path.exists():
        scan = json.loads(scan_path.read_text(encoding="utf-8"))
        if scan.get("source") != "ecr":
            print("   ❌ scan_report.json is not from ECR — re-run Step 8")
            ok = False
        elif scan.get("scan_status") in ("PENDING", "TIMED_OUT"):
            print("   ❌ ECR scan still pending — wait and re-run Step 8")
            ok = False

    (CONFIG_DIR / "lab5_validation.json").write_text(
        json.dumps({"lab": 5, "valid": ok}, indent=2),
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    if ok:
        print("Prerequisites OK — proceed to Lab 6")
    else:
        print("Complete Labs 3 and 5 steps first (lab5/STEPS.md).")
        sys.exit(1)


if __name__ == "__main__":
    main()
