class BinaryHeap:
    def __init__(self, is_min_heap=True):
        self.heap = []
        self.is_min_heap = is_min_heap

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def compare(self, a, b):
        if self.is_min_heap:
            return a < b
        else:
            return a > b

    def heapify_up(self, i):
        while i > 0 and self.compare(self.heap[i], self.heap[self.parent(i)]):
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def heapify_down(self, i):
        min_index = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < len(self.heap) and self.compare(self.heap[left], self.heap[min_index]):
            min_index = left

        if right < len(self.heap) and self.compare(self.heap[right], self.heap[min_index]):
            min_index = right

        if i != min_index:
            self.swap(i, min_index)
            self.heapify_down(min_index)

    def insert(self, key):
        self.heap.append(key)
        self.heapify_up(len(self.heap) - 1)

    def extract_min_max(self):
        if not self.heap:
            return None

        root = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()

        if self.heap:
            self.heapify_down(0)

        return root

    def search(self, key):
        return key in self.heap

    def build_heap(self, array):
        self.heap = array.copy()
        for i in range(len(self.heap) // 2, -1, -1):
            self.heapify_down(i)

    def __str__(self):
        return str(self.heap)


def demonstrate_heap_operations():
    heap = BinaryHeap(is_min_heap=True)

    initial_array = [5, 2, 3, 7, 1]
    heap.build_heap(initial_array)

    print("Initial array:", initial_array)
    print("Min-heap after building:", heap)

    print("\nInserting value 0")
    heap.insert(0)
    print("Min-heap after insertion:", heap)

    value_to_search = 7
    print(f"\nSearching for {value_to_search}:", heap.search(value_to_search))

    print("\nRemoving the minimum element (root)")
    min_element = heap.extract_min_max()
    print(f"Removed element: {min_element}")
    print("Min-heap after removal:", heap)

    print("\n--- Max-Heap Demo ---")
    max_heap = BinaryHeap(is_min_heap=False)
    max_heap.build_heap(initial_array)
    print("Max-heap after building:", max_heap)

    max_element = max_heap.extract_min_max()
    print(f"Removed maximum element: {max_element}")
    print("Max-heap after removal:", max_heap)


if __name__ == "__main__":
    demonstrate_heap_operations()