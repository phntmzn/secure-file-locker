from __future__ import annotations
from pathlib import Path
import shutil, time

def backup_file(src: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    dst = backup_dir / f"{src.name}.{ts}.bak"
    shutil.copy2(src, dst)
    return dst
