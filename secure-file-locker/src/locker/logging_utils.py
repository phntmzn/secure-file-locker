from __future__ import annotations
import logging, json, sys
def setup_logger(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("secure_file_locker")
    if logger.handlers:  # idempotent
        return logger
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    h = logging.StreamHandler(sys.stdout)
    def fmt(record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "msg": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
        }
        return json.dumps(payload, ensure_ascii=False)
    h.setFormatter(logging.Formatter(fmt="%(message)s"))
    logger.addHandler(h)
    return logger
