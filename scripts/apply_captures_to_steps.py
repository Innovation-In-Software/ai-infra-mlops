"""Inject EC2 terminal captures into labN/STEPS.md Expected output blocks."""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CAP = REPO / "docs" / "terminal-captures"

CAP_ALIASES = {
    "validate": ["stepval", "step-validate", "step-11-validate", "step-11-verify", "step11"],
    "run": ["steprun", "step-run"],
}

SECTION_MAP = {
    "3": {
        "load training data": 4,
        "train models": 5,
        "sagemaker experiments": 6,
        "fairness testing": 7,
        "select best model": 8,
    },
    "4": {
        "project structure": 4,
        "compliance gates": 5,
        "codepipeline config": 6,
        "simulate pipeline": 7,
    },
    "5": {
        "prepare container artifacts": 3,
        "docker build": 4,
        "ecr repository": 6,
    },
    "6": {
        "blue-green plan": 3,
        "staging deploy": 4,
        "test staging": 5,
        "production deploy": 6,
        "traffic shift": 7,
        "rollback drill": 8,
    },
    "7": {
        "prepare monitoring data": 3,
        "setup model monitor": 5,
        "monitor model quality": 6,
    },
    "8": {
        "define pipeline params": 3,
        "build pipeline": 4,
        "upsert pipeline": 5,
    },
    "9": {
        "review iam policies": 3,
        "audit encryption": 4,
        "governance fairness check": 5,
    },
    "10": {
        "collect course artifacts": 2,
        "architecture assessment": 3,
        "generate executive summary": 7,
    },
}


def load_capture(lab: str, kind: str) -> str | None:
    for suffix in CAP_ALIASES[kind]:
        p = CAP / f"lab{lab}-{suffix}.txt"
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")
    return None


def clean_capture(raw: str, max_lines: int = 60) -> str:
    skip_sub = ("PythonDeprecationWarning", "warnings.warn", "sagemaker.config INFO", "ConvergenceWarning")
    lines = []
    for line in raw.splitlines():
        if line.startswith("=== Lab") or line.startswith("$ "):
            continue
        if any(s in line for s in skip_sub):
            continue
        lines.append(line)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if len(lines) > max_lines:
        lines = lines[:max_lines] + ["   ..."]
    return "\n".join(lines)


def extract_sections(run_text: str) -> dict[str, str]:
    sections = {}
    if not run_text:
        return sections
    for part in re.split(r"\n▶ ", run_text):
        if not part.strip():
            continue
        first_line, _, body = part.partition("\n")
        if not body.strip():
            continue
        sections[first_line.strip().lower()] = clean_capture(body, max_lines=22)
    return sections


def find_step_block(text: str, step_num: int) -> tuple[int, int] | None:
    pat = re.compile(rf"^# Step {step_num}\b", re.MULTILINE)
    m = pat.search(text)
    if not m:
        return None
    start = m.start()
    nxt = re.search(r"^# Step \d+\b", text[m.end() :], re.MULTILINE)
    end = m.end() + nxt.start() if nxt else len(text)
    return start, end


def replace_in_block(block: str, new_output: str) -> str:
    exp = block.find("**Expected output:**")
    if exp < 0:
        return block
    fence = block.find("```text", exp)
    if fence >= 0:
        inner_start = block.find("\n", fence) + 1
        inner_end = block.find("```", inner_start)
        if inner_end < 0:
            return block
        return block[:inner_start] + new_output + "\n" + block[inner_end:]
    # inline backticks
    m = re.search(r"\*\*Expected output:\*\* `([^`]*)`", block[exp:])
    if m:
        return block[: exp + m.start(1)] + new_output.splitlines()[0] + block[exp + m.end(1) :]
    return block


def replace_step(text: str, step_num: int, new_output: str) -> str:
    span = find_step_block(text, step_num)
    if not span:
        return text
    s, e = span
    new_block = replace_in_block(text[s:e], new_output)
    if new_block == text[s:e]:
        return text
    return text[:s] + new_block + text[e:]


def validate_step_num(text: str, lab: str) -> int | None:
    if lab == "0":
        for sn in (11, 8):
            if f"# Step {sn}" in text and "verify_environment" in text:
                return sn
        return 11
    if lab == "1":
        return 9
    for m in re.finditer(r"# Step (\d+)[^\n]*\n(?:.*?\n){0,40}?```bash\n.*?validate_lab", text, re.DOTALL):
        return int(m.group(1))
    for m in re.finditer(r"# Step (\d+)[^\n]*\n(?:.*?\n){0,40}?validate_environment", text, re.DOTALL):
        return int(m.group(1))
    return None


def apply_lab(lab: str) -> list[str]:
    changes = []
    steps_path = REPO / f"lab{lab}" / "STEPS.md"
    if not steps_path.exists():
        return changes
    text = steps_path.read_text(encoding="utf-8")

    val = load_capture(lab, "validate")
    if val:
        sn = validate_step_num(text, lab)
        if sn:
            updated = replace_step(text, sn, clean_capture(val))
            if updated != text:
                text = updated
                changes.append(f"lab{lab} step {sn} validate")

    run = load_capture(lab, "run")
    if run:
        for key, step_num in SECTION_MAP.get(lab, {}).items():
            if key in extract_sections(run):
                updated = replace_step(text, step_num, extract_sections(run)[key])
                if updated != text:
                    text = updated
                    changes.append(f"lab{lab} step {step_num}")

    for sn, suffix in {"0": [(2, "step2"), (7, "step7"), (11, "step11")], "1": [(3, "step3"), (9, "step9")], "2": [(11, "step11")]}.get(lab, []):
        p = CAP / f"lab{lab}-{suffix}.txt"
        if p.exists():
            updated = replace_step(text, sn, clean_capture(p.read_text(encoding="utf-8")))
            if updated != text:
                text = updated
                changes.append(f"lab{lab} step {sn}")

    if changes:
        steps_path.write_text(text, encoding="utf-8")
    return changes


def main():
    all_changes = []
    for n in range(11):
        all_changes.extend(apply_lab(str(n)))
    print("Updated:", ", ".join(all_changes) if all_changes else "nothing")


if __name__ == "__main__":
    main()
