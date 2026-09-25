import numpy as np
from numba import njit, prange, set_num_threads
import time

N = 100_000_000

@njit(parallel=True)
def calc_pi_race(num_steps):
    step = 1.0 / num_steps

    shared_sum = np.zeros(1, dtype=np.float64)

    for i in prange(num_steps):
        x = (i + 0.5) * step

        shared_sum[0] += 4.0 / (1.0 + x * x)

    return shared_sum[0] * step


def main():

    thread_counts = [1, 2, 4, 8]

    set_num_threads(1)
    calc_pi_race(1000)

    print("Task 2.1 - Race Condition Quantification")
    print(f"N = {N:,}")
    print()

    print(
        f"{'Threads':<10}"
        f"{'Calculated Pi':<20}"
        f"{'Absolute Error':<20}"
        f"{'Time (s)':<12}"
    )

    for p in thread_counts:
        set_num_threads(p)

        start = time.perf_counter()

        calculated_pi = calc_pi_race(N)

        end = time.perf_counter()

        error = abs(calculated_pi - np.pi)
        elapsed = end - start

        print(
            f"{p:<10}"
            f"{calculated_pi:<20.12f}"
            f"{error:<20.12e}"
            f"{elapsed:<12.4f}"
        )


if __name__ == "__main__":
    main()