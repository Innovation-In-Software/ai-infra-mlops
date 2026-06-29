#!/usr/bin/env python3
"""Re-apply Lab 1 banking IAM roles (run after git pull before Labs 5–10)."""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from scripts.course_common import refresh_banking_iam

if __name__ == "__main__":
    raise SystemExit(refresh_banking_iam())
