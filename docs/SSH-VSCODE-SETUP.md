# VS Code Remote SSH → EC2 (all labs)

Use this workflow for **every lab** (0–10). All commands run in the **EC2 integrated terminal** (bash).

## 1. SSH config (on your laptop)

Edit `~/.ssh/config` (Windows: `C:\Users\<you>\.ssh\config`):

```
Host student-ec2
    HostName <EC2-public-ip>
    User ec2-user
    IdentityFile ~/.ssh/your-lab-key.pem
```

Example from instructor handout — replace IP and key path.

## 2. Connect in VS Code

1. Install extension **Remote - SSH**
2. **Ctrl+Shift+P** → **Remote-SSH: Connect to Host** → `student-ec2`
3. **File → Open Folder** → `/home/ec2-user/ai-infra-mlops`
4. **Terminal → New Terminal** (bash)

Confirm prompt:

```text
[ec2-user@ip-172-31-xx-xx ai-infra-mlops]$
```

## 3. Rules for every lab

| Rule | Detail |
|------|--------|
| Working path | `~/ai-infra-mlops/labN` |
| Python | `python3` |
| Scripts | `python3 scripts/<name>.py` |
| Outputs | `~/ai-infra-mlops/workspace/labN/` |
| Region | `us-west-2` |
| Clear terminal | Run `clear` before each step (cleaner screenshots) |

## 4. Optional screenshots

Each step in `STEPS.md` has an **Optional screenshot** line. Capture from VS Code terminal or AWS Console when ready; save as `labN/images/step-XX-description.png`.

Screenshots are **optional** for passing the lab — scripts and expected output text are the source of truth.

## 5. Fresh start

```bash
cd ~/ai-infra-mlops
git pull
python3 scripts/reset_course.py --labs lab1,lab2
```

See [CLOUD-DELIVERY.md](../CLOUD-DELIVERY.md) for full reset including AWS resources.
