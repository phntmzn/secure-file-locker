from __future__ import annotations
from pathlib import Path
import shutil

def restore_file(backup_path: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup_path, dst)
