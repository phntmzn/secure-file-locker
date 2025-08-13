from __future__ import annotations
from pathlib import Path

def enforce_canary(root: Path) -> None:
    """Ensure only *.CANARY files are touched when --canary is set."""
    for p in root.rglob("*"):
        if p.is_file() and not p.name.endswith(".CANARY") and not p.name.endswith(".CANARY.enc"):
            raise SystemExit("Canary mode active: non-CANARY file found. Aborting.")
