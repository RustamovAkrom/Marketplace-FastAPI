# 🛠 Project Tools & Infrastructure

This table summarizes the **tools and technologies** used in the E-Commerce project, categorized by purpose.

| Category         | Technology / Tools                        |
| ---------------- | ----------------------------------------- |
| CI/CD            | GitHub Actions, Docker Hub, SSH Deploy    |
| Monitoring       | Prometheus, Grafana, Sentry               |
| Logging          | structlog, loguru                         |
| Cache            | Redis                                     |
| Architecture     | Service + Repository pattern              |
| Testing          | pytest, asyncio, factory-boy              |
| Security         | JWT, Refresh Tokens, Roles, Rate Limiting |
| Containerization | Dockerfile, Docker Compose                |
| Workflow         | pre-commit hooks                          |
| Notifications    | Telegram, Slack, Email                    |
| AI / Embeddings  | Qdrant, Embeddings                        |

---

## Notes / Recommendations

* **CI/CD:** GitHub Actions runs tests, security checks, and deploys automatically.
* **Monitoring:** Prometheus + Grafana collect metrics; Sentry tracks errors and exceptions.
* **Logging:** `structlog` or `loguru` provide structured and centralized logs.
* **Cache:** Redis used for caching API responses and async tasks.
* **Architecture:** Follows **Service + Repository pattern** for modularity and testability.
* **Testing:** `pytest` + `asyncio` for async tests; `factory-boy` for fixtures.
* **Security:** JWT authentication, refresh tokens, role-based access control, rate limiting for APIs.
* **Notifications:** Alerts sent via Telegram, Slack, and email.
* **AI / Embeddings:** Qdrant database for vector search / embeddings.
