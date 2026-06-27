"""Environment verification for Banking MLOps Labs."""
import argparse
import importlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent


class EnvironmentVerifier:
    """Verify all environment components are properly configured."""

    PACKAGE_ALIASES = {"sklearn": "sklearn"}

    REQUIRED_PACKAGES = [
        "boto3",
        "sagemaker",
        "pandas",
        "numpy",
        "sklearn",
        "xgboost",
        "shap",
        "matplotlib",
        "seaborn",
        "joblib",
        "flask",
        "pytest",
    ]

    def __init__(self, dry_run=False, workspace=None, skip_aws=False):
        self.dry_run = dry_run
        self.skip_aws = skip_aws or dry_run
        self.workspace = Path(workspace) if workspace else REPO_ROOT / "workspace"
        self.results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "dry_run": dry_run,
            "checks": [],
        }
        self.passed = 0
        self.failed = 0

    def add_check(self, name, passed, details):
        self.results["checks"].append({"name": name, "passed": passed, "details": details})
        if passed:
            self.passed += 1
            print(f"   [PASS] {name}: {details}")
        else:
            self.failed += 1
            print(f"   [FAIL] {name}: {details}")

    def verify_python(self):
        version_info = sys.version_info
        ok = version_info >= (3, 8)
        self.add_check(
            "Python Version",
            ok,
            f"Python {version_info.major}.{version_info.minor}.{version_info.micro}",
        )

    def verify_packages(self):
        installed = []
        missing = []
        for package in self.REQUIRED_PACKAGES:
            try:
                importlib.import_module(package)
                installed.append(package)
            except ImportError:
                missing.append(package)

        self.add_check(
            "Required Packages",
            len(missing) == 0,
            f"Installed: {len(installed)}, Missing: {len(missing)}",
        )
        if missing:
            print(f"      Missing: {', '.join(missing)}")
            print(f"      Run: pip install -r requirements.txt")

    def verify_aws_cli(self):
        if self.skip_aws:
            self.add_check("AWS CLI Region", True, "Skipped (--dry-run)")
            self.add_check("AWS CLI Credentials", True, "Skipped (--dry-run)")
            return

        aws = shutil.which("aws")
        if not aws:
            self.add_check("AWS CLI", False, "aws command not found")
            return

        try:
            region_result = subprocess.run(
                [aws, "configure", "get", "region"],
                capture_output=True,
                text=True,
                check=False,
            )
            region = region_result.stdout.strip()
            self.add_check("AWS CLI Region", region == "us-west-2", f"Region: {region or 'not set'}")

            identity_result = subprocess.run(
                [aws, "sts", "get-caller-identity"],
                capture_output=True,
                text=True,
                check=False,
            )
            if identity_result.returncode == 0:
                identity = json.loads(identity_result.stdout)
                arn = identity.get("Arn", "Unknown")
                self.add_check("AWS CLI Credentials", True, f"Arn: {arn}")
            else:
                self.add_check("AWS CLI Credentials", False, identity_result.stderr.strip() or "Failed")
        except Exception as exc:
            self.add_check("AWS CLI", False, str(exc))

    def verify_boto3(self):
        if self.skip_aws:
            self.add_check("Boto3 AWS Access", True, "Skipped (--dry-run)")
            return
        try:
            import boto3

            identity = boto3.client("sts").get_caller_identity()
            self.add_check(
                "Boto3 AWS Access",
                True,
                f"Account: {identity.get('Account', 'unknown')}",
            )
        except Exception as exc:
            self.add_check("Boto3 AWS Access", False, str(exc))

    def verify_directories(self):
        config_path = ROOT / "config" / "environment_config.json"
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

        course_missing = []
        for lab_folder in config["course_labs"]:
            if not (REPO_ROOT / lab_folder).exists():
                course_missing.append(lab_folder)

        workspace_missing = []
        if self.workspace.exists():
            for dir_name in config["student_workspace_dirs"]:
                if not (self.workspace / dir_name).exists():
                    workspace_missing.append(dir_name)

        course_ok = len(course_missing) == 0
        workspace_ok = self.workspace.exists() and len(workspace_missing) == 0

        if course_ok:
            self.add_check(
                "Course Lab Folders",
                True,
                f"Found {len(config['course_labs'])} lab folder(s) in repo",
            )
        else:
            self.add_check(
                "Course Lab Folders",
                False,
                f"Missing: {', '.join(course_missing)}",
            )

        if self.workspace.exists():
            self.add_check(
                "Student Workspace",
                workspace_ok,
                f"Workspace: {self.workspace} ({len(workspace_missing)} missing)",
            )
        else:
            self.add_check(
                "Student Workspace",
                self.dry_run,
                f"Not created yet (run setup_lab_directories.py). Expected: {self.workspace}",
            )

    def verify_git(self):
        git = shutil.which("git")
        if not git:
            self.add_check("Git", False, "git command not found")
            return
        try:
            result = subprocess.run(
                [git, "rev-parse", "--is-inside-work-tree"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            in_repo = result.returncode == 0 and result.stdout.strip() == "true"
            self.add_check("Git Repository", in_repo, "Repo cloned" if in_repo else "Not in git repo")
        except Exception as exc:
            self.add_check("Git Repository", False, str(exc))

    def verify_region_config(self):
        config_path = ROOT / "config" / "environment_config.json"
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
        self.add_check(
            "Default Region Config",
            config.get("default_region") == "us-west-2",
            config.get("default_region", "unknown"),
        )

    def run_verification(self):
        print("Banking MLOps Environment Verification")
        print("=" * 60)
        if self.dry_run:
            print("Mode: dry-run (AWS checks skipped)")

        self.verify_python()
        self.verify_packages()
        self.verify_region_config()
        self.verify_aws_cli()
        self.verify_boto3()
        self.verify_directories()
        self.verify_git()

        print("\n" + "=" * 60)
        print("Verification Summary:")
        print(f"   Total Checks: {self.passed + self.failed}")
        print(f"   Passed: {self.passed}")
        print(f"   Failed: {self.failed}")

        if self.failed == 0:
            print("\nALL CHECKS PASSED. Environment is ready.")
            print("   Proceed to Lab 1 (open lab1/STEPS.md)")
        else:
            print("\nSome checks failed. Fix issues before proceeding.")

        self.results["summary"] = {
            "passed": self.passed,
            "failed": self.failed,
            "ready": self.failed == 0,
        }

        logs_dir = ROOT / "logs"
        logs_dir.mkdir(exist_ok=True)
        results_path = logs_dir / "verification_results.json"
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved: {results_path}")

        return self.passed, self.failed


def main():
    parser = argparse.ArgumentParser(description="Verify Banking MLOps environment")
    parser.add_argument("--dry-run", action="store_true", help="Skip live AWS credential checks")
    parser.add_argument("--workspace", type=str, default=None, help="Student workspace path")
    args = parser.parse_args()

    verifier = EnvironmentVerifier(dry_run=args.dry_run, workspace=args.workspace)
    passed, failed = verifier.run_verification()
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
