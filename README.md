# Secure File Locker (safe-by-default)

> **Safety banner:** This tool is for **controlled demos and learning**. It defaults to `--dry-run` and supports `--canary` so only `*.CANARY` files are touched during testing. **Do not** aim it at system folders or irreplaceable data.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
cd examples && ./quickstart.sh
