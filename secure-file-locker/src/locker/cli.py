from __future__ import annotations
import argparse
from pathlib import Path
from locker.config import Config
from locker.logging_utils import setup_logger
from locker.crypto import encrypt_file, decrypt_file, generate_key
from locker.key_management import save_raw_key, load_raw_key
from safeguards.guardrails import preflight_checks
from safeguards.canary import enforce_canary

def iter_target_files(root: Path, excludes, max_mb: int):
    for p in root.rglob("*"):
        if p.is_file() and all(ex not in str(p) for ex in excludes) and p.stat().st_size <= max_mb * 1024 * 1024:
            yield p

def main():
    ap = argparse.ArgumentParser(prog="sfl", description="Secure File Locker (safe-by-default)")
    ap.add_argument("command", choices=["encrypt", "decrypt", "backup", "restore", "gen-key"])
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--keyfile", type=Path, default=Path(".sfl-key"))
    ap.add_argument("--dry-run", action="store_true", help="simulate; no files changed")
    ap.add_argument("--canary", action="store_true", help="operate on *.CANARY files only")
    ap.add_argument("--max-mb", type=int, default=50)
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    cfg = Config(allowlist_dir=args.root, dry_run=args.dry_run, max_file_size_mb=args.max_mb, log_level=args.log_level)
    log = setup_logger(cfg.log_level)
    preflight_checks(cfg)
    if args.canary:
        enforce_canary(cfg.allowlist_dir)

    if args.command == "gen-key":
        key = generate_key()
        if cfg.dry_run:
            log.info("DRY-RUN: would write key to %s", extra={})
        else:
            save_raw_key(key, args.keyfile)
            log.info("key_saved")
        return

    key = load_raw_key(args.keyfile)

    if args.command == "encrypt":
        for p in iter_target_files(cfg.allowlist_dir, cfg.excludes, cfg.max_file_size_mb):
            dst = p.with_suffix(p.suffix + ".enc")
            if cfg.dry_run:
                log.info(f'{{"action":"encrypt","src":"{p}","dst":"{dst}"}}')
            else:
                encrypt_file(p, dst, key)
                log.info(f'{{"action":"encrypted","src":"{p}","dst":"{dst}"}}')

    elif args.command == "decrypt":
        for p in cfg.allowlist_dir.rglob("*.enc"):
            dst = p.with_suffix("")
            if cfg.dry_run:
                log.info(f'{{"action":"decrypt","src":"{p}","dst":"{dst}"}}')
            else:
                decrypt_file(p, dst, key)
                log.info(f'{{"action":"decrypted","src":"{p}","dst":"{dst}"}}')

    elif args.command == "backup":
        from locker.backup import backup_file
        for p in iter_target_files(cfg.allowlist_dir, cfg.excludes, cfg.max_file_size_mb):
            if cfg.dry_run:
                log.info(f'{{"action":"backup","src":"{p}"}}')
            else:
                b = backup_file(p, cfg.backup_dir)
                log.info(f'{{"action":"backed_up","src":"{p}","backup":"{b}"}}')

    elif args.command == "restore":
        from locker.restore import restore_file
        for b in cfg.backup_dir.glob("*.bak"):
            dst = cfg.allowlist_dir / b.name.split(".")[0]
            if cfg.dry_run:
                log.info(f'{{"action":"restore","backup":"{b}","dst":"{dst}"}}')
            else:
                restore_file(b, dst)
                log.info(f'{{"action":"restored","backup":"{b}","dst":"{dst}"}}')

if __name__ == "__main__":
    main()
