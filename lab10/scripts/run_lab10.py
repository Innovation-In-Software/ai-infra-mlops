"""Run Lab 10 capstone."""
from architecture_assessment import main as assess_main
from build_compliance_bundle import main as bundle_main
from collect_course_artifacts import main as collect_main
from gap_analysis import main as gap_main
from generate_executive_summary import main as summary_main
from implementation_checklist import main as checklist_main
from implementation_roadmap import main as roadmap_main


def run_lab10():
    print("Lab 10 — Enterprise MLOps Architecture")
    print("=" * 60)
    for fn in [collect_main, assess_main, gap_main, roadmap_main, checklist_main, summary_main, bundle_main]:
        print(f"\n▶ {fn.__module__}")
        fn()
    print("\nLab 10 complete.")


if __name__ == "__main__":
    run_lab10()
