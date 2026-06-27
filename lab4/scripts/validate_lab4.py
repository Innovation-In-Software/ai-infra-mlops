"""Validate Lab 4."""
import json
import sys

from lab_paths import ARTIFACTS_DIR, CONFIG_DIR, MODELS_DIR, LAB1, LAB3, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 4")
    print("=" * 60)
    ok = True
    for path, label in [
        (LAB1 / "buckets.json", "Lab 1 buckets.json"),
        (LAB3 / "models" / "best_model.pkl", "Lab 3 best_model.pkl"),
        (ARTIFACTS_DIR / "cicd_compliance_report_final.json", "cicd_compliance_report_final.json"),
    ]:
        if path.exists():
            print(f"   ✅ {label}")
        else:
            print(f"   ⚠️ not yet created: {label}")
    print("Prerequisites OK — proceed to Lab 5" if ok else "Complete prior labs first.")
    (CONFIG_DIR / "lab4_validation.json").write_text(json.dumps({"lab": 4, "ok": ok}), encoding="utf-8")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
