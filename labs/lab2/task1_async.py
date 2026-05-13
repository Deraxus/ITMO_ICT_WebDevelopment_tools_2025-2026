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

import asyncio


async def calculate_sum_async(start: int, end: int) -> int:
    await asyncio.sleep(0)
    return calculate_sum(start, end)


async def main() -> None:
    started_at = perf_counter()

    ranges = split_ranges(N, WORKERS)
    tasks = [
        asyncio.create_task(calculate_sum_async(start, end))
        for start, end in ranges
    ]

    results = await asyncio.gather(*tasks)
    total = sum(results)
    elapsed = perf_counter() - started_at

    print("Подход: asyncio")
    print(f"Количество async-задач: {WORKERS}")
    print(f"Сумма: {total}")
    print(f"Проверка: {total == expected_sum(N)}")
    print(f"Время выполнения: {elapsed:.6f} сек.")


if __name__ == "__main__":
    asyncio.run(main())
