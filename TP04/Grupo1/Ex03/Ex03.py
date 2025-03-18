from typing import Any
import matplotlib.pyplot as plt
import random
import time
from TP04.Grupo1.heap.binary_heap import BinaryHeap


def search_in_heap(heap: BinaryHeap, value: Any) -> bool:
    return value in heap.get_array()


def analyze_search_performance(max_size: int = 1000, step: int = 100) -> None:
    sizes = list(range(step, max_size + 1, step))
    search_times = []
    theoretical_times = []

    for size in sizes:
        data = list(range(size))
        random.shuffle(data)

        heap = BinaryHeap()
        heap.build_heap(data)

        start_time = time.time()

        for _ in range(100):
            target = random.choice(data)
            search_in_heap(heap, target)

        end_time = time.time()

        avg_time = (end_time - start_time) / 100
        search_times.append(avg_time)

        if len(search_times) > 0:
            theoretical_times.append(size / sizes[0] * search_times[0])

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, search_times, 'bo-', label='Actual search time')
    plt.plot(sizes, theoretical_times, 'r--', label='Theoretical O(n) complexity')
    plt.xlabel('Heap Size')
    plt.ylabel('Time (seconds)')
    plt.title('Binary Heap Search Performance Analysis')
    plt.legend()
    plt.grid(True)
    plt.savefig('heap_search_performance.png')
    plt.close()


def demonstrate_heap_search() -> None:
    example_data = [5, 2, 3, 7, 1]

    heap = BinaryHeap()
    heap.build_heap(example_data)

    print(f"Original list: {example_data}")
    print(f"Heap after building: {heap.get_array()}")

    heap.insert(0)
    print(f"Heap after inserting 0: {heap.get_array()}")

    value_to_search = 7
    found = search_in_heap(heap, value_to_search)
    print(f"Value {value_to_search} found in heap: {found}")

    value_not_present = 10
    found = search_in_heap(heap, value_not_present)
    print(f"Value {value_not_present} found in heap: {found}")


if __name__ == "__main__":
    demonstrate_heap_search()

    analyze_search_performance()