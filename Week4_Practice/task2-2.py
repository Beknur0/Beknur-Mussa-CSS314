import math
import time
import threading

N = 1_000_000


# -------------------------------------------------
# Serial baseline
# -------------------------------------------------
def calc_pi_serial(num_steps):
    step = 1.0 / num_steps
    total_sum = 0.0

    for i in range(num_steps):
        x = (i + 0.5) * step
        total_sum += 4.0 / (1.0 + x * x)

    return total_sum * step


# -------------------------------------------------
# Critical Section version
# Equivalent to #pragma omp critical
# -------------------------------------------------
def calc_pi_critical(num_steps, num_threads):
    step = 1.0 / num_steps

    shared_sum = [0.0]

    # Only one thread can enter the critical section at a time
    lock = threading.Lock()

    threads = []

    chunk_size = num_steps // num_threads

    def worker(start, end):
        for i in range(start, end):
            x = (i + 0.5) * step
            term = 4.0 / (1.0 + x * x)

            # Critical section
            with lock:
                shared_sum[0] += term

    for t in range(num_threads):
        start = t * chunk_size

        if t == num_threads - 1:
            end = num_steps
        else:
            end = start + chunk_size

        thread = threading.Thread(
            target=worker,
            args=(start, end)
        )

        threads.append(thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Barrier equivalent
    for thread in threads:
        thread.join()

    return shared_sum[0] * step


def main():

    # You can change this to 2, 4, or 8
    P = 4

    print("Task 2.2 - Critical Section Overhead")
    print(f"N = {N:,}")
    print(f"Threads = {P}")
    print()

    # ----------------------------
    # Serial benchmark
    # ----------------------------
    start = time.perf_counter()

    pi_serial = calc_pi_serial(N)

    end = time.perf_counter()

    serial_time = end - start
    serial_error = abs(pi_serial - math.pi)

    # ----------------------------
    # Critical section benchmark
    # ----------------------------
    start = time.perf_counter()

    pi_critical = calc_pi_critical(N, P)

    end = time.perf_counter()

    critical_time = end - start
    critical_error = abs(pi_critical - math.pi)

    # ----------------------------
    # Lock contention overhead
    # ----------------------------
    overhead = (
        (critical_time - serial_time)
        / serial_time
        * 100.0
    )

    slowdown = critical_time / serial_time

    # ----------------------------
    # Results
    # ----------------------------
    print("Serial baseline:")
    print(f"Pi             = {pi_serial:.12f}")
    print(f"Absolute Error = {serial_error:.12e}")
    print(f"Time           = {serial_time:.6f} s")

    print()

    print("Critical section:")
    print(f"Pi             = {pi_critical:.12f}")
    print(f"Absolute Error = {critical_error:.12e}")
    print(f"Time           = {critical_time:.6f} s")

    print()

    print("Performance:")
    print(f"Slowdown              = {slowdown:.2f}x")
    print(f"Lock Contention Overhead = {overhead:.2f}%")


if __name__ == "__main__":
    main()