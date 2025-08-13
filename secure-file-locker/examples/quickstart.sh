#!/usr/bin/env bash
set -euo pipefail
echo "example.CANARY" > example.CANARY
python -m locker.cli gen-key --dry-run || true
python -m locker.cli gen-key
python -m locker.cli encrypt --canary --dry-run
python -m locker.cli encrypt --canary
python -m locker.cli decrypt --canary --dry-run
python -m locker.cli decrypt --canary
