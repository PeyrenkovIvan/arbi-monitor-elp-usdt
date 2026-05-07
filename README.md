# 🔍 Arbitrage Monitor (ELP / USDT)

Система мониторинга арбитражных возможностей для пары ELP/USDT с автоматическим анализом рыночных данных и уведомлениями в Telegram.

---

# 📌 Описание проекта

Arbitrage Monitor — это lightweight monitoring service, предназначенный для отслеживания разницы цен между централизованными и децентрализованными источниками ликвидности.

Проект получает данные в реальном времени из KuCoin и DexScreener, рассчитывает процентный спред между ценами и отправляет уведомления при обнаружении потенциальной арбитражной возможности.

Основная задача проекта — сократить время реакции трейдера на рыночные изменения и автоматизировать процесс мониторинга торговых возможностей.

---

# 🎯 Цель проекта

Проект создавался как практический инструмент для:

* мониторинга арбитражных ситуаций;
* работы с финансовыми API;
* построения real-time monitoring systems;
* обработки рыночных данных;
* автоматизации уведомлений;
* демонстрации модульной архитектуры monitoring services.

Также проект выступает как технический showcase:

* работы с API,
* resilient/fallback логики,
* structured logging,
* обработки ошибок,
* финансовых вычислений с Decimal.

---

# ⚙️ Основной функционал

* 📡 Получение рыночных данных через API
* 🔄 Сравнение цен между DEX и CEX
* 🧮 Расчет процентного спреда
* 🔔 Telegram-уведомления при достижении заданного порога
* ⚙️ Настройка порогов и интервалов мониторинга
* 🧾 JSON structured logging
* 📁 Ротация и очистка логов
* 🛡 Retry/fallback механизмы при работе с API
* 💰 Financial-safe calculations через Decimal
* 📊 Liquidity-aware выбор торговых пар

---

# 🏗 Архитектура проекта

Проект построен по модульному принципу и разделён на несколько слоёв:

```bash
arbi_monitor/
│
├── datasources/      # Интеграции с биржами и market data providers
├── notifier/         # Telegram notification layer
├── utils/            # Общие utility-модули
│
├── monitor.py        # Основная логика мониторинга
├── config.py         # Централизованная конфигурация
├── alerts.txt        # История alert-событий
└── requirements.txt
```

---

# 📂 Основные модули

## datasources/

Отвечает за получение рыночных данных.

Реализованы:

* отдельные datasource providers;
* retry handling;
* timeout handling;
* fallback logic;
* liquidity-based pair selection.

### Поддерживаемые источники:

* DexScreener
* KuCoin

---

## notifier/

Система уведомлений.

Telegram вынесен в отдельный notification layer, что позволяет легко расширять проект:

* Discord
* Slack
* Email
* Webhooks

---

## utils/

Набор вспомогательных модулей:

* structured logging;
* secrets management;
* reusable helper functions;
* financial calculations.

---

# 🛠 Технологический стек

* Python
* REST API
* Telegram Bot API
* Decimal financial calculations
* JSON structured logging
* Timed rotating logs
* Retry/Fallback architecture

---

# 🚀 Установка и запуск

## 1. Клонирование репозитория

```bash
git clone <repository_url>
cd arbi_monitor
```

## 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 3. Настройка конфигурации

Отредактируйте:

```bash
config.py
```

Укажите:

* торговую пару;
* параметры мониторинга;
* spread threshold;
* Telegram settings;
* пути логирования.

---

## 4. Настройка secrets

Создайте JSON-файл с секретами:

```json
{
  "TELEGRAM_TOKEN": "your_token",
  "TELEGRAM_CHAT_ID": "your_chat_id"
}
```

---

## 5. Запуск проекта

```bash
python monitor.py
```

---

# 📊 Какие задачи решает проект

Проект помогает:

* автоматизировать мониторинг рынка;
* сократить ручной анализ;
* ускорить реакцию на рыночные изменения;
* централизовать обработку market data;
* автоматически получать сигналы о возможных арбитражных ситуациях.

---

# 🔥 Технические особенности

## Resilient API Integration

Система использует retry/fallback механизмы для повышения стабильности работы с внешними API.

## Structured Logging

Реализованы:

* JSON logs;
* log rotation;
* alert-specific logs;
* automatic cleanup.

## Financial Precision

Все финансовые вычисления выполняются через Decimal для избежания ошибок float arithmetic.

## Extensible Architecture

Проект легко расширяется:

* новыми биржами;
* notification providers;
* торговыми парами;
* аналитическими модулями.

---

# ⚠️ Ограничения

На текущем этапе проект:

* не выполняет сделки автоматически;
* работает как monitoring/alerting system;
* использует polling вместо websocket streams;
* не содержит dashboard/UI;
* не использует database storage.

---

# 🔧 Возможные улучшения

* Multi-pair monitoring
* WebSocket market feeds
* Database integration
* Web dashboard
* Historical analytics
* Docker support
* Async architecture
* Auto-trading execution
* Multi-exchange orchestration
* Metrics & observability

# 🔍 Arbitrage Monitor (ELP / USDT)

A real-time arbitrage monitoring system for the ELP/USDT trading pair with automated market analysis and Telegram alert notifications.

---

# 📌 Project Description

Arbitrage Monitor is a lightweight monitoring service designed to detect price differences between centralized and decentralized liquidity sources.

The project retrieves real-time market data from KuCoin and DexScreener, calculates percentage spreads between prices, and sends Telegram alerts whenever a potential arbitrage opportunity is detected.

The primary goal of the project is to reduce trader reaction time and automate market opportunity monitoring.

---

# 🎯 Project Goal

This project was created as a practical tool for:

* arbitrage opportunity monitoring;
* financial API integration;
* building real-time monitoring systems;
* market data processing;
* notification automation;
* demonstrating modular monitoring service architecture.

The project also serves as a technical showcase for:

* resilient API integrations;
* fallback/retry mechanisms;
* structured logging;
* exception handling;
* Decimal-based financial calculations.

---

# ⚙️ Core Features

* 📡 Real-time market data retrieval via API
* 🔄 DEX/CEX price comparison
* 🧮 Percentage spread calculation
* 🔔 Telegram alert notifications
* ⚙️ Configurable monitoring thresholds and intervals
* 🧾 JSON structured logging
* 📁 Log rotation and cleanup
* 🛡 Retry/fallback API mechanisms
* 💰 Financial-safe Decimal calculations
* 📊 Liquidity-aware pair selection

---

# 🏗 Project Architecture

The project follows a modular architecture with separated service layers:

```bash
arbi_monitor/
│
├── datasources/      # Exchange and market data integrations
├── notifier/         # Telegram notification layer
├── utils/            # Shared utility modules
│
├── monitor.py        # Core monitoring loop
├── config.py         # Centralized configuration
├── alerts.txt        # Alert history storage
└── requirements.txt
```

---

# 📂 Main Modules

## datasources/

Responsible for market data retrieval.

Implemented features:

* separate datasource providers;
* retry handling;
* timeout handling;
* fallback logic;
* liquidity-based pair selection.

### Supported sources:

* DexScreener
* KuCoin

---

## notifier/

Notification delivery system.

Telegram integration is separated into its own notification layer, allowing easy future extensions:

* Discord
* Slack
* Email
* Webhooks

---

## utils/

Shared utility layer containing:

* structured logging;
* secrets management;
* reusable helper functions;
* financial calculations.

---

# 🛠 Tech Stack

* Python
* REST API
* Telegram Bot API
* Decimal financial calculations
* JSON structured logging
* Timed rotating logs
* Retry/Fallback architecture

---

# 🚀 Installation & Usage

## 1. Clone repository

```bash
git clone <repository_url>
cd arbi_monitor
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure project

Edit:

```bash
config.py
```

Configure:

* trading pair;
* monitoring parameters;
* spread thresholds;
* Telegram settings;
* logging paths.

---

## 4. Configure secrets

Create a JSON secrets file:

```json
{
  "TELEGRAM_TOKEN": "your_token",
  "TELEGRAM_CHAT_ID": "your_chat_id"
}
```

---

## 5. Run the project

```bash
python monitor.py
```

---

# 📊 Problems Solved by the Project

This project helps:

* automate market monitoring;
* reduce manual analysis;
* improve reaction speed to market events;
* centralize market data processing;
* automatically detect potential arbitrage opportunities.

---

# 🔥 Technical Highlights

## Resilient API Integration

The system uses retry/fallback mechanisms to improve reliability when working with external APIs.

## Structured Logging

Implemented:

* JSON logs;
* log rotation;
* alert-specific logs;
* automatic cleanup.

## Financial Precision

All financial calculations use Decimal to avoid floating-point arithmetic errors.

## Extensible Architecture

The project can be easily extended with:

* new exchanges;
* additional notification providers;
* more trading pairs;
* analytics modules.

---

# ⚠️ Current Limitations

At its current stage, the project:

* does not execute trades automatically;
* works as a monitoring/alerting system;
* uses polling instead of websocket streams;
* has no dashboard/UI;
* does not use database storage.

---

# 🔧 Possible Improvements

* Multi-pair monitoring
* WebSocket market feeds
* Database integration
* Web dashboard
* Historical analytics
* Docker support
* Async architecture
* Auto-trading execution
* Multi-exchange orchestration
* Metrics & observability
