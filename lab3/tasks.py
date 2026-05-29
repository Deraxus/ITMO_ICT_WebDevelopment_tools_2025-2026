import requests
import psycopg
from bs4 import BeautifulSoup

from app.celery_app import celery_app
from app.core.config import settings


def get_psycopg_database_url() -> str:
    return settings.database_url.replace("postgresql+psycopg://", "postgresql://")


def parse_title(url: str) -> str:
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "Без заголовка"


def save_trip(title: str, description: str) -> int:
    with psycopg.connect(get_psycopg_database_url()) as connection:
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


@celery_app.task(name="app.tasks.parse_url_task")
def parse_url_task(url: str) -> dict:
    title = parse_title(url)
    description = f"Страница была получена с URL: {url}. Подход: Celery + Redis."
    trip_id = save_trip(title, description)

    return {
        "trip_id": trip_id,
        "title": title,
        "url": url,
        "message": "Parsing completed by Celery worker"
    }
