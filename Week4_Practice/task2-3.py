import time
import math
from numba import njit, prange, set_num_threads, get_num_threads

N = 100_000_000
TRIALS = 5


@njit(parallel=True)
def calc_pi_reduction(num_steps):
    step = 1.0 / num_steps
    total_sum = 0.0

    for i in prange(num_steps):
        x = (i + 0.5) * step
        total_sum += 4.0 / (1.0 + x * x)

    return total_sum * step


def main():
    thread_counts = [1, 2, 4, 8, 16]

    print("Task 2.3 - Strong Scaling Benchmark")
    print(f"N = {N:,}")
    print(f"Trials per configuration = {TRIALS}")
    print()

    set_num_threads(1)
    calc_pi_reduction(10_000)

    print(
        f"{'Threads':<10}"
        f"{'T1 (s)':<12}"
        f"{'T2 (s)':<12}"
        f"{'T3 (s)':<12}"
        f"{'T4 (s)':<12}"
        f"{'T5 (s)':<12}"
        f"{'Average (s)':<14}"
        f"{'Error':<14}"
    )

    results = {}

    for p in thread_counts:
        try:
            set_num_threads(p)
        except ValueError:
            print(f"{p:<10}Not supported by current Numba configuration")
            continue

        times = []
        calculated_pi = 0.0

        for trial in range(TRIALS):
            start = time.perf_counter()

            calculated_pi = calc_pi_reduction(N)

            end = time.perf_counter()

            times.append(end - start)

        average_time = sum(times) / TRIALS
        error = abs(calculated_pi - math.pi)

        results[p] = average_time

        print(
            f"{p:<10}"
            f"{times[0]:<12.4f}"
            f"{times[1]:<12.4f}"
            f"{times[2]:<12.4f}"
            f"{times[3]:<12.4f}"
            f"{times[4]:<12.4f}"
            f"{average_time:<14.4f}"
            f"{error:<14.2e}"
        )


if __name__ == "__main__":
    main()
