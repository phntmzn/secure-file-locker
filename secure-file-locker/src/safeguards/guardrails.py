from __future__ import annotations
from locker.config import Config
from pathlib import Path

def preflight_checks(cfg: Config) -> None:
    # Must operate only within allowlisted directory
    if not cfg.allowlist_dir.exists():
        raise SystemExit(f"Allowlist directory does not exist: {cfg.allowlist_dir}")
    # Refuse to run if allowlist_dir is '/' or very short path (dangerous)
    p = cfg.allowlist_dir.resolve()
    if str(p) in ("/", "/home", "/Users"):
        raise SystemExit("Refusing to operate on high-risk root directories.")
