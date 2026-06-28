# Use the canonical lab repo

**Do not use this copy for `git pull`.** The authoritative repo is:

https://github.com/gjkaur/ai-infra-mlops

## Recommended setup (instructor / EC2)

```bash
cd ~
rm -rf ai-infra-mlops   # if an old partial clone exists
git clone https://github.com/gjkaur/ai-infra-mlops.git
cd ai-infra-mlops
```

This course folder may contain a **synced snapshot** for convenience. After `git clone` above, open `~/ai-infra-mlops` in VS Code Remote SSH.

See [EC2-TESTING.md](docs/EC2-TESTING.md) for instructor EC2 and PEM key details.
