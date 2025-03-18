import random
from typing import List
from TP04.Grupo1.heap.binary_heap import BinaryHeap
from TP04.Grupo1.heap.heap_analyzer import HeapAnalyzer

class HeapInserter:
    @staticmethod
    def insert(heap: BinaryHeap, value: int) -> None:
        heap.insert(value)

    @staticmethod
    def analyze_insertion(sizes: List[int], trials: int = 5) -> None:
        def setup_insertion(size: int) -> dict:
            arr = [random.randint(1, 10000) for _ in range(size)]
            heap = BinaryHeap()
            heap.build_heap(arr)
            value = random.randint(1, 10000)
            return {"heap": heap, "value": value}

        def run_insertion(heap: BinaryHeap, value: int) -> None:
            HeapInserter.insert(heap, value)

        print("\nAnalyzing time complexity of heap insertion...")
        sizes, times = HeapAnalyzer.analyze_operation(
            operation_func=run_insertion,
            sizes=sizes,
            setup_func=setup_insertion,
            trials=trials
        )

        HeapAnalyzer.plot_time_complexity(
            sizes=sizes,
            times=times,
            operation="Binary Heap Insertion",
            expected_complexity="O(log n)",
            filename="heap_insertion_time_complexity.png"
        )


def main() -> None:
    example_list = [5, 2, 3, 7, 1]

    min_heap = BinaryHeap(is_min_heap=True)
    min_heap.build_heap(example_list)

    value_to_insert = 0

    print("Original heap:", min_heap.get_array())
    print(f"Inserting value: {value_to_insert}")

    HeapInserter.insert(min_heap, value_to_insert)

    print("Heap after insertion:", min_heap.get_array())

    HeapInserter.analyze_insertion(
        sizes=[100, 500, 1000, 5000, 10000, 50000, 100000]
    )


if __name__ == "__main__":
    main()