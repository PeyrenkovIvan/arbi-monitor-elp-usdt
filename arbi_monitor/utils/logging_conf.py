# utils/logging_conf.py
import logging
import os
import json
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta

def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "lvl": record.levelname,
            "name": record.name,
            "msg": record.getMessage(),
        }
        if record.__dict__.get("extra"):
            payload.update(record.__dict__["extra"])
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)

def _cleanup_old_logs(log_dir: str, keep_hours: int = 24):
    cutoff = datetime.utcnow() - timedelta(hours=keep_hours)
    for fn in os.listdir(log_dir):
        if not fn.endswith(".log") and ".log." not in fn:
            continue
        full = os.path.join(log_dir, fn)
        try:
            mtime = datetime.utcfromtimestamp(os.path.getmtime(full))
            if mtime < cutoff:
                os.remove(full)
        except Exception:
            pass

def setup_logging():
    log_dir = os.getenv("LOG_DIR", "logs")
    _ensure_dir(log_dir)

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Консоль (короткий текст)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(name)s | %(message)s"))
    root.addHandler(ch)

    # app.log (JSON)
    app_path = os.path.join(log_dir, "app.log")
    fh_app = TimedRotatingFileHandler(app_path, when="midnight", interval=1, backupCount=2, utc=True, encoding="utf-8")
    fh_app.setLevel(logging.INFO)
    fh_app.setFormatter(JsonFormatter())
    root.addHandler(fh_app)

    # alerts.log
    alerts_path = os.path.join(log_dir, "alerts.log")
    fh_alerts = TimedRotatingFileHandler(alerts_path, when="midnight", interval=1, backupCount=2, utc=True, encoding="utf-8")
    fh_alerts.setLevel(logging.INFO)
    fh_alerts.setFormatter(logging.Formatter("%(message)s"))
    alerts_logger = logging.getLogger("alerts")
    alerts_logger.setLevel(logging.INFO)
    alerts_logger.addHandler(fh_alerts)

    # уборка старых файлов старше 24 часов
    _cleanup_old_logs(log_dir, keep_hours=24)

    return {
        "app_logger": logging.getLogger("app"),
        "alerts_logger": alerts_logger,
    }
