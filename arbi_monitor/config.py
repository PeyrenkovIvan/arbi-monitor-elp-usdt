from decimal import Decimal

# DexScreener
DEX_CHAIN = "ethereum"
DEX_PAIR_ADDRESS = "0x6b4ecec31b33aeee49f2a2ac09690b275cdf79beab4ab75b39180ad32dd27a88"

# KuCoin
KUCOIN_SYMBOL = "ELP-USDT"

# Параметры мониторинга
THRESHOLD_FRAC = Decimal("0.07")   # 3%
INTERVAL_SEC   = 10                 # опрос каждые 5 секунд
COOLDOWN_SEC   = 3 * 60           # 10 минут

# Управление
USE_TELEGRAM = False
SECRETS_FILE = "tg.json"

ALERTS_FILE  = "alerts.txt"

# HTTP
REQ_TIMEOUT  = 5
RETRIES      = 2
