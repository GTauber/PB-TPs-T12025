from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import List, Tuple
from TP03.performance_analyzer.decorators import measure_performance
from TP03.bst.binary_search_tree import BinarySearchTree
from TP03.bst.node import Node
from TP03.bst.visualization import BSTVisualizer


class ParallelSearchBST(BinarySearchTree):
    def __init__(self):
        super().__init__()
        self.path_lock = Lock()

    @measure_performance("parallel_search")
    def parallel_search(self, value: int) -> Tuple[bool, List[int]]:
        if not self.root:
            return False, []

        self.analyzer.record_comparison()
        if value == self.root.value:
            return True, [self.root.value]

        shared_path = [self.root.value]
        found = [False]

        with ThreadPoolExecutor(max_workers=2) as executor:
            if value < self.root.value and self.root.left:
                left_future = executor.submit(
                    self._parallel_search_recursive,
                    self.root.left,
                    value,
                    shared_path,
                    found
                )

            if value > self.root.value and self.root.right:
                right_future = executor.submit(
                    self._parallel_search_recursive,
                    self.root.right,
                    value,
                    shared_path,
                    found
                )

            if value < self.root.value and self.root.left:
                left_future.result()
            if value > self.root.value and self.root.right:
                right_future.result()

        return found[0], shared_path

    def _parallel_search_recursive(self,
                                   node: Node,
                                   value: int,
                                   shared_path: List[int],
                                   found: List[bool]) -> None:
        if not node or found[0]:
            return

        self.analyzer.record_comparison()

        with self.path_lock:
            shared_path.append(node.value)

        if value == node.value:
            found[0] = True
            return

        if value < node.value:
            self._parallel_search_recursive(node.left, value, shared_path, found)
        else:
            self._parallel_search_recursive(node.right, value, shared_path, found)


def test_parallel_bst_search():
    bst = ParallelSearchBST()

    initial_values = [50, 30, 70, 20, 40, 60, 80, 15, 25, 35, 45, 55, 65, 75, 85]
    print("\nBuilding initial tree:")
    for value in initial_values:
        bst.insert(value)

    print(f"Tree in-order traversal: {bst.inorder_traversal()}")

    test_values = [60, 25, 90, 55, 85, 45]
    sequential_results = []
    parallel_results = []

    print("\nComparing Sequential vs Parallel Search:")
    for value in test_values:
        print(f"\nSearching for value: {value}")

        seq_found, seq_path = bst.search(value)
        sequential_results.append({
            'value': value,
            'found': seq_found,
            'path': seq_path
        })
        print(f"Sequential search path: {' -> '.join(map(str, seq_path))}")

        par_found, par_path = bst.parallel_search(value)
        parallel_results.append({
            'value': value,
            'found': par_found,
            'path': par_path
        })
        print(f"Parallel search path: {' -> '.join(map(str, par_path))}")

        assert seq_found == par_found, f"Search results don't match for value {value}"

    print("\nGenerating performance visualizations...")
    BSTVisualizer.visualize_search_performance(bst, test_values)

    return sequential_results, parallel_results


if __name__ == "__main__":
    sequential_results, parallel_results = test_parallel_bst_search()
    print("\nAnalysis complete! Check the generated visualization files.")