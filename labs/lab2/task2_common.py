import os

import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://docs.python.org/3/",
    "https://www.djangoproject.com/",
    "https://fastapi.tiangolo.com/",
    "https://httpbin.org/html",
]


def check_database_url() -> None:
    if not DATABASE_URL:
        raise RuntimeError(
            "Не найдена переменная DATABASE_URL. "
            "Создай файл .env в корне проекта и добавь туда строку подключения к PostgreSQL."
        )


def get_connection():
    check_database_url()
    return psycopg.connect(DATABASE_URL)


def save_trip(title: str, description: str) -> None:
    """
    Сохраняет результат парсинга в таблицу trips из лабораторной работы 1.

    Структура таблицы:
    id SERIAL PRIMARY KEY
    title VARCHAR NOT NULL
    description VARCHAR
    owner_id INTEGER NULL
    """
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO trips (title, description, owner_id)
                VALUES (%s, %s, NULL)
                """,
                (title, description),
            )


def print_saved_rows() -> None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, description, owner_id
                FROM trips
                ORDER BY id DESC
                LIMIT 10
                """
            )

            rows = cursor.fetchall()

    print("\nПоследние записи в таблице trips:")
    for row_id, title, description, owner_id in rows:
        print(f"{row_id}. {title} | owner_id={owner_id} | {description}")


def split_list(items: list[str], parts: int) -> list[list[str]]:
    chunk_size = max(1, len(items) // parts)
    chunks = []

    for i in range(0, len(items), chunk_size):
        chunks.append(items[i:i + chunk_size])

    return chunks
