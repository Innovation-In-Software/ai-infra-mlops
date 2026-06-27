"""Validate course completion."""
import json
import sys
from lab_paths import RESULTS_DIR, ensure_workspace, lab_workspace


def main():
    ensure_workspace()
    print("Validate Lab 10 — Course Completion")
    print("=" * 60)
    score_path = RESULTS_DIR / "architecture_assessment.json"
    score = 0
    if score_path.exists():
        with open(score_path, encoding="utf-8") as f:
            score = json.load(f).get("score", 0)
    ok = score >= 90 and (RESULTS_DIR / "course_compliance_bundle.zip").exists()
    if ok:
        print("🎉 COURSE COMPLETE — ai-mlops-2026-jun30")
    else:
        print("   Run all Lab 10 steps first.")
        sys.exit(1)


if __name__ == "__main__":
    main()
