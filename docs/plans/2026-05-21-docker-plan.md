# Docker Containerization + GitHub Actions CI/CD Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Контейнеризиране на Excel2CSVConverter с автоматичен build/push към `ghcr.io` при `git push main` и `docker-compose` деплой на Linux сървър.

**Architecture:** Четири нови файла — `Dockerfile`, `.dockerignore`, `docker-compose.yml`, `.github/workflows/docker-publish.yml`. Кодът не се пипа. `supercronic` изпълнява `converter.py` всеки ден в 16:30. GitHub Actions ползва `GITHUB_TOKEN` за автентикация към `ghcr.io`.

**Tech Stack:** Python 3.14.4-slim (Debian 12), Microsoft ODBC Driver 18, supercronic, GitHub Actions, ghcr.io, docker-compose

---

### Task 1: .dockerignore

**Files:**
- Create: `.dockerignore`

**Step 1: Създай `.dockerignore`**

Точно това съдържание:

```
venv/
.env
.env-sampel
.git/
.idea/
__pycache__/
*.pyc
docs/
tests/
*.bat
.DS_Store
```

**Step 2: Провери синтаксиса**

```bash
cat .dockerignore
```

Очакван резултат: файлът съдържа изброените редове.

**Step 3: Commit**

```bash
git add .dockerignore
git commit -m "chore: add .dockerignore"
```

---

### Task 2: Dockerfile

**Files:**
- Create: `Dockerfile`

**Step 1: Създай `Dockerfile`**

Точно това съдържание:

```dockerfile
FROM python:3.14.4-slim

RUN apt-get update && apt-get install -y curl gnupg2 apt-transport-https \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
       | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
       > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/aptible/supercronic/releases/latest/download/supercronic-linux-amd64 \
    -o /usr/local/bin/supercronic && chmod +x /usr/local/bin/supercronic

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo "30 16 * * * cd /app && python converter.py" > /etc/crontab.txt

CMD ["supercronic", "/etc/crontab.txt"]
```

**Step 2: Build локално**

```bash
docker build -t excel2csv-test .
```

Очакван резултат: `Successfully built <image-id>` без грешки.

**Step 3: Провери Python версията в контейнера**

```bash
docker run --rm excel2csv-test python --version
```

Очакван резултат: `Python 3.14.4`

**Step 4: Провери supercronic**

```bash
docker run --rm excel2csv-test supercronic --version
```

Очакван резултат: версия на supercronic (напр. `0.2.33`)

**Step 5: Провери ODBC Driver**

```bash
docker run --rm excel2csv-test odbcinst -q -d -n "ODBC Driver 18 for SQL Server"
```

Очакван резултат: `[ODBC Driver 18 for SQL Server]` без грешка.

**Step 6: Изчисти тест image-а**

```bash
docker rmi excel2csv-test
```

**Step 7: Commit**

```bash
git add Dockerfile
git commit -m "feat: add Dockerfile with Python 3.14.4, ODBC Driver 18 and supercronic"
```

---

### Task 3: docker-compose.yml

**Files:**
- Create: `docker-compose.yml`

**Step 1: Създай `docker-compose.yml`**

Точно това съдържание:

```yaml
services:
  excel2csv:
    image: ghcr.io/gik986/excel2csvconverter:latest
    container_name: excel2csv
    restart: unless-stopped
    env_file: .env
    volumes:
      - /mnt/pricelist:/data/pricelist
      - /mnt/logs:/data/logs
```

**Step 2: Провери синтаксиса**

```bash
docker compose config
```

Очакван резултат: валиден YAML output без грешки.

> **Забележка:** `docker compose config` ще покаже warning за липсващ `.env` — това е нормално за локална машина. На Linux сървъра `.env` ще е наличен.

**Step 3: Commit**

```bash
git add docker-compose.yml
git commit -m "feat: add docker-compose.yml for Linux server deployment"
```

---

### Task 4: GitHub Actions Workflow

**Files:**
- Create: `.github/workflows/docker-publish.yml`

**Step 1: Създай директорията**

```bash
mkdir -p .github/workflows
```

**Step 2: Създай `.github/workflows/docker-publish.yml`**

Точно това съдържание:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Log in to ghcr.io
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository_owner }}/excel2csvconverter:latest
```

**Step 3: Провери YAML синтаксиса**

```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/docker-publish.yml')); print('OK')"
```

Очакван резултат: `OK`

**Step 4: Commit и push**

```bash
git add .github/workflows/docker-publish.yml
git commit -m "feat: add GitHub Actions workflow for Docker build and push to ghcr.io"
git push origin main
```

**Step 5: Провери GitHub Actions**

Отвори `https://github.com/GiK986/Excel2CSVConverter/actions` и провери:
- Workflow `Build and Push Docker Image` се е стартирал
- Всички стъпки са зелени
- Image е наличен в `ghcr.io/gik986/excel2csvconverter:latest`

**Step 6: Провери image в ghcr.io**

```bash
docker pull ghcr.io/gik986/excel2csvconverter:latest
```

Очакван резултат: image се изтегля успешно.

---

### Бележки за Linux сървъра (след деплой)

1. Монтирай Samba share:
```bash
# Инсталирай cifs-utils
sudo apt-get install -y cifs-utils

# Създай mount points
sudo mkdir -p /mnt/pricelist /mnt/logs

# Добави в /etc/fstab
//10.10.10.200/pricelist/ /mnt/pricelist cifs credentials=/etc/samba-creds,uid=1000,gid=1000,iocharset=utf8,_netdev 0 0
```

2. Създай `/etc/samba-creds`:
```
username=<samba-user>
password=<samba-password>
```

3. Създай `.env` файл до `docker-compose.yml`:
```
INPUT_FOLDER=/data/pricelist/input
OUTPUT_FOLDER=/data/pricelist/output
LOG_FOLDER=/data/logs
SERVER_NAME=<linux-sql-server>
DATABASE_NAME=<database-name>
DATABASE_USER=<user>
DATABASE_PASSWORD=<password>
```

4. Стартирай контейнера:
```bash
docker compose pull && docker compose up -d
```
