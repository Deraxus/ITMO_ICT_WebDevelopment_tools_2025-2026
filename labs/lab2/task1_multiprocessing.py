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

from multiprocessing import Pool, cpu_count


def main() -> None:
    started_at = perf_counter()

    workers = min(WORKERS, cpu_count())
    ranges = split_ranges(N, workers)

    with Pool(processes=workers) as pool:
        results = pool.starmap(calculate_sum, ranges)

    total = sum(results)
    elapsed = perf_counter() - started_at

    print("Подход: multiprocessing")
    print(f"Количество процессов: {workers}")
    print(f"Сумма: {total}")
    print(f"Проверка: {total == expected_sum(N)}")
    print(f"Время выполнения: {elapsed:.6f} сек.")


if __name__ == "__main__":
    main()
