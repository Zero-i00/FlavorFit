# FlavorFit Backend

## Локальный запуск

### 1. Установите uv

Если uv ещё не установлен:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Подробнее: https://docs.astral.sh/uv/getting-started/installation/

### 2. Создайте файл окружения

```bash
cp .env.example .env
```

### 3. Активируйте виртуальное окружение и  установите зависимости

```bash
uv venv
```

```bash
uv install
```

### 4. Запустите приложение

```bash
uv run src/main.py
```

Приложение будет доступно по адресу http://localhost:8080
