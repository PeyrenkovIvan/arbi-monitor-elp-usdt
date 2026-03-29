# notifier/telegram.py
import requests
import sys
from typing import Optional

from utils import get_secret

def send_telegram(
    text: str,
    secrets_file: str,
    timeout: int = 5,
    token: Optional[str] = None,
    chat_id: Optional[str] = None,
) -> None:
    token = token or get_secret(secrets_file, "TELEGRAM_TOKEN")
    chat_id = chat_id or get_secret(secrets_file, "TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[warn] TELEGRAM_TOKEN/TELEGRAM_CHAT_ID не заданы — пропускаю отправку.", file=sys.stderr)
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",   # <-- включаем поддержку Markdown
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, data=payload, timeout=timeout)
        r.raise_for_status()
    except Exception as e:
        print(f"[error] Telegram send failed: {e}", file=sys.stderr)
