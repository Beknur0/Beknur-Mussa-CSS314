from concurrent.futures import ThreadPoolExecutor
import os
import threading
import time


def worker_task(thread_id: int, team_size: int):
  native_tid = threading.get_native_id()
  time.sleep(0.0001)


def run_team_benchmark(num_threads: int) -> float:
  start_time = time.perf_counter()

  with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [
      executor.submit(worker_task, tid, num_threads)
      for tid in range(num_threads)
    ]
    for f in futures:
      f.result() 

  end_time = time.perf_counter()
  return end_time - start_time


if __name__ == '__main__':
  thread_counts = [1, 2, 4, 8, 16, 32, 64]
  num_trials = 5

  print(f"{'P (Threads)':<12} | {'Avg Time (s)':<15} | {'Status'}")
  print("-" * 45)

  for P in thread_counts:
    total_time = 0.0
    for _ in range(num_trials):
      total_time += run_team_benchmark(P)

    avg_time = total_time / num_trials
    print(f"{P:<12} | {avg_time:<15.6f} | Completed")