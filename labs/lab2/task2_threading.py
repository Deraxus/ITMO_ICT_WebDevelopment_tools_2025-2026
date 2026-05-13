import threading
from time import perf_counter

import requests
from bs4 import BeautifulSoup

from task2_common import URLS, save_trip, print_saved_rows


APPROACH = "threading"


def parse_and_save(url: str) -> None:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "Без заголовка"

    description = f"Страница была получена с URL: {url}. Подход: {APPROACH}."

    save_trip(title, description)
    print(f"Сохранено в trips: {title} | {url}")


def main() -> None:
    started_at = perf_counter()

    threads = []

    for url in URLS:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    elapsed = perf_counter() - started_at

    print(f"\nПодход: {APPROACH}")
    print(f"Количество URL: {len(URLS)}")
    print(f"Время выполнения: {elapsed:.6f} сек.")

    print_saved_rows()


if __name__ == "__main__":
    main()
