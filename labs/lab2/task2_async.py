import asyncio
from time import perf_counter

import aiohttp
from bs4 import BeautifulSoup

from task2_common import URLS, save_trip, print_saved_rows


APPROACH = "asyncio"


async def save_trip_async(title: str, description: str) -> None:
    """
    Запись в PostgreSQL выполняется через обычный psycopg в отдельном потоке.

    HTTP-запросы остаются настоящими асинхронными через aiohttp.
    Такой вариант проще ставится на Python 3.13, потому что не требует asyncpg.
    """
    await asyncio.to_thread(save_trip, title, description)


async def parse_and_save(url: str, session: aiohttp.ClientSession) -> None:
    async with session.get(url, timeout=10) as response:
        response.raise_for_status()
        html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "Без заголовка"

    description = f"Страница была получена с URL: {url}. Подход: {APPROACH}."

    await save_trip_async(title, description)
    print(f"Сохранено в trips: {title} | {url}")


async def main() -> None:
    started_at = perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(parse_and_save(url, session))
            for url in URLS
        ]

        await asyncio.gather(*tasks)

    elapsed = perf_counter() - started_at

    print(f"\nПодход: {APPROACH}")
    print(f"Количество URL: {len(URLS)}")
    print(f"Время выполнения: {elapsed:.6f} сек.")

    print_saved_rows()


if __name__ == "__main__":
    asyncio.run(main())
