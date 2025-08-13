from __future__ import annotations
from pathlib import Path
from typing import Tuple
from cryptography.fernet import Fernet, InvalidToken

def generate_key() -> bytes:
    return Fernet.generate_key()

def get_cipher(k: bytes) -> Fernet:
    return Fernet(k)

def encrypt_file(src: Path, dst: Path, key: bytes) -> Tuple[int, int]:
    data = src.read_bytes()
    ct = get_cipher(key).encrypt(data)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(ct)
    return (len(data), len(ct))

def decrypt_file(src: Path, dst: Path, key: bytes) -> Tuple[int, int]:
    data = src.read_bytes()
    pt = get_cipher(key).decrypt(data)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(pt)
    return (len(data), len(pt))
