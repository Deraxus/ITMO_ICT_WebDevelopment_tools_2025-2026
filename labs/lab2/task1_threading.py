from time import perf_counter

N = 10_000_000_000_000
WORKERS = 8


def split_ranges(n: int, workers: int) -> list[tuple[int, int]]:
    chunk = n // workers
    ranges = []

    start = 1
    for i in range(workers):
        end = start + chunk - 1

        if i == workers - 1:
            end = n

        ranges.append((start, end))
        start = end + 1

    return ranges


def calculate_sum(start: int, end: int) -> int:
    """
    Считает сумму чисел от start до end включительно.

    Используется формула арифметической прогрессии, потому что прямой цикл
    до 10_000_000_000_000 будет выполняться нереалистично долго.
    """
    count = end - start + 1
    return (start + end) * count // 2


def expected_sum(n: int) -> int:
    return n * (n + 1) // 2

import threading


def worker(start: int, end: int, results: list[int], index: int) -> None:
    results[index] = calculate_sum(start, end)


def main() -> None:
    started_at = perf_counter()

    ranges = split_ranges(N, WORKERS)
    results = [0] * WORKERS
    threads = []

    for index, (start, end) in enumerate(ranges):
        thread = threading.Thread(
            target=worker,
            args=(start, end, results, index),
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total = sum(results)
    elapsed = perf_counter() - started_at

    print("Подход: threading")
    print(f"Количество задач: {WORKERS}")
    print(f"Сумма: {total}")
    print(f"Проверка: {total == expected_sum(N)}")
    print(f"Время выполнения: {elapsed:.6f} сек.")


if __name__ == "__main__":
    main()
