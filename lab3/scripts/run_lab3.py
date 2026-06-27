"""Run all Lab 3 steps in sequence."""
import sys

from fairness_testing import main as fairness_main
from load_training_data import main as load_main
from sagemaker_experiments import main as experiments_main
from select_best_model import main as select_main
from train_models import main as train_main


def _experiments_dry_run():
    sys.argv = ["", "--dry-run"]
    experiments_main()


def run_lab3():
    print("Lab 3 — Model Training & Fairness Testing")
    print("=" * 60)
    steps = [
        ("Load training data", load_main),
        ("Train models", train_main),
        ("SageMaker experiments", _experiments_dry_run),
        ("Fairness testing", fairness_main),
        ("Select best model", select_main),
    ]
    for name, fn in steps:
        print(f"\n▶ {name}")
        fn()
    print("\n" + "=" * 60)
    print("Lab 3 complete.")


if __name__ == "__main__":
    run_lab3()
