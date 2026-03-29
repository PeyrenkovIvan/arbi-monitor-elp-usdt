# datasources/kucoin.py
from decimal import Decimal, InvalidOperation
from typing import Optional
import time
import requests

def _http_get_json(url: str, params: Optional[dict] = None, timeout: int = 5, retries: int = 2) -> dict:
    last_exc = None
    for attempt in range(retries + 1):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_exc = e
            time.sleep(0.3 * (attempt + 1))
    raise last_exc

def get_price_kucoin(symbol: str, timeout: int = 5, retries: int = 2) -> Decimal:
    """
    Возвращает level1 price для спот-символа KuCoin, например ELP-USDT:
    GET /api/v1/market/orderbook/level1?symbol=ELP-USDT
    """
    url = "https://api.kucoin.com/api/v1/market/orderbook/level1"
    data = _http_get_json(url, params={"symbol": symbol}, timeout=timeout, retries=retries)

    code = str(data.get("code", "200000"))
    if code != "200000":
        raise RuntimeError(f"KuCoin: неожиданный code: {code}")

    d = data.get("data") or {}
    price = d.get("price")
    if price is None:
        raise RuntimeError("KuCoin: нет поля data.price")

    try:
        return Decimal(str(price))
    except InvalidOperation:
        raise RuntimeError(f"KuCoin: не удалось распарсить цену: {price!r}")
