from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict
import json, hashlib, time

@dataclass
class Entry:
    path: str
    size: int
    sha256: str
    mtime: float

def file_sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def snapshot(root: Path) -> Dict[str, Entry]:
    out: Dict[str, Entry] = {}
    for p in root.rglob("*"):
        if p.is_file():
            out[str(p.relative_to(root))] = Entry(
                path=str(p), size=p.stat().st_size, sha256=file_sha256(p), mtime=p.stat().st_mtime
            )
    return out

def write_manifest(path: Path, entries: Dict[str, Entry]) -> None:
    path.write_text(json.dumps({k: asdict(v) for k, v in entries.items()}, indent=2))
