# -*- coding: utf-8 -*-
import time
from decimal import Decimal
from dotenv import load_dotenv

from config import (
    DEX_CHAIN,
    DEX_PAIR_ADDRESS,
    KUCOIN_SYMBOL,
    THRESHOLD_FRAC,
    INTERVAL_SEC,
    COOLDOWN_SEC,
    USE_TELEGRAM,
    ALERTS_FILE,
    SECRETS_FILE,
)

from datasources.dexscreener import get_price_dex
from datasources.kucoin import get_price_kucoin
from notifier.telegram import send_telegram
from utils import now_utc_iso, append_alert_line, rate_percent, setup_logging


def main():
    load_dotenv(SECRETS_FILE)

    logs = setup_logging()
    log = logs["app_logger"]
    alog = logs["alerts_logger"]

    print("[info] Старт мониторинга ELP (DEX ↔ KuCoin)")
    print(f"[info] DEX: {DEX_CHAIN}/{DEX_PAIR_ADDRESS} | CEX: KuCoin {KUCOIN_SYMBOL}")
    print(f"[info] Порог алерта: {THRESHOLD_FRAC*100:.2f}% | Интервал: {INTERVAL_SEC}s | Таймаут: {COOLDOWN_SEC}s")

    last_alert_time = 0.0

    while True:
        try:
            dex_price = Decimal(get_price_dex(DEX_CHAIN, DEX_PAIR_ADDRESS))
            cex_price = Decimal(get_price_kucoin(KUCOIN_SYMBOL))

            diff_pct = rate_percent(dex_price, cex_price)  # (dex/cex - 1)*100

            log.info(f"DEX={dex_price} | CEX={cex_price} | Δ={diff_pct:.2f}%")

            # ИЗМЕНЕНО: триггер только если DEX > CEX и спред >= порога
            if (dex_price > cex_price) and (diff_pct >= THRESHOLD_FRAC * 100):
                now = time.time()
                if now - last_alert_time > COOLDOWN_SEC:
                    msg = (
                        f"[ELP] ALERT {now_utc_iso()} Δ={diff_pct:.2f}% (DEX выше KuCoin)\n"
                        f"DEX={dex_price}\nCEX={cex_price}\n"
                        f"Пара: {DEX_CHAIN}/{DEX_PAIR_ADDRESS} | {KUCOIN_SYMBOL}"
                    )
                    append_alert_line(ALERTS_FILE, msg)
                    alog.warning(msg)
                    if USE_TELEGRAM:
                        send_telegram(msg)
                    last_alert_time = now

        except Exception as e:
            log.error(f"Ошибка цикла: {e}")

        time.sleep(INTERVAL_SEC)


if __name__ == "__main__":
    main()
