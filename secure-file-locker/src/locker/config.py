from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

@dataclass
class Config:
    allowlist_dir: Path
    excludes: List[str] = field(default_factory=lambda: [".git", "__pycache__"])
    max_file_size_mb: int = 50
    dry_run: bool = True
    log_level: str = "INFO"
    manifest_path: Path = Path(".sfl-manifest.json")
    backup_dir: Path = Path(".sfl-backups")
