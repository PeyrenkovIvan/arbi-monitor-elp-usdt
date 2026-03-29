# datasources/dexscreener.py
from decimal import Decimal, InvalidOperation
from typing import Optional, List, Dict, Any
import time
import requests
import sys
import json

def _http_get_json(url: str, params: Optional[dict] = None, timeout: int = 5, retries: int = 2) -> dict:
    last_exc = None
    headers = {"User-Agent": "arbi-monitor/1.0"}
    for attempt in range(retries + 1):
        try:
            r = requests.get(url, params=params, timeout=timeout, headers=headers)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_exc = e
            time.sleep(0.3 * (attempt + 1))
    raise last_exc

def _pick_price_from_pair(p: Dict[str, Any]) -> Decimal:
    price_usd = p.get("priceUsd") or p.get("price") or p.get("priceNative")
    if price_usd is None:
        raise RuntimeError("DexScreener: нет поля priceUsd/price/priceNative в объекте пары")
    try:
        return Decimal(str(price_usd))
    except InvalidOperation:
        raise RuntimeError(f"DexScreener: не удалось распарсить цену: {price_usd!r}")

def _best_pair_by_liquidity(pairs: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not pairs:
        return None
    def liq_usd(p):
        liq = p.get("liquidity") or {}
        return Decimal(str(liq.get("usd", "0"))) if "usd" in liq else Decimal("0")
    return max(pairs, key=liq_usd)

def get_price_dex(chain: str, address: str, timeout: int = 5, retries: int = 2) -> Decimal:
    # 1) Прямая попытка как пара
    url_pair = f"https://api.dexscreener.com/latest/dex/pairs/{chain}/{address}"
    data = _http_get_json(url_pair, timeout=timeout, retries=retries)
    pairs = data.get("pairs") or []
    if pairs:
        return _pick_price_from_pair(pairs[0])

    try:
        print("[debug] DexScreener /pairs empty. Raw:", json.dumps(data)[:600], file=sys.stderr)
    except Exception:
        pass

    # 2) Поиск по адресу (может вернуть пару или токеновые пары)
    url_search = "https://api.dexscreener.com/latest/dex/search"
    s_data = _http_get_json(url_search, params={"q": address}, timeout=timeout, retries=retries)
    s_pairs = s_data.get("pairs") or []

    exact = [p for p in s_pairs
             if str(p.get("pairAddress", "")).lower() == address.lower()
             and str(p.get("chainId", "")).lower() == chain.lower()]
    if exact:
        return _pick_price_from_pair(exact[0])

    try:
        print("[debug] DexScreener /search candidates:", json.dumps(s_pairs[:3])[:600], file=sys.stderr)
    except Exception:
        pass

    # 3) Похоже, это не пара, а токен — пробуем /tokens/{tokenAddress}
    url_token = f"https://api.dexscreener.com/latest/dex/tokens/{address}"
    t_data = _http_get_json(url_token, timeout=timeout, retries=retries)
    t_pairs = t_data.get("pairs") or []

    t_pairs_chain = [p for p in t_pairs if str(p.get("chainId", "")).lower() == chain.lower()]
    best = _best_pair_by_liquidity(t_pairs_chain) or _best_pair_by_liquidity(t_pairs)
    if not best:
        try:
            print("[debug] DexScreener /tokens empty. Raw:", json.dumps(t_data)[:600], file=sys.stderr)
        except Exception:
            pass
        raise RuntimeError("DexScreener: не удалось найти подходящую пару ни через /pairs, ни через /search, ни через /tokens")

    return _pick_price_from_pair(best)
