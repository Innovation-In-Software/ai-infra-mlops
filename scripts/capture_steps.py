#!/usr/bin/env python3
"""Capture terminal output for STEPS.md (run from repo root)."""
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "terminal-captures"
OUT.mkdir(parents=True, exist_ok=True)
ENV = {**os.environ, "LAB_NUM_RECORDS": "1000", "LAB_USE_COMPREHEND": "0"}


def normalize(text: str) -> str:
    home = "/home/ec2-user/ai-infra-mlops"
    text = text.replace(str(REPO).replace("\\", "/"), home).replace(str(REPO), home)
    text = re.sub(r"Python 3\.\d+\.\d+", "Python 3.11.x", text)
    text = re.sub(r"git version 2\.[\d.]+", "git version 2.x.x", text)
    text = re.sub(r"aws-cli/[\d.]+ Python/[\d.]+ \S+", "aws-cli/2.x.x Python/3.x.x Linux/x86_64", text)
    return text.strip()


def run(*cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd or REPO, capture_output=True, text=True, env=ENV)
    return (p.stdout + p.stderr).strip()


def save(lab, step, text):
    path = OUT / f"lab{lab}-step-{step}.txt"
    path.write_text(normalize(text), encoding="utf-8")
    print(f"  lab{lab}-{step}: {len(text)} chars -> {path.name}")


def main():
    print("Capturing outputs (normalize paths to EC2)...")
    save("0", "02-tools", "\n".join([run("python", "--version"), run("git", "--version"), run("aws", "--version")]))
    save("0", "07-aws-cli", run("aws", "sts", "get-caller-identity") + "\n" + run("aws", "configure", "get", "region"))
    save("0", "11-verify", run(sys.executable, "scripts/verify_environment.py", cwd=REPO / "lab0"))
    save("1", "03-aws", run("aws", "sts", "get-caller-identity") + "\n" + run("aws", "configure", "get", "region"))
    save("1", "09-validate", run(sys.executable, "scripts/validate_environment.py", cwd=REPO / "lab1"))
    save("2", "11-validate", run(sys.executable, "scripts/validate_lab2.py", cwd=REPO / "lab2"))
    for n in range(3, 11):
        save(str(n), "run", run(sys.executable, f"scripts/run_lab{n}.py", cwd=REPO / f"lab{n}"))
        save(str(n), "validate", run(sys.executable, f"scripts/validate_lab{n}.py", cwd=REPO / f"lab{n}"))
    if "--teardown" in sys.argv:
        save("10", "teardown", run(sys.executable, str(REPO / "scripts" / "teardown_course.py"), "--yes", "--skip-aws"))
    print(f"Done -> {OUT}")


if __name__ == "__main__":
    main()
