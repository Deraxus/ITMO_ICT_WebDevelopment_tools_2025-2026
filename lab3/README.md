# Лабораторная работа 3. Docker, источники данных и очереди

## Цель

Упаковать FastAPI-приложение в Docker, подключить PostgreSQL, вынести парсер в отдельный сервис и реализовать вызов парсера напрямую и через очередь Celery + Redis.

## Состав проекта

- `app` — основное FastAPI-приложение Travel Buddy из лабораторной работы №1.
- `parser_service` — отдельное FastAPI-приложение для парсинга страниц.
- `db` — PostgreSQL.
- `redis` — брокер сообщений и хранилище результатов Celery.
- `celery_worker` — обработчик фоновых задач парсинга.
- `celery_beat` — сервис для периодических задач.

## Запуск

```bash
docker compose up --build
```

После запуска:

- основное API: `http://localhost:8000/docs`
- parser service: `http://localhost:8001/docs`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

## Проверка

### 1. Проверить основное FastAPI-приложение

```bash
curl http://localhost:8000/
```

Ожидаемый ответ:

```json
{"message":"Travel Buddy API is running"}
```

### 2. Проверить отдельный parser service

```bash
curl -X POST http://localhost:8001/parse \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://example.com\"}"
```

### 3. Проверить вызов parser service из основного FastAPI

```bash
curl -X POST http://localhost:8000/parser/parse \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://example.com\"}"
```

### 4. Проверить постановку задачи в очередь Celery

```bash
curl -X POST http://localhost:8000/parser/parse-async \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://example.com\"}"
```

Ответ содержит `task_id`. Статус задачи можно проверить так:

```bash
curl http://localhost:8000/parser/tasks/<task_id>
```

## Остановка

```bash
docker compose down
```

Чтобы удалить данные PostgreSQL:

```bash
docker compose down -v
```
