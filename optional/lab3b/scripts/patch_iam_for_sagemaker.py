"""Re-apply Lab 1 Data Scientist policy (adds CloudWatch Logs for Lab 3b)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lab1" / "scripts"))
from create_banking_iam_roles import create_banking_iam_roles

if __name__ == "__main__":
    create_banking_iam_roles()
