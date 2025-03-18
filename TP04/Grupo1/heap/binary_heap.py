from typing import List, Optional, Any, Callable


class BinaryHeap:
    def __init__(self, is_min_heap: bool = True, custom_comparator: Optional[Callable[[Any, Any], bool]] = None):
        self.heap_array: List[Any] = []
        self.is_min_heap = is_min_heap
        self.comparator = custom_comparator or self._default_comparator

    def _default_comparator(self, a: Any, b: Any) -> bool:
        if self.is_min_heap:
            return a > b
        else:
            return a < b

    def build_heap(self, arr: List[Any]) -> None:
        self.heap_array = arr.copy()

        n = len(self.heap_array)
        for i in range(n // 2 - 1, -1, -1):
            self._heapify_down(i)

    def _heapify_down(self, idx: int) -> None:

        size = len(self.heap_array)
        target_idx = idx

        left = 2 * idx + 1
        right = 2 * idx + 2

        if left < size and self.comparator(self.heap_array[target_idx], self.heap_array[left]):
            target_idx = left

        if right < size and self.comparator(self.heap_array[target_idx], self.heap_array[right]):
            target_idx = right

        if target_idx != idx:
            self.heap_array[idx], self.heap_array[target_idx] = self.heap_array[target_idx], self.heap_array[idx]
            self._heapify_down(target_idx)

    def _heapify_up(self, idx: int) -> None:
        if idx == 0:
            return

        parent = (idx - 1) // 2

        if self.comparator(self.heap_array[parent], self.heap_array[idx]):
            self.heap_array[idx], self.heap_array[parent] = self.heap_array[parent], self.heap_array[idx]
            self._heapify_up(parent)

    def get_array(self) -> List[Any]:
        return self.heap_array.copy()

    def is_empty(self) -> bool:
        return len(self.heap_array) == 0

    def size(self) -> int:
        return len(self.heap_array)

    def insert(self, value: Any) -> None:
        self.heap_array.append(value)
        self._heapify_up(len(self.heap_array) - 1)