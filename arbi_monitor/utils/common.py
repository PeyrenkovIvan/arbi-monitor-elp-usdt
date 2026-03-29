# utils/common.py
from datetime import datetime, timezone
from decimal import Decimal
from typing import Union

def now_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")

def append_alert_line(filepath: str, line: str) -> None:
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(line + "\n")

Number = Union[int, float, Decimal]

def rate_percent(a: Number, b: Number) -> Decimal:
    da = Decimal(str(a))
    db = Decimal(str(b))
    low = min(da, db)
    high = max(da, db)
    if low == 0:
        return Decimal("0")
    return (high - low) / low
