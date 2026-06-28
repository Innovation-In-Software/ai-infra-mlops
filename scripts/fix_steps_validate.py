"""Fix step-1 corruption and apply validate captures to correct steps."""
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[1]
CAP = REPO / "docs" / "terminal-captures"

STEP1_OUTPUT = {
    "2": "STEPS.md\nconfig\nimages\nrequirements.txt\nscripts",
    "3": "STEPS.md\nconfig\nimages\nrequirements.txt\nscripts",
    "4": "STEPS.md\nconfig\nimages\nrequirements.txt\nscripts\nsrc\ntests\nbuildspecs",
    "5": "STEPS.md\nconfig\nimages\nrequirements.txt\nscripts\nsrc",
    "6": "STEPS.md\nconfig\nimages\nrequirements.txt\nscripts",
    "7": "STEPS.md\nconfig\nimages\nrequirements.txt\nscripts",
    "8": "STEPS.md\nconfig\nimages\npipeline\nrequirements.txt\nscripts",
    "9": "STEPS.md\nconfig\nimages\nrequirements.txt\nscripts",
    "10": "STEPS.md\nconfig\nimages\nrequirements.txt\nscripts",
}

VALIDATE_STEP = {
    "0": 11, "1": 9, "2": 11, "3": 9, "4": 10, "5": 10,
    "6": 10, "7": 10, "8": 10, "9": 10, "10": 9,
}


def clean_capture(raw: str, max_lines: int = 60) -> str:
    skip = ("PythonDeprecationWarning", "warnings.warn", "sagemaker.config INFO", "ConvergenceWarning")
    lines = []
    for line in raw.splitlines():
        if line.startswith("=== Lab") or line.startswith("$ "):
            continue
        if any(s in line for s in skip):
            continue
        lines.append(line)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines[:max_lines])


def load_val(lab: str) -> str | None:
    for suffix in ("stepval", "step-validate", "step-11-validate", "step11"):
        p = CAP / f"lab{lab}-{suffix}.txt"
        if p.exists():
            return clean_capture(p.read_text(encoding="utf-8"))
    return None


def find_step_block(text: str, step_num: int) -> tuple[int, int] | None:
    m = re.search(rf"^# Step {step_num}\b", text, re.MULTILINE)
    if not m:
        return None
    start = m.start()
    nxt = re.search(r"^# Step \d+\b", text[m.end():], re.MULTILINE)
    end = m.end() + nxt.start() if nxt else len(text)
    return start, end


def set_text_block(block: str, new_output: str) -> str:
    exp = block.find("**Expected output:**")
    if exp < 0:
        return block
    if "**Expected output:** `" in block[exp:exp+30]:
        return block  # inline — skip
    fence = block.find("```text", exp)
    if fence < 0:
        return block
    inner_start = block.find("\n", fence) + 1
    inner_end = block.find("```", inner_start)
    return block[:inner_start] + new_output + "\n" + block[inner_end:]


def main():
    for lab, out in STEP1_OUTPUT.items():
        path = REPO / f"lab{lab}" / "STEPS.md"
        text = path.read_text(encoding="utf-8")
        span = find_step_block(text, 1)
        if span:
            s, e = span
            new_block = set_text_block(text[s:e], out)
            text = text[:span[0]] + new_block + text[span[1]:]
        val = load_val(lab)
        if val:
            sn = VALIDATE_STEP[lab]
            span = find_step_block(text, sn)
            if span:
                s, e = span
                text = text[:s] + set_text_block(text[s:e], val) + text[e:]
        path.write_text(text, encoding="utf-8")
        print(f"fixed lab{lab}")


if __name__ == "__main__":
    main()
