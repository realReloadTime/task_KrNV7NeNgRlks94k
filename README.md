# task_KrNV7NeNgRlks94k

Асинхронный backend-сервис на `FastAPI` с миграциями `Alembic` и базой данных `PostgreSQL`.

## Что нужно для запуска

- `Python 3.11+` (для локального запуска)
- `Docker` и `Docker Compose` (для запуска в контейнерах)

## Переменные окружения

Создайте файл `.env` в корне проекта:

```env
SECRET_KEY=change_me_secret
REFRESH_SECRET_KEY=change_me_refresh_secret
ALGORITHM=HS256

DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=task_db
IS_DEBUG=False
```

`docker-compose.yml` также берет параметры БД из этого же `.env`.
### ВНИМАНИЕ!
`DB_HOST=db` определение хоста для **Docker**! Для локального запуска используйте хост `localhost` или Ваш удаленный хост.

## Запуск вручную (без Docker)

1. Создайте и активируйте виртуальное окружение:

```bash
python -m venv .venv
```

### Windows (PowerShell)
```bash
.venv\Scripts\Activate.ps1
```

### Linux/macOS
```bash
source .venv/bin/activate
```

2. Установите зависимости:

```bash
pip install -r backend/requirements.txt
```

3. Примените миграции:

```bash
alembic upgrade head
```

4. Запустите API:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Если запускаете API локально, а БД не в Docker, укажите `DB_HOST=localhost` в `.env`.

## Запуск через Docker Compose

1. Запустите сервисы:

```bash
docker compose up --build
```

2. Остановите сервисы:

```bash
docker compose down
```

## Данные для авторизации созданных по-умолчанию пользователей в миграции
### Обычный пользователь:
- email: `test_user@example.com`
- пароль: `string`

### Администратор
- email: `test_admin@example.com`
- пароль: `string`

## Полезные ссылки

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health-check: [http://localhost:8000/health](http://localhost:8000/health)
- POST эндпоинт для веб-хука: [http://localhost:8000/transaction-histories/webhook](http://localhost:8000/transaction-histories/webhook)