# Use the canonical lab repo

**Authoritative source:** https://github.com/gjkaur/ai-infra-mlops

This folder is a **local snapshot** for the course directory. For the latest steps, clone or pull from GitHub.

## Fresh clone (recommended)

```bash
cd ~
rm -rf ai-infra-mlops
git clone https://github.com/gjkaur/ai-infra-mlops.git
cd ai-infra-mlops
```

On **EC2** after clone, open `/home/ec2-user/ai-infra-mlops` in VS Code Remote SSH.

## Setup order (participants)

1. [labs.protechtraining.com](https://labs.protechtraining.com) → training VM (Lab 0 Steps 1–3)
2. AWS Console → `us-west-2` → launch EC2 (Lab 0 Steps 4–10)
3. VS Code Remote SSH → EC2 (Lab 0 Steps 11–13)
4. Clone repo on EC2 → verify → Labs 1–10

**Full guide:** [lab0/STEPS.md](lab0/STEPS.md)

## Key docs on GitHub

| Doc | Purpose |
|-----|---------|
| [README.md](README.md) | Participant overview |
| [lab0/STEPS.md](lab0/STEPS.md) | ProTech + AWS + EC2 + VS Code setup |
| [docs/PROTECH-VM-SETUP.md](docs/PROTECH-VM-SETUP.md) | Instructor dual delivery |
| [docs/SSH-VSCODE-SETUP.md](docs/SSH-VSCODE-SETUP.md) | Remote SSH reference |
| [CLOUD-DELIVERY.md](CLOUD-DELIVERY.md) | Class timing & AMI |
| [lab10/STEPS.md](lab10/STEPS.md) | Course teardown |

## Teardown (fresh AWS account)

```bash
cd ~/ai-infra-mlops
python3 scripts/teardown_course.py --yes
python3 scripts/teardown_course.py --yes --terminate-ec2   # optional: stop lab EC2
```

## Do not use old remotes

If `git remote -v` shows `MLOps_using_AWS`, reset:

```bash
git remote set-url origin https://github.com/gjkaur/ai-infra-mlops.git
git fetch origin && git reset --hard origin/main
```

Or delete this folder and `git clone` again.
