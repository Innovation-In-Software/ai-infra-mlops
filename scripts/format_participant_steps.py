#!/usr/bin/env python3
"""Normalize lab STEPS.md for participant readability (Do this / Expected result)."""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

LAB_META = {
    "0": {
        "title": "Environment Setup & Prerequisites",
        "prereq": "None — start here",
        "extra": "| **Repo** | [github.com/gjkaur/ai-infra-mlops](https://github.com/gjkaur/ai-infra-mlops) |\n",
    },
    "1": {"title": "Secure MLOps Environment Setup", "prereq": "[Lab 0](../lab0/STEPS.md)"},
    "2": {"title": "Banking Data Management & PII Protection", "prereq": "[Lab 1](../lab1/STEPS.md)"},
    "3": {"title": "Model Training & Fairness Testing", "prereq": "[Lab 2](../lab2/STEPS.md)"},
    "4": {"title": "CI/CD Pipeline with Compliance Gates", "prereq": "[Lab 3](../lab3/STEPS.md)"},
    "5": {"title": "Secure Containerization for Banking", "prereq": "[Lab 4](../lab4/STEPS.md)"},
    "6": {"title": "Blue-Green Deployment", "prereq": "[Lab 5](../lab5/STEPS.md)"},
    "7": {"title": "Compliance Monitoring & Observability", "prereq": "[Lab 6](../lab6/STEPS.md)"},
    "8": {"title": "End-to-End SageMaker Pipeline", "prereq": "[Lab 7](../lab7/STEPS.md)"},
    "9": {"title": "Banking Security & Governance Framework", "prereq": "[Lab 8](../lab8/STEPS.md)"},
    "10": {"title": "Enterprise MLOps Architecture", "prereq": "[Lab 9](../lab9/STEPS.md)"},
}


def build_header(lab: str, meta: dict) -> str:
    n = lab
    extra = meta.get("extra", "")
    scripts_note = ""
    if int(lab) >= 3:
        scripts_note = f"\n> **Quick run:** `python3 scripts/run_lab{n}.py` runs all script steps in order.\n"
    return f"""# Lab {n}: {meta['title']}

| | |
|---|---|
| **Class** | `ai-mlops-2026-jun30` |
| **Duration** | ~30 minutes |
| **Region** | `us-west-2` |
| **Platform** | EC2 · [VS Code Remote SSH](../docs/SSH-VSCODE-SETUP.md) · **bash** |
| **Prerequisite** | {meta['prereq']} |
| **Working directory** | `~/ai-infra-mlops/lab{n}` |
| **Outputs** | `~/ai-infra-mlops/workspace/lab{n}/` |
{extra}
> All commands run in the **VS Code integrated terminal** on EC2. Do not use local Windows PowerShell for lab steps.
{scripts_note}
---

## Before you start

```bash
cd ~/ai-infra-mlops && git pull
cd lab{n}
```

Run `clear` before each step for clean terminal screenshots.

---

"""


def format_step_block(block: str) -> str:
    block = block.strip()
    if not block.startswith("# Step "):
        return block

    m = re.match(r"# Step (\d+) — (.+)", block)
    if not m:
        return block

    num, title = m.group(1), m.group(2)
    body = block[m.end() :].strip()

    # Already formatted
    if "**Do this:**" in body and "**Expected result:**" in body:
        return f"## Step {num} — {title}\n\n{body}\n\n---\n"

    do_text = ""
    expected = ""
    screenshot = ""

    # **Do:** prose (no bash)
    do_prose = re.search(r"\*\*Do:\*\*\s*(.+?)(?=\n\n|\*\*Expected|\*\*Optional|$)", body, re.DOTALL)
    if do_prose:
        do_text = do_prose.group(1).strip()

    bash = re.search(r"```bash\n(.*?)```", body, re.DOTALL)
    if bash:
        do_text = f"```bash\n{bash.group(1).strip()}\n```" if not do_text else do_text + "\n\n" + f"```bash\n{bash.group(1).strip()}\n```"

    inline_exp = re.search(r"\*\*Expected output:\*\*\s*`([^`]+)`", body)
    if inline_exp:
        expected = inline_exp.group(1).strip()
    else:
        text_block = re.search(r"\*\*Expected (?:output|result):\*\*\s*\n\n```(?:text)?\n(.*?)```", body, re.DOTALL)
        if text_block:
            expected = text_block.group(1).strip()
        else:
            exp_result = re.search(r"\*\*Expected result:\*\*\s*(.+?)(?=\n\n|\*\*Optional|$)", body, re.DOTALL)
            if exp_result:
                expected = exp_result.group(1).strip()

    shot = re.search(r"\*\*Optional screenshot:\*\*\s*`([^`]+)`", body)
    if shot:
        screenshot = f"\n\n**Screenshot (optional):** `{shot.group(1)}`"

    out = f"## Step {num} — {title}\n\n"
    if do_text:
        out += f"**Do this:**\n\n{do_text}\n\n"
    if expected:
        if "\n" in expected or len(expected) > 60:
            out += f"**Expected result:**\n\n```text\n{expected}\n```\n"
        else:
            out += f"**Expected result:** `{expected}`\n"
    out += screenshot + "\n\n---\n"
    return out


def format_steps_content(text: str, lab: str) -> str:
    meta = LAB_META[lab]
    # Find first step
    first_step = re.search(r"^# Step 1 ", text, re.MULTILINE)
    if not first_step:
        return text

    preamble = text[: first_step.start()]
    # Keep special sections before steps (e.g. classroom env) from preamble if after title
    special = ""
    for section in ("## Classroom env", "## Before you start"):
        sm = re.search(rf"({section}.*?)(?=\n# Step 1 |\Z)", preamble, re.DOTALL)
        if sm and section != "## Before you start":
            special += sm.group(1).strip() + "\n\n---\n\n"

    rest = text[first_step.start() :]
    parts = re.split(r"(?=^# Step \d+ — )", rest, flags=re.MULTILINE)
    steps = [format_step_block(p) for p in parts if p.strip()]

    footer = ""
    fm = re.search(r"^## Lab \d+ complete.*", text, re.MULTILINE | re.DOTALL)
    if fm:
        footer = "\n" + fm.group(0).strip() + "\n"

    header = build_header(lab, meta)
    if special:
        header = header.rstrip() + "\n\n" + special

    return header + "\n".join(steps) + footer


def main():
    for lab, meta in LAB_META.items():
        path = REPO / f"lab{lab}" / "STEPS.md"
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        formatted = format_steps_content(original, lab)
        path.write_text(formatted, encoding="utf-8")
        print(f"Formatted lab{lab}/STEPS.md")


if __name__ == "__main__":
    main()
