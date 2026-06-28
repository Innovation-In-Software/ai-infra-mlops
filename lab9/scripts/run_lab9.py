"""Run Lab 9 governance workflow."""
from audit_encryption import main as enc_main
from export_audit_trail import main as audit_main
from generate_explainability import main as explain_main
from generate_governance_report import main as report_main
from governance_fairness_check import main as fair_main
from load_governance_baseline import main as base_main
from model_approval_workflow import main as approval_main
from review_iam_policies import main as iam_main


def run_lab9():
    print("Lab 9 — Security & Governance")
    print("=" * 60)
    base_main()
    for fn in [iam_main, enc_main, approval_main, explain_main, fair_main, audit_main, report_main]:
        print(f"\n▶ {fn.__module__}")
        fn()
    print("\nLab 9 complete.")


if __name__ == "__main__":
    run_lab9()
