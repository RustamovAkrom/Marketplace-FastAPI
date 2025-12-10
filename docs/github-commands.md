Отлично — круто, что не спешим с Docker/деплоем и хотим сначала укрепить проект и рабочий процесс. Я подготовил практический набор технологий, автоматизаций и конфигураций, которые можно добавить прямо сейчас — они поднимут безопасность, качество кода и скорость CI без Docker.

Я даю:

* краткое объяснение *почему* каждая вещь полезна;
* точные файлы / сниппеты + куда их положить;
* небольшие рекомендации по настройке GitHub (UI) и по правам.

Внедрять можно по частям — возьми то, что нужно сейчас, и скажи, если вставить в репозиторий код прямо.

---

# Короткий план (что и зачем)

1. **Dependabot** — автоматические обновления зависимостей + security alerts.
2. **CodeQL (GitHub Code Scanning)** — SAST (статический анализ уязвимостей).
3. **pip-audit + Bandit + safety** в CI — Python-ориентированные сканеры зависимостей и кода.
4. **Secret scanning / Detect secrets** — предотвратить попадание ключей в репозиторий.
5. **Pre-commit: add security hooks** — локальная ранняя защита.
6. **Branch protection + required checks + CODEOWNERS** — регламентация PR / review.
7. **Security policy & issue templates** — как сообщать уязвимости и кто отвечает.
8. **Least-privilege for secrets & rotating keys** — безопасное хранение секретов.
9. **Optional**: Trivy/Clair/Snyk integration later for container/image scanning (на будущее).

---

# 1) Dependabot — `.github/dependabot.yml`

**Куда:** `.github/dependabot.yml`
**Зачем:** автоматически создает PR при устаревших/уязвимых зависимостях.

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/" 
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
    rebase-strategy: "auto"
    # optional: ignore dev deps or certain packages
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
```

---

# 2) CodeQL — SAST workflow

**Куда:** `.github/workflows/codeql-analysis.yml`
**Зачем:** GitHub Code Scanning (CodeQL) ищет уязвимости в коде и зависимостях.

```yaml
name: "CodeQL"

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: "0 3 * * 0"

jobs:
  analyze:
    name: Analyze (CodeQL)
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: python

      - name: Autobuild (if needed)
        uses: github/codeql-action/autobuild@v2

      - name: Run CodeQL analysis
        uses: github/codeql-action/analyze@v2
```

> CodeQL бесплатен для публичных репозиториев; для приватных — часть GitHub Advanced Security (проверь тариф).

---

# 3) Добавим security сканеры в CI (улучшим `ci.yml`)

Добавим этапы для `pip-audit` (скан зависимостей), `bandit` (статический анализ Python) и `pip install safety` (опционально). Ниже — улучшённый фрагмент (вставь в свой `ci.yml` под `Run Pre-commit checks` или как отдельный job `security`).

```yaml
      - name: Install security tools
        run: |
          python -m pip install --upgrade pip
          pip install pip-audit bandit safety

      - name: Dependency security audit (pip-audit)
        run: |
          pip-audit --format=human

      - name: Static security scan (Bandit)
        run: |
          bandit -r src -ll

      - name: Safety check (optional)
        run: |
          safety check
```

Если хочешь — добавлю флаг `--fail-on` или parse results and fail CI only for critical CVEs.

---

# 4) Pre-commit — security hooks

В `.pre-commit-config.yaml` предложу добавить `detect-secrets` и `pre-commit-hooks` для простых проверок.

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: check-added-large-files
      - id: check-ast
      - id: end-of-file-fixer

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: [--baseline, .secrets.baseline]

  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.7
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.19.0
    hooks:
      - id: mypy
```

**Действия:**

* Запустить локально: `pre-commit install && pre-commit run --all-files`
* `detect-secrets` создаст baseline: `detect-secrets scan > .secrets.baseline` (потом закоммить baseline).

---

# 5) Secret scanning / GitHub secrets

* Перенеси ключи (`STRIPE_SECRET_KEY` и т.д.) в **GitHub Secrets** (`Settings → Secrets and variables → Actions`).
* Используй имена `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `DATABASE_URL_PROD` и т.д.
* **Не хранить** значения в коде (в `core.config.py` оставь заглушки; реальные — из env).

**Дополнительно:** включи GitHub Secret Scanning (в репозитории/organization) — будет сообщать о возможных утечках.

---

# 6) Branch protection & PR rules (через UI)

Включи для `main` (Settings → Branches → Branch protection rules):

* Require pull request reviews before merging (min 1-2 approving reviews).
* Require status checks to pass before merging — включи `CI Pipeline`, `CodeQL` и любые тесты.
* Require linear history (optional).
* Require signed commits (optional).
* Include administrators (если нужно).
* Restrict who can push to matching branches (use teams).

Также:

* Включи **Enforce administrators** (если хочешь, что даже админы проходили правила).

---

# 7) CODEOWNERS — обязательные ревьюеры

**Куда:** `.github/CODEOWNERS`
Пример:

```
# owners for core
/src/services/* @your-org/backend-team
/src/db/* @your-org/db-team
/src/api/* @your-org/backend-team
```

Это назначит ревьюеров автоматически на PR и улучшит code ownership.

---

# 8) SECURITY.md и ISSUE_TEMPLATE — как сообщать уязвимости

**`.github/SECURITY.md`** (корень репозитория):

```markdown
# Security Policy

If you found a security vulnerability, please reach out to security@example.com (or open a private issue).
We will respond within 72 hours.

Preferred disclosure: private report to the above address.
```

**`.github/ISSUE_TEMPLATE/security.md`** — шаблон для репорта.

---

# 9) GitHub Actions secrets & least privilege

* Не хранить long-lived personal access tokens (PAT) в secrets; если нужно — создать **machine user** с минимальными правами.
* Для Telegram / Stripe — использовать **restricted** API keys.
* Ротация: планируй ротацию ключей (каждые 90 дней) и хранение в vault (Vault, AWS Secrets Manager, GitHub Secrets).

---

# 10) Optional but recommended: pip-audit gating + auto-fix PRs

* Можно настроить Dependabot + `pip-audit` in PR check and auto-merge minor security updates.
* Для critical vulnerability — set CI to fail and block merge.

---

# 11) Short checklist / runbook to apply now

1. Создай/вставь:

   * `.github/dependabot.yml`
   * `.github/workflows/codeql-analysis.yml`
   * `.github/CODEOWNERS`
   * `.github/SECURITY.md`
   * добавить pre-commit hooks (detect-secrets)
2. Обнови `ci.yml` — вставь security steps (pip-audit, bandit).
3. Настрой GitHub Secrets (STRIPE_*, TELEGRAM_*, DB URL).
4. Включи Branch Protection для `main`.
5. Запусти `pre-commit install` локально; создай `.secrets.baseline` (если detect-secrets).
6. Проверить уведомления Dependabot и откликнуться на PRs.
7. (Опционально) Включить Code Scanning (CodeQL) и просмотреть alerts.

---

# Полезные команды / быстрое тестирование локально

* Установить сканеры:

```bash
python -m pip install pip-audit bandit safety detect-secrets
```

* Локальный тест:

```bash
pip-audit
bandit -r src
detect-secrets scan > .secrets.baseline
pre-commit run --all-files
```

---

Если хочешь, я могу прямо сейчас:

1. Создать и прислать полные файлы (`dependabot.yml`, `codeql-analysis.yml`, `CODEOWNERS`, `SECURITY.md`, обновлённый `.pre-commit-config.yaml`, и патч для `ci.yml` с секцией security).
2. Или — открыть PR с этими изменениями (если у меня доступ к репозиторию — скажи как дать доступ; иначе пришлю патчи/файлы).

Скажи: **(A)** Прислать все файлы прямо сюда, **(B)** Сгенерировать патч/PR инструкции, или **(C)** вставить изменения прямо в `ci.yml` и `.pre-commit-config.yaml` (и прислать diff).

---

```sh
# 1️⃣ Обновление pip и uv
python -m pip install --upgrade pip
pip install --upgrade uv

# 2️⃣ Синхронизация зависимостей проекта
uv sync

# 3️⃣ Обновление pre-commit хуков (чтобы detect-secrets и другие хуки были актуальны)
uv run pre-commit autoupdate

# 4️⃣ Очистка старого кэша pre-commit (чтобы не было конфликтов)
uv run pre-commit clean

# 5️⃣ Запуск pre-commit проверки всех файлов
uv run pre-commit run --all-files

# 6️⃣ Проверка типов mypy
uv run mypy src/

# 7️⃣ Проверка кода линтером ruff
uv run ruff check src/

# 8️⃣ Проверка форматирования black (опционально, если хочешь принудительно исправить)
uv run black --check src/

# 9️⃣ Проверка на секреты (detect-secrets)
uv run detect-secrets scan

# 🔟 Запуск тестов
uv run pytest -v tests

# ✅ Итоговая команда для Windows PowerShell
# Все шаги можно объединить через &&

```
