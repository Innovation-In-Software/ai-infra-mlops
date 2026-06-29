"""Validate Lab 9."""
import json
import sys

from lab_paths import CONFIG_DIR, LOGS_DIR, RESULTS_DIR, ensure_workspace


def main():
    ensure_workspace()
    print("Validate Lab 9")
    print("=" * 60)
    ok = True
    checks = [
        (CONFIG_DIR / "iam_review.json", "iam_review.json", "aws-iam"),
        (CONFIG_DIR / "encryption_audit.json", "encryption_audit.json", "aws"),
        (LOGS_DIR / "governance_audit_export.json", "governance_audit_export.json", "cloudtrail"),
        (RESULTS_DIR / "governance_report_final.json", "governance_report_final.json", None),
        (CONFIG_DIR / "governance_state.json", "governance_state.json", None),
    ]
    for path, name, source_key in checks:
        if path.exists():
            print(f"   ✅ {name}")
            if source_key:
                data = json.loads(path.read_text(encoding="utf-8"))
                if data.get("source") != source_key:
                    print(f"   ❌ {name} not from live AWS ({source_key})")
                    ok = False
        else:
            print(f"   ❌ Missing: {name}")
            ok = False

    print("\n" + "=" * 60)
    if ok:
        print("Prerequisites OK — proceed to Lab 10")
    else:
        print("Complete Lab 9 steps (lab9/STEPS.md).")
        sys.exit(1)


if __name__ == "__main__":
    main()
