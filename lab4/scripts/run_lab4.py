"""Run Lab 4 CI/CD workflow."""
from generate_cicd_report import main as report_main
from run_compliance_checks import main as compliance_main
from setup_codepipeline import main as pipeline_main
from setup_project_structure import main as structure_main
from simulate_pipeline_run import main as simulate_main


def run_lab4():
    print("Lab 4 — CI/CD with Compliance Gates")
    print("=" * 60)
    for name, fn in [
        ("Project structure", structure_main),
        ("Compliance gates", compliance_main),
        ("CodePipeline config", pipeline_main),
        ("Simulate pipeline", simulate_main),
        ("CI/CD report", report_main),
    ]:
        print(f"\n▶ {name}")
        fn()
    print("\nLab 4 complete.")


if __name__ == "__main__":
    run_lab4()
