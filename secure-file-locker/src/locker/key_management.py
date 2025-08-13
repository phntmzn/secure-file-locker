from __future__ import annotations
from pathlib import Path
from typing import Optional
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os, base64, secrets, json

def derive_key_from_password(password: str, salt: bytes, n=2**14, r=8, p=1) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=n, r=r, p=p, backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))

def create_password_key(password: str, metadata_path: Path) -> bytes:
    salt = secrets.token_bytes(16)
    key = derive_key_from_password(password, salt)
    metadata_path.write_text(json.dumps({"kdf": "scrypt", "salt": base64.b64encode(salt).decode()}))
    return key

def load_password_key(password: str, metadata_path: Path) -> bytes:
    meta = json.loads(metadata_path.read_text())
    salt = base64.b64decode(meta["salt"])
    return derive_key_from_password(password, salt)

def rotate_key(old_key: bytes, new_key: bytes, keyfile: Path) -> None:
    # Placeholder for proper key escrow/rotation mechanism.
    keyfile.write_bytes(new_key)

def save_raw_key(key: bytes, path: Path) -> None:
    os.umask(0o077)
    path.write_bytes(key)

def load_raw_key(path: Path) -> bytes:
    return path.read_bytes()
