# 🧩 1) Архитектурная структура Marketplace (DDD + Clean Architecture)

```
src/
 ├── api/                   # FastAPI endpoints (HTTP вход)
 │    ├── v1/
 │    │    ├── auth/
 │    │    ├── users/
 │    │    ├── products/
 │    │    ├── orders/
 │    │    ├── payments/
 │    │    ├── reviews/
 │    │    ├── shipment/
 │    │    ├── notifications/
 │    │    └── analytics/
 │    └── dependencies/
 │
 ├── core/
 │    ├── config.py
 │    ├── security.py
 │    ├── exceptions/
 │    ├── logging.py
 │    ├── middleware/
 │    └── rate_limiter.py
 │
 ├── domain/               # Бизнес-логика (чистая)
 │    ├── users/
 │    ├── products/
 │    ├── orders/
 │    ├── payments/
 │    ├── shipment/
 │    ├── reviews/
 │    ├── notifications/
 │    └── analytics/
 │
 ├── services/             # Сервисные слои
 │    ├── auth.py
 │    ├── product_service.py
 │    ├── order_service.py
 │    ├── payment_service.py
 │    ├── shipment_service.py
 │    ├── search_service.py
 │    └── email_service.py
 │
 ├── db/
 │    ├── base.py
 │    ├── session.py
 │    └── migrations/
 │
 ├── repositories/
 │    ├── user_repo.py
 │    ├── product_repo.py
 │    ├── order_repo.py
 │    └── payment_repo.py
 │
 ├── schemas/
 │    ├── auth.py
 │    ├── users.py
 │    ├── products.py
 │    ├── orders.py
 │    ├── payments.py
 │    └── shipment.py
 │
 ├── utils/
 │    ├── validators.py
 │    ├── image_processor.py
 │    ├── jwt_manager.py
 │    └── pagination.py
 │
 └── main.py
```

---

# 🔒 2) Безопасность Marketplace (ТОП — must have)

## 🔥 JWT безопасность уровня Production

* Access token: 5–15 min
* Refresh token: 7–30 days
* JTI (unique token ID)
* Blacklist Revoked Tokens (Redis)
* Rotate refresh tokens (как у Google)
* IP + User-Agent binding (опционально)

## 🔐 OAuth 2.0 / Social Login

* Google
* GitHub
* Apple
* Facebook

## 🔒 Advanced защита

* Rate Limiting (Redis)
* Brute force protection
* CAPTCHA (hCaptcha / Cloudflare Turnstile)
* SQL Injection protection (ORM + validators)
* CORS security
* CSRF для админ-панели
* File upload sanitizer (для images)
* Content Security Policy (CSP)
* Password Pepper (не только Salt)

---

# 👤 3) User System (продвинутая модель)

## Пользователь имеет:

* Профиль
* Роли:

  * **Customer**
  * **Seller**
  * **Courier**
  * **Admin**
  * **Support**
* Баланс
* Токены (refresh + revoked)
* История заказов
* Адреса
* Избранное

## Функции

* Регистрация
* Email verification
* Multi-session support (несколько устройств)
* Password reset
* Device management
* Two-Factor Auth (TOTP)

---

# 🛒 4) Product System — самое важное

## Модель товара включает:

* Название + описание + характеристики
* Фото (несколько)
* Цена, скидка, комиссия
* Вариации (цвет, размер)
* Категории + подкатегории + теги
* Остатки на складе
* Количество продаж
* Средняя оценка + отзывы
* Продавец (Seller)

## Функции:

* Поиск товаров
* Фильтры (цена, рейтинг, доставка)
* Индексация в Search Engine (Elasticsearch / Meilisearch)
* Обновление остатков
* Рекомендации (на основе покупок)

---

# 📦 5) Корзина + Заказы (Order System)

## Включает:

* OrderItem[]
* Промокоды
* Доставка и расчёт стоимости
* Способы оплаты
* Статусы заказов:

  * CREATED
  * PAID
  * PROCESSING
  * SHIPPED
  * DELIVERED
  * CANCELLED
  * RETURNED

## Функции:

* Создание заказа
* Подтверждение оплаты
* Интеграция с платежными системами
* Расчёт налога / комиссии
* Уведомления (email, telegram, sms)

---

# 💳 6) Payment System (Обязательно)

Интеграции:

* Stripe
* PayPal
* Click / Payme (Узбекистан)
* YooKassa (Россия)
* Crypto USDT/TRC20 (опционально)

Функции:

* Webhooks
* Payment Confirmations
* Refunds (возвраты)
* Partial refunds
* Payment receipt generation (PDF)

---

# 🚚 7) Delivery System (Shipment)

## Интеграции:

* DHL / UPS
* PonyExpress
* CDEK
* UzPost
* Local курьеры

## Функции:

* Расчёт доставки по весу и габаритам
* Трекинг посылки
* Адресная доставка
* Пункты выдачи
* Смена адреса до отправки

---

# ⭐ 8) Reviews + Ratings

* Система отзывов + оценок
* Фото-отзывы
* Модерация отзывов (AI)
* Жалобы на продавцов
* Подтверждённые покупки

---

# 🔍 9) Search Engine (как у крупных marketplace)

## Технологии:

* Elasticsearch
* Meilisearch
* OpenSearch

## Функции:

* полнотекстовый поиск
* autosuggest
* похожие товары
* сортировка по популярности и рейтингу

---

# 🔔 10) Notifications System

Использует брокер сообщений:

* Redis Streams
* RabbitMQ
* Kafka

## Каналы:

* Email (SMTP / SendGrid)
* SMS (Twilio, Eskiz)
* Telegram Bot
* WebPush
* Admin notifications

---

# 🧠 11) Analytics & Reporting

* Метрики заказов
* Метрики товаров
* Метрики продавцов
* Мониторинг (Grafana + Prometheus)
* Логи (ELK: Elasticsearch + Logstash + Kibana)

---

# 📁 12) Media Service

* Хранение картинок:

  * S3 Compatible: MinIO / AWS S3
* Изменение размеров изображений
* WebP оптимизация
* CDN integration

---

# 🧪 13) Testing Level

* Unit tests
* Integration tests
* E2E tests
* Load testing (Locust)
* API contract tests

---

# ⚙️ 14) DevOps Infrastructure

* Docker + Docker Compose
* CI/CD (GitHub Actions)
* Alembic migrations
* Reverse proxy: Nginx
* HTTPS via Certbot
* Environment secrets (Vault)

---

# 🔥 15) Seller System (маркетплейс обязательно)

* Регистрация продавца
* Проверка документов (KYC)
* Баланс продавца
* Выплаты (payouts)
* Комиссия Marketplace
* Статистика продавца
* Управление товарами

---

# 🧩 16) Админ Панель

* Управление пользователями
* Управление продавцами
* Финансовая аналитика
* Настройка категорий
* Логи
* Модерация отзывов

---

# 🧱 17) НЕОБХОДИМЫЕ внешние сервисы

| Направление | Инструменты          |
| ----------- | -------------------- |
| База данных | PostgreSQL           |
| Кеш         | Redis                |
| Поиск       | Elasticsearch        |
| Логи        | ELK                  |
| Мониторинг  | Grafana + Prometheus |
| Файлы       | Minio                |
| Очереди     | RabbitMQ / Kafka     |
| CDN         | Cloudflare           |
