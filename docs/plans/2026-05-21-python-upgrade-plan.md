# Python 3.11 → 3.14.4 Upgrade Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Надграждане на Python от 3.11.4 до 3.14.4 чрез обновяване на `requirements.txt` и пресъздаване на виртуалната среда.

**Architecture:** Само зависимостите се актуализират — кодът остава непроменен. Старото `venv` се изтрива и се създава ново с Python 3.14.4. Pinned версии на инфраструктурни пакети (`pip`, `setuptools`, `six`, `et-xmlfile`) се премахват от `requirements.txt`.

**Tech Stack:** Python 3.14.4, pandas>=2.2, numpy>=2.0, openpyxl>=3.1, pyodbc, python-dotenv

---

### Task 1: Инсталиране на Python 3.14.4

**Files:**
- Нищо не се променя в проекта

**Step 1: Провери дали Python 3.14 вече е наличен**

```bash
python3.14 --version
```

Очакван резултат: `Python 3.14.x` — ако е налично, прескочи към Task 2.

**Step 2: Инсталирай Python 3.14.4 чрез Homebrew (ако не е наличен)**

```bash
brew install python@3.14
```

**Step 3: Потвърди инсталацията**

```bash
python3.14 --version
```

Очакван резултат: `Python 3.14.4`

---

### Task 2: Актуализиране на `requirements.txt`

**Files:**
- Modify: `requirements.txt`

**Step 1: Замени съдържанието на `requirements.txt`**

Новото съдържание:

```
numpy>=2.0
openpyxl>=3.1
pandas>=2.2
python-dateutil>=2.9
pytz>=2024
tzdata>=2024
xlrd>=2.0
python-dotenv
pyodbc
```

Премахнати: `et-xmlfile` (transitive dep), `pip`, `setuptools`, `six` (не са app зависимости).

**Step 2: Commit**

```bash
git add requirements.txt
git commit -m "chore: update requirements.txt for Python 3.14.4 compatibility"
```

---

### Task 3: Пресъздаване на виртуалната среда

**Files:**
- `venv/` — изтрива се и се създава наново

**Step 1: Изтрий старото venv**

```bash
rm -rf venv
```

**Step 2: Създай ново venv с Python 3.14.4**

```bash
python3.14 -m venv venv
```

**Step 3: Активирай venv**

```bash
source venv/bin/activate
```

Потвърди: `which python` трябва да сочи към `venv/bin/python`.

**Step 4: Инсталирай зависимостите**

```bash
pip install -r requirements.txt
```

Очакван резултат: всички пакети се инсталират без грешки.

**Step 5: Провери инсталираните версии**

```bash
pip list | grep -E "numpy|pandas|openpyxl|pyodbc"
```

Очакван резултат: numpy 2.x, pandas 2.2+, openpyxl 3.1+, pyodbc 5.x

---

### Task 4: Стартиране на съществуващите тестове

**Files:**
- Test: `tests/unit_test.py`

**Step 1: Инсталирай pytest (ако не е в requirements)**

```bash
pip install pytest
```

**Step 2: Стартирай тестовете**

```bash
python -m pytest tests/ -v
```

Очакван резултат:
```
tests/unit_test.py::TestGetInputRootFolder::test_returns_input_folder PASSED
```

**Step 3: При грешка**

Ако тестът фейлва с `ModuleNotFoundError` — провери дали `.env` файлът е наличен с валидни стойности:
```bash
cat .env
```
`INPUT_FOLDER` трябва да е `./test_input` или реален път.

---

### Task 5: Ръчно тестване с реален Excel файл (по избор)

**Step 1: Провери .env за реалните пътища**

```bash
cat .env
```

**Step 2: Стартирай конвертора**

```bash
python converter.py
```

Очакван резултат: лог файл се създава в `LOG_FOLDER`, CSV файловете се генерират в `OUTPUT_FOLDER`.

**Step 3: Commit на финалното състояние**

```bash
git add .
git commit -m "chore: recreate venv with Python 3.14.4"
```

> **Забележка:** `venv/` е в `.gitignore` — само `requirements.txt` реално се commit-ва.
