# 🏗 Project Infrastructure & Architecture

## 1️⃣ Project Overview

* **Backend framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy + Alembic (migrations)
* **Task queue / async jobs:** Celery + Flower
* **API docs:** OpenAPI (Swagger)
* **Monitoring:** Prometheus + Grafana
* **Logging & error tracking:** Sentry
* **Security & CI/CD:** Dependabot, CodeQL, pre-commit hooks, pip-audit, Bandit, Safety
* **Payment gateway:** Stripe
* **Email service:** FastAPI-Mail
* **Testing:** pytest + pytest-asyncio + pytest-cov

---

## 2️⃣ Folder & Module Structure

```
e-commerce/
├── src/                       
│   ├── main.py                 # Entry point for Uvicorn/Docker
│   ├── core/                   # Core application settings and configuration
│   │   ├── config/             # Config modules
│   │   │   ├── base.py         # Base settings (Pydantic BaseSettings)
│   │   │   ├── broker.py       # Celery broker configuration
│   │   │   ├── database.py     # Database connection & engine
│   │   │   └── email.py        # Email service configuration
│   │   └── security.py         # Security utilities (JWT, password hashing)
│   ├── db/                     # Database models & migrations
│   │   ├── models/             # SQLAlchemy models
│   │   ├── base.py             # Base model class
│   │   └── alembic/            # Migrations folder
│   ├── api/                    # Routers & endpoints
│   │   ├── v1/                 # Versioned API
│   │   └── dependencies/       # Dependencies (auth, permissions)
│   ├── services/               # Business logic & integrations
│   │   ├── email_service.py
│   │   ├── payment_service.py
│   │   └── celery_tasks.py
│   ├── schemas/                # Pydantic models (request/response)
│   ├── utils/                  # Helper functions & utilities
│   └── tests/                  # Unit and integration tests
│
├── docker/                      # Docker and container configs
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .github/                     # GitHub workflows & CI/CD configs
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── codeql-analysis.yml
│   │   └── security.yml
│   ├── dependabot.yml
│   └── CODEOWNERS
│
├── scripts/                     # Utility scripts (DB, Celery, migrations)
├── .env-example                 # Example environment variables
├── pyproject.toml               # Project dependencies & build config
├── README.md
└── docs/                        # Documentation files
    ├── ci-cd-security.md
    └── infrastructure.md
```

---

## 3️⃣ Infrastructure Components

### **3.1 Application**

* Runs on **Uvicorn** (ASGI server)
* Uses FastAPI for REST API and async support

### **3.2 Configuration (`src/core/config/`)**

* `base.py` — base settings (Pydantic)
* `database.py` — PostgreSQL connection & session management
* `broker.py` — Celery broker and backend configuration
* `email.py` — FastAPI-Mail configuration

### **3.3 Database**

* PostgreSQL as main DB
* SQLAlchemy ORM + Alembic migrations

### **3.4 Task Queue**

* Celery handles async jobs (email, payment)
* Flower for monitoring
* Broker: Redis or RabbitMQ

### **3.5 Monitoring & Logging**

* Prometheus metrics via `prometheus-fastapi-instrumentator`
* Grafana dashboard for metrics visualization
* Sentry for error tracking

### **3.6 CI/CD & Security**

* GitHub Actions for pipelines
* Dependabot updates dependencies automatically
* CodeQL scans for vulnerabilities
* pre-commit hooks: linters, type checks, secret scanning
* pip-audit, Bandit, Safety run in CI

### **3.7 Deployment**

* Dockerized for local and production deployment
* `docker-compose.yml` orchestrates services: app, DB, Celery, Flower

---

## 4️⃣ Suggested Workflow

1. **Local development:**

   * Run pre-commit checks: `uv run pre-commit run --all-files`
   * Run tests: `uv run pytest -v`
   * Type checking: `uv run mypy src/`

2. **CI/CD (GitHub Actions):**

   * Runs tests, linters, security scans automatically

3. **Deployment:**

   * Docker / Docker Compose
   * Optional: Kubernetes or cloud hosting for scaling
