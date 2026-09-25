import matplotlib.pyplot as plt

# Average times from Task 2.3
times = {
    1: 0.1554,
    2: 0.0774,
    4: 0.0498,
    8: 0.0369
}

t1 = times[1]

threads = []
speedups = []
efficiencies = []

print("Task 2.4 - Speedup & Efficiency Modeling")
print()

print(
    f"{'Threads':<10}"
    f"{'Time (s)':<12}"
    f"{'Speedup':<12}"
    f"{'Efficiency':<14}"
    f"{'Efficiency %':<14}"
)

for p, time_p in times.items():

    # S(P) = T(1) / T(P)
    speedup = t1 / time_p

    # E(P) = S(P) / P
    efficiency = speedup / p

    threads.append(p)
    speedups.append(speedup)
    efficiencies.append(efficiency)

    print(
        f"{p:<10}"
        f"{time_p:<12.4f}"
        f"{speedup:<12.3f}"
        f"{efficiency:<14.3f}"
        f"{efficiency * 100:<14.2f}%"
    )


# -------------------------------------------------
# Graph: Measured vs Ideal Speedup
# -------------------------------------------------

ideal_speedup = threads

plt.figure(figsize=(8, 5))

plt.plot(
    threads,
    speedups,
    marker="o",
    linewidth=2,
    label="Measured Speedup"
)

plt.plot(
    threads,
    ideal_speedup,
    marker="s",
    linestyle="--",
    linewidth=2,
    label="Linear Ideal Speedup"
)

plt.xlabel("Number of Threads P")
plt.ylabel("Speedup S(P)")

plt.title("Strong Scaling: Measured vs Ideal Speedup")

plt.xticks(threads)

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()

plt.tight_layout()

# Save graph for the lab report
plt.savefig("task_2_4_speedup.png", dpi=300)

plt.show()