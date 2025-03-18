import random
from typing import List
from TP04.Grupo1.heap.binary_heap import BinaryHeap
from TP04.Grupo1.heap.heap_analyzer import HeapAnalyzer


class HeapCreator:

    @staticmethod
    def create_heap(input_list: List[int], is_min_heap: bool = True) -> BinaryHeap:
        heap = BinaryHeap(is_min_heap=is_min_heap)
        heap.build_heap(input_list)
        return heap

    @staticmethod
    def display_heap(heap: BinaryHeap) -> List[int]:
        return heap.get_array()

    @staticmethod
    def analyze_heap_creation(sizes: List[int], trials: int = 5) -> None:


        def setup_heap_creation(size: int) -> dict:
            return {"arr": [random.randint(1, 10000) for _ in range(size)]}

        def run_heap_creation(arr: List[int]) -> BinaryHeap:
            heap = BinaryHeap()
            heap.build_heap(arr)
            return heap

        print("\nStarting heap creation analysis...")
        sizes, times = HeapAnalyzer.analyze_operation(
            operation_func=run_heap_creation,
            sizes=sizes,
            setup_func=setup_heap_creation,
            trials=trials
        )

        HeapAnalyzer.plot_time_complexity(
            sizes=sizes,
            times=times,
            operation="Binary Heap Creation",
            expected_complexity="O(n)",
            filename="heap_creation_time_complexity.png"
        )


def main() -> None:
    example_list = [5, 2, 3, 7, 1]

    min_heap = HeapCreator.create_heap(example_list, is_min_heap=True)
    max_heap = HeapCreator.create_heap(example_list, is_min_heap=False)

    print("Original list:", example_list)
    print("After heapify (min-heap):", HeapCreator.display_heap(min_heap))
    print("After heapify (max-heap):", HeapCreator.display_heap(max_heap))

    HeapCreator.analyze_heap_creation(
        sizes=[100, 500, 1000, 5000, 10000, 50000, 100000]
    )


if __name__ == "__main__":
    main()