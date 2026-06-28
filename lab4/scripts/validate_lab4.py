"""Validate Lab 4."""
import json
import sys

from lab_paths import ARTIFACTS_DIR, CONFIG_DIR, LAB1, LAB3, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 4")
    print("=" * 60)
    ok = True

    prerequisites = [
        (LAB1 / "buckets.json", "Lab 1 buckets.json"),
        (LAB3 / "models" / "best_model.pkl", "Lab 3 best_model.pkl"),
    ]
    outputs = [
        (CONFIG_DIR / "compliance_gates.json", "config: compliance_gates.json"),
        (CONFIG_DIR / "codepipeline_config.json", "config: codepipeline_config.json"),
        (ARTIFACTS_DIR / "pipeline_run_simulation.json", "artifacts: pipeline_run_simulation.json"),
        (ARTIFACTS_DIR / "cicd_compliance_report_final.json", "cicd_compliance_report_final.json"),
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
            print(f"   ⚠️ not yet created: {label}")

    (CONFIG_DIR / "lab4_validation.json").write_text(
        json.dumps({"lab": 4, "prerequisites_ok": ok}, indent=2),
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    if ok:
        print("Prerequisites OK — proceed to Lab 5")
    else:
        print("Complete Labs 1 and 3 first (lab4/STEPS.md).")
        sys.exit(1)


if __name__ == "__main__":
    main()
