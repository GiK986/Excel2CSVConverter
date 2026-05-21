# Design: Docker Containerization + GitHub Actions CI/CD

**Date:** 2026-05-21
**Scope:** Фаза 2 — Docker контейнеризация, CI/CD pipeline към ghcr.io, cron job в контейнера

## Цел

Контейнеризиране на Excel2CSVConverter с автоматичен build и push към `ghcr.io` при `git push` на `main`. Контейнерът върви непрекъснато на Linux сървър и изпълнява конвертора всеки ден в 16:30 чрез `supercronic`.

## Архитектура

```
git push main
      │
      ▼
GitHub Actions
  → build Docker image
  → push ghcr.io/gik986/excel2csvconverter:latest
      │
      ▼ (ръчно на сървъра)
docker-compose pull
docker-compose up -d
      │
      ▼
Контейнер върви непрекъснато
supercronic → 16:30 всеки ден → python converter.py
      │                                │
      ▼                                ▼
/data/pricelist                MS SQL Server (Linux)
(Samba share, монтиран на хоста)
```

## Компоненти

### 1. Dockerfile

- Base image: `python:3.14.4-slim` (Debian 12)
- Microsoft ODBC Driver 18 за SQL Server (Linux/Debian)
- `supercronic` binary (AMD64) за cron scheduling
- Инсталация на Python зависимости от `requirements.txt`
- Cron schedule: `30 16 * * *` → `python converter.py`
- Entrypoint: `supercronic /etc/crontab.txt`

### 2. GitHub Actions Workflow

- Файл: `.github/workflows/docker-publish.yml`
- Trigger: push към `main` branch
- Registry: `ghcr.io`
- Authentication: `GITHUB_TOKEN` (автоматичен, без ръчни secrets)
- Tag: `ghcr.io/gik986/excel2csvconverter:latest`

### 3. docker-compose.yml (Linux сървър)

- Image: `ghcr.io/gik986/excel2csvconverter:latest`
- `restart: unless-stopped` — автоматичен restart при reboot
- `env_file: .env` — credentials от `.env` файл на сървъра
- Volume mounts:
  - `/mnt/pricelist` → `/data/pricelist` (Samba share)
  - `/mnt/logs` → `/data/logs`
- `docker-compose.yml` се commit-ва в git
- `.env` файлът НЕ се commit-ва (вече в `.gitignore`)

### 4. .dockerignore

Изключва от image-а: `venv/`, `.env`, `.git/`, `.idea/`, `__pycache__/`, `docs/`, `tests/`, `*.bat`

## Файлове за създаване

| Файл | Действие |
|---|---|
| `Dockerfile` | нов |
| `.github/workflows/docker-publish.yml` | нов |
| `docker-compose.yml` | нов, commit-ва се |
| `.dockerignore` | нов |

## Update workflow на сървъра

```bash
docker-compose pull && docker-compose up -d
```

## Следващи фази

- **Фаза 3:** DB промени — нов сървър, нова таблица в `validators.py`
