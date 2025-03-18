import matplotlib.pyplot as plt
import numpy as np
import time
import random

from TP04.Grupo1.Ex04.Ex04 import BinaryHeap


def measure_heap_operations(sizes):
    build_times = []
    insert_times = []
    extract_times = []

    for size in sizes:
        arr = [random.randint(1, 10000) for _ in range(size)]

        heap = BinaryHeap()
        start = time.time()
        heap.build_heap(arr)
        end = time.time()
        build_times.append(end - start)

        start = time.time()
        heap.insert(0)
        end = time.time()
        insert_times.append(end - start)

        start = time.time()
        heap.extract_min_max()
        end = time.time()
        extract_times.append(end - start)

    return build_times, insert_times, extract_times


def plot_time_complexity():
    sizes = [100, 500, 1000, 5000, 10000, 20000, 50000]
    build_times, insert_times, extract_times = measure_heap_operations(sizes)

    plt.figure(figsize=(14, 8))

    plt.subplot(1, 2, 1)
    plt.plot(sizes, build_times, 'o-', label='Build Heap (Actual)')
    plt.plot(sizes, insert_times, 's-', label='Insert (Actual)')
    plt.plot(sizes, extract_times, '^-', label='Extract Min/Max (Actual)')

    plt.title('Actual Time Measurements')
    plt.xlabel('Number of Elements (n)')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)

    build_theoretical = [n * np.log2(n) / 10000 for n in sizes]
    insert_theoretical = [np.log2(n) / 1000 for n in sizes]
    extract_theoretical = [np.log2(n) / 1000 for n in sizes]
    plt.plot(sizes, build_theoretical, 'o-', label='Build Heap - O(n)')
    plt.plot(sizes, insert_theoretical, 's-', label='Insert - O(log n)')
    plt.plot(sizes, extract_theoretical, '^-', label='Extract Min/Max - O(log n)')

    plt.title('Theoretical Time Complexity')
    plt.xlabel('Number of Elements (n)')
    plt.ylabel('Normalized Time')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('heap_time_complexity.png')
    plt.show()


plot_time_complexity()
