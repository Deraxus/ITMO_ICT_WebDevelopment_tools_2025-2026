import os

import psycopg
import requests
from bs4 import BeautifulSoup


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")

    return database_url.replace("postgresql+psycopg://", "postgresql://")


def parse_title(url: str) -> str:
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    if soup.title and soup.title.string:
        return soup.title.string.strip()

    return "Без заголовка"


def save_to_trips(title: str, url: str) -> int:
    description = f"Страница была получена с URL: {url}. Подход: отдельный parser_service по HTTP."

    with psycopg.connect(get_database_url()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO trips (title, description, owner_id)
                VALUES (%s, %s, NULL)
                RETURNING id
                """,
                (title, description),
            )
            trip_id = cursor.fetchone()[0]

    return trip_id


def parse_and_save(url: str) -> dict:
    title = parse_title(url)
    trip_id = save_to_trips(title, url)

    return {
        "trip_id": trip_id,
        "title": title,
        "url": url,
        "message": "Parsing completed by parser_service"
    }
