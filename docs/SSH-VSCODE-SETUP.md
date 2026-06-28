# VS Code Remote SSH → EC2 (all labs)

Use this workflow for **every lab** (0–10). All commands run in the **EC2 integrated terminal** (bash).

**First-time setup (ProTech VM, AWS login, region, launch EC2, connect VS Code):** follow **[lab0/STEPS.md](../lab0/STEPS.md) Steps 1–13** in full.

1. **Steps 1–3** — [labs.protechtraining.com](https://labs.protechtraining.com) → sign in → connect to training VM  
2. **Steps 4–12** — AWS Console + SSH config on the VM  
3. **Step 13** — VS Code Remote SSH to EC2

---

## Quick reference (after Lab 0)

### SSH config (on ProTech VM or laptop)

Edit `~/.ssh/config` (Windows: `C:\Users\<you>\.ssh\config`):

```
Host mlops-lab-ec2
    HostName YOUR_EC2_PUBLIC_IP
    User ec2-user
    IdentityFile C:/Users/<you>/.ssh/mlops-lab-key.pem
```

Replace `YOUR_EC2_PUBLIC_IP` with the value from EC2 console (Lab 0 Step 10). Update after stop/start.

### Connect in VS Code

1. Extension **Remote - SSH** installed
2. **Ctrl+Shift+P** → **Remote-SSH: Connect to Host** → `mlops-lab-ec2`
3. **File → Open Folder** → `/home/ec2-user/ai-infra-mlops`
4. **Terminal → New Terminal** (bash)

Confirm prompt:

```text
[ec2-user@ip-172-31-xx-xx ai-infra-mlops]$
```

---

## Rules for every lab

| Rule | Detail |
|------|--------|
| Working path | `~/ai-infra-mlops/labN` |
| Python | `python3` |
| Scripts | `python3 scripts/<name>.py` |
| Outputs | `~/ai-infra-mlops/workspace/labN/` |
| Region | `us-west-2` |
| Clear terminal | Run `clear` before each step (cleaner screenshots) |

---

## Optional screenshots

Each step in `STEPS.md` has an **Optional screenshot** line. Capture from VS Code terminal or AWS Console when ready; save as `labN/images/step-XX-description.png`.

Screenshots are **optional** for passing the lab — scripts and expected output text are the source of truth.

---

## Fresh start

```bash
cd ~/ai-infra-mlops
git pull
python3 scripts/reset_course.py --labs lab1,lab2
```

See [CLOUD-DELIVERY.md](../CLOUD-DELIVERY.md) for full reset including AWS resources.

---

## Related

- [Lab 0 STEPS.md](../lab0/STEPS.md) — full AWS Console + EC2 + VS Code setup
- [PROTECH-VM-SETUP.md](PROTECH-VM-SETUP.md) — instructor ProTech VM + EC2 dual delivery
