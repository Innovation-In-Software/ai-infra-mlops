<h1 align="center">AI-MLOps on AWS</h1>
<h2 align="center">Participant Labs</h2>

<p align="center">
  <strong>Class:</strong> ai-mlops-2026-jun30 &nbsp;·&nbsp;
  <strong>Region:</strong> us-west-2
</p>

<p align="center">
  <strong>Delivery:</strong> EC2 in <code>us-west-2</code> + SSH + <a href="docs/SSH-VSCODE-SETUP.md">VS Code Remote SSH</a>.
  See <a href="CLOUD-DELIVERY.md">CLOUD-DELIVERY.md</a> for golden AMI, fresh start, and 30-minute timing.
</p>

<p align="center">
  <strong>All labs run on EC2</strong> — use the VS Code integrated terminal (bash). Do not use local Windows PowerShell for lab steps.
</p>

<p align="center">
  Clone once in Lab 0 — open each lab’s <code>STEPS.md</code> in order.
  Outputs go under <code>workspace/labN/</code> (gitignored).
</p>

---

<h2>Fresh start</h2>

<pre>
cd ~/ai-infra-mlops
python3 scripts/reset_course.py --labs lab1,lab2,lab3,lab4,lab5,lab6,lab7,lab8,lab9,lab10
cd lab2 && python3 scripts/cleanup_lab2.py --aws   # optional: remove Feature Groups
</pre>

<p>Then re-run <a href="lab0/STEPS.md">Lab 0</a> verify → Labs 1–10 in order.</p>

---

<h2>Lab index (0–10)</h2>

| Lab | Title | Folder | Guide |
|-----|-------|--------|-------|
| 0 | Environment Setup | <code>lab0/</code> | <a href="lab0/STEPS.md">lab0/STEPS.md</a> |
| 1 | Secure MLOps Environment | <code>lab1/</code> | <a href="lab1/STEPS.md">lab1/STEPS.md</a> |
| 2 | Banking Data &amp; PII | <code>lab2/</code> | <a href="lab2/STEPS.md">lab2/STEPS.md</a> |
| 3 | Model Training &amp; Fairness | <code>lab3/</code> | <a href="lab3/STEPS.md">lab3/STEPS.md</a> |
| 4 | CI/CD with Compliance Gates | <code>lab4/</code> | <a href="lab4/STEPS.md">lab4/STEPS.md</a> |
| 5 | Secure Containerization | <code>lab5/</code> | <a href="lab5/STEPS.md">lab5/STEPS.md</a> |
| 6 | Blue-Green Deployment | <code>lab6/</code> | <a href="lab6/STEPS.md">lab6/STEPS.md</a> |
| 7 | Monitoring &amp; Observability | <code>lab7/</code> | <a href="lab7/STEPS.md">lab7/STEPS.md</a> |
| 8 | SageMaker Pipelines | <code>lab8/</code> | <a href="lab8/STEPS.md">lab8/STEPS.md</a> |
| 9 | Security &amp; Governance | <code>lab9/</code> | <a href="lab9/STEPS.md">lab9/STEPS.md</a> |
| 10 | Enterprise MLOps Architecture | <code>lab10/</code> | <a href="lab10/STEPS.md">lab10/STEPS.md</a> |

**Classroom defaults (Lab 2):** `LAB_NUM_RECORDS=1000`, `LAB_USE_COMPREHEND=0`

**Labs 3–10:** Runnable scripts in each `labN/scripts/` — use `python3 scripts/run_labN.py` or follow `labN/STEPS.md`.

---

<h2>Quick links</h2>

<ul>
  <li><a href="docs/SSH-VSCODE-SETUP.md">SSH + VS Code setup</a></li>
  <li><a href="CLOUD-DELIVERY.md">Instructor cloud delivery guide</a></li>
  <li><a href="lab0/STEPS.md">Start here — Lab 0</a></li>
</ul>
