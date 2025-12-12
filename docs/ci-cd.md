# 📄 CI/CD & Security Documentation

## 1️⃣ Overview

This document summarizes all tools, workflows, and commands for **CI/CD, security, and code quality**.

**Key components:**

1. **Dependabot** — automatic dependency updates + security alerts
2. **CodeQL (GitHub Code Scanning)** — SAST for vulnerabilities
3. **pip-audit + Bandit + Safety** — Python security scanners in CI
4. **Secret scanning / Detect-secrets** — prevent leaking secrets into repo
5. **Pre-commit hooks with security checks** — early local protection
6. **Branch protection + required checks + CODEOWNERS** — enforce PR rules
7. **Security policy & issue templates** — vulnerability reporting
8. **Least-privilege secrets & key rotation** — safe secret management
9. **Optional:** Trivy/Clair/Snyk — future container/image scanning

---

## 2️⃣ Dependabot

**File:** `.github/dependabot.yml`
**Purpose:** automatically creates PRs for outdated/vulnerable dependencies.

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/" 
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
    rebase-strategy: "auto"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
```

---

## 3️⃣ CodeQL (SAST)

**File:** `.github/workflows/codeql-analysis.yml`
**Purpose:** static security analysis.

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
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v2
        with:
          languages: python
      - uses: github/codeql-action/autobuild@v2
      - uses: github/codeql-action/analyze@v2
```

---

## 4️⃣ Security Scanners in CI

Add to `ci.yml` or a dedicated job:

```yaml
- name: Install security tools
  run: |
    python -m pip install --upgrade pip
    pip install pip-audit bandit safety

- name: Dependency security audit (pip-audit)
  run: pip-audit --format=human

- name: Static security scan (Bandit)
  run: bandit -r src -ll

- name: Safety check (optional)
  run: safety check
```

---

## 5️⃣ Pre-commit Hooks

**File:** `.pre-commit-config.yaml`

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

**Commands:**

```bash
pre-commit install
pre-commit run --all-files
detect-secrets scan > .secrets.baseline
```

---

## 6️⃣ GitHub Secrets & Environment

* Store sensitive keys (`STRIPE_SECRET_KEY`, `TELEGRAM_BOT_TOKEN`, `DATABASE_URL_PROD`) in **GitHub Secrets**.
* Do **not** store real values in code; use `.env` placeholders.
* Enable **GitHub Secret Scanning** for automatic alerts.

---

## 7️⃣ Branch Protection & PR Rules

* Require pull request reviews (1-2 approvals)
* Require status checks (CI, CodeQL, tests)
* Optional: linear history, signed commits
* Restrict push access to specific teams

---

## 8️⃣ CODEOWNERS

**File:** `.github/CODEOWNERS`

```
/src/services/* @org/backend-team
/src/db/* @org/db-team
/src/api/* @org/backend-team
```

---

## 9️⃣ Security Policy & Issue Template

**`.github/SECURITY.md`**

```markdown
# Security Policy
Report vulnerabilities to security@example.com. Response within 72 hours.
Preferred disclosure: private report.
```

**`.github/ISSUE_TEMPLATE/security.md`** — template for reporting issues.

---

## 🔧 Quick Local Commands

```bash
# Update pip and uv
python -m pip install --upgrade pip
pip install --upgrade uv

# Sync dependencies
uv sync

# Update pre-commit hooks
uv run pre-commit autoupdate

# Clear pre-commit cache
uv run pre-commit clean

# Run all pre-commit checks
uv run pre-commit run --all-files

# Type checking
uv run mypy src/

# Linting
uv run ruff check src/

# Code formatting (optional)
uv run black --check src/

# Secret scan
uv run detect-secrets scan

# Run tests
uv run pytest -v tests
```
