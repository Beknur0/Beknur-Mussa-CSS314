from concurrent.futures import ThreadPoolExecutor
import math
import os
import time


def heavy_workload(thread_id: int, iterations: int = 10_000_000) -> float:
  """CPU-bound task designed to saturate a physical/logical hardware core."""
  total = 0.0
  for i in range(1, iterations + 1):
    total += math.sqrt(i)
  return total


def run_saturation_test(num_threads: int) -> None:
  print(f"\n=== Running Saturation Test with P = {num_threads} Threads ===")
  print(
      "Open your OS System Monitor (Task Manager / htop) to observe CPU"
      " utilization..."
  )

  start_time = time.perf_counter()

  with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [
        executor.submit(heavy_workload, tid) for tid in range(num_threads)
    ]
    for f in futures:
      f.result()  # Implicit barrier: wait for all worker threads to join

  elapsed = time.perf_counter() - start_time
  print(f"Execution completed in: {elapsed:.4f} seconds")


if __name__ == "__main__":
  logical_cores = os.cpu_count() or 4
  print(f"Detected Logical CPU Cores: {logical_cores}")

  run_saturation_test(logical_cores)