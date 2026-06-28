# Reading the lab guides

Lab steps live in **`labN/STEPS.md`**. Each file uses the same layout so you can scan quickly.

## On every lab page

| Section | Meaning |
|---------|---------|
| **Info table** | Class, region, prerequisite, folders |
| **Before you start** | `git pull` and `cd labN` |
| **Do this** | Copy into the EC2 terminal (bash) |
| **Expected result** | Match this before moving on |
| **Screenshot (optional)** | Save under `labN/images/` if you want proof of work |

## Comfortable reading in VS Code

This repo includes `.vscode/settings.json` with:

- **Segoe UI / Nirmala UI** for Markdown preview (headings and body)
- **Consolas** for code in the editor
- Slightly larger line height for step text

Open any `STEPS.md` → **Ctrl+Shift+V** (Markdown preview) or side-by-side preview while you run commands.

## Tips

1. Run `clear` before each step.
2. Use **one terminal tab per lab** so history stays readable.
3. If output differs slightly (timestamps, IDs), check that checks show ✅ or PASS.
4. Never paste AWS access keys into chat, git, or screenshots.
