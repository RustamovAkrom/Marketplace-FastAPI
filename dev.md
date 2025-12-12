# 🛒 E-Commerce API (FastAPI)


## 🚀 Features

* 🔐 Authentication & Authorization (JWT)
* 📦 Product, Category & Image Management
* 🛒 Cart, Checkout & Orders
* 💳 Stripe Payment Integration
* 📊 Monitoring with Prometheus + Grafana
* 🐞 Logging & Error Tracking with Sentry
* 🧵 Background Tasks (Celery + Flower)
* 🧪 Full Testing Suite (pytest)
* 💅 Code Quality Tools: ruff, black, isort, mypy
* 🛡 Security Layers: bandit, detect-secrets, pip-audit, safety

---

## 📦 Dependencies

 - [aiofiles](https://github.com/Tinche/aiofiles): Async file I/O
 - [aiosqlite](https://github.com/omnilib/aiosqlite): Async SQLite driver
 - [alembic](https://github.com/sqlalchemy/alembic): Database migrations
 - [argon2-cffi](https://github.com/hynek/argon2-cffi): Password hashing
 - [bandit](https://github.com/PyCQA/bandit): Security analysis
 - [black](https://github.com/psf/black): Code formatter
 - [celery](https://github.com/celery/celery): Task queue system
 - [cryptography](https://github.com/pyca/cryptography): Cryptographic library
 - [detect-secrets](https://github.com/Yelp/detect-secrets): Secret scanner
 - [fastapi](https://github.com/fastapi/fastapi): Web framework
 - [fastapi-mail](https://github.com/sabuhish/fastapi-mail): Email sending
 - [flower](https://github.com/mher/flower): Celery monitoring UI
 - [httpx](https://github.com/encode/httpx): Async HTTP client
 - [isort](https://github.com/PyCQA/isort): Import sorter
 - [loguru](https://github.com/Delgan/loguru): Logging library
 - [mypy](https://github.com/python/mypy): Static type checker
 - [orjson](https://github.com/ijl/orjson): Fast JSON serialization
 - [passlib](https://github.com/passlib/passlib): Password hashing utilities
 - [pip-audit](https://github.com/pypa/pip-audit): Vulnerability scanner
 - [pre-commit](https://github.com/pre-commit/pre-commit): Git hooks manager
 - [prometheus-fastapi-instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator): Metrics exporter
 - [psycopg](https://github.com/psycopg/psycopg): PostgreSQL driver
 - [pydantic-settings](https://github.com/pydantic/pydantic-settings): Config management
 - [pydantic](https://github.com/pydantic/pydantic): Data validation
 - [pyjwt](https://github.com/jpadilla/pyjwt): JWT handling
 - [pytest](https://github.com/pytest-dev/pytest): Testing framework
 - [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio): Async tests
 - [pytest-cov](https://github.com/pytest-dev/pytest-cov): Coverage reports
 - [python-dotenv](https://github.com/theskumar/python-dotenv): Environment loader
 - [python-jose](https://github.com/mpdavis/python-jose): JWT + Crypto
 - [python-multipart](https://github.com/andrew-d/python-multipart): Multipart form parser
 - [ruff](https://github.com/astral-sh/ruff): Linter & formatter
 - [safety](https://github.com/pyupio/safety): Security auditing
 - [sentry-sdk](https://github.com/getsentry/sentry-python): Error tracking
 - [stripe](https://github.com/stripe/stripe-python): Payments API
 - [uvicorn](https://github.com/encode/uvicorn): ASGI server

## 🚀 How to Run the Project

There are **two ways** to start the E-Commerce API:


### **1️⃣ Run with Docker (Recommended)**

Make sure you have **Docker** and **Docker Compose** installed.

### **Start the project**

```bash
docker compose up --build
```

### **Stop the project**

```bash
docker compose down
```

### The API will be available at:

```
http://localhost:8000
```

---

## **2️⃣ Run Locally with Uvicorn**

### **1. Install dependencies**

```bash
pip install -r requirements.txt
```

or (if using pyproject.toml)

```bash
uv pip install . # or use "uv sync"
```

### **2. Configure environment**

Create `.env` file:

```bash
cp .env-example .env
```

Update your DB URL, secret keys, etc.

### **3. Run database migrations**

```bash
alembic upgrade head
```

### **4. Start the server**

```bash
uvicorn dev:app --app-dir src --host 0.0.0.0 --port 8000 --reload
```
