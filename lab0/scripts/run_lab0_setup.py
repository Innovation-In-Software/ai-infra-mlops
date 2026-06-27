"""Orchestrate Lab 0 environment setup."""
import argparse
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from setup_lab_directories import create_workspace, default_workspace
from verify_environment import EnvironmentVerifier


def main():
    parser = argparse.ArgumentParser(description="Complete Lab 0 setup")
    parser.add_argument("--dry-run", action="store_true", help="Skip AWS checks")
    parser.add_argument("--skip-workspace", action="store_true", help="Do not create student workspace")
    parser.add_argument("--target", type=Path, default=None, help="Student workspace path")
    args = parser.parse_args()

    print("Banking MLOps Lab 0 Setup")
    print("=" * 60)

    if not args.skip_workspace:
        target = args.target or default_workspace()
        print(f"\n1. Creating workspace at {target}...")
        created, mapping = create_workspace(target)
        print(f"   Created {len(created)} top-level directories")
        print(f"   Mapping: {mapping}")
    else:
        target = args.target or default_workspace()
        print("\n1. Skipping workspace creation (--skip-workspace)")

    print("\n2. Running environment verification...")
    verifier = EnvironmentVerifier(dry_run=args.dry_run, workspace=str(target))
    passed, failed = verifier.run_verification()

    print("\nLab 0 setup complete.")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
