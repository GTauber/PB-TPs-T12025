from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List

from TP03.bst.binary_search_tree import BinarySearchTree
from TP03.bst.node import Node
from TP03.bst.visualization import BSTVisualizer
from TP03.performance_analyzer.decorators import measure_performance


@dataclass
class MaxResult:
    """Class to store maximum value finding results"""
    value: int
    path: List[int]
    nodes_visited: int


class ParallelMaxFinder(BinarySearchTree):

    def __init__(self):
        super().__init__()

    @measure_performance("sequential_max")
    def find_max_sequential(self) -> MaxResult:
        if not self.root:
            raise ValueError("Tree is empty")

        nodes_visited = [0]
        path = []
        max_val = self._find_max_recursive(self.root, path, nodes_visited)
        return MaxResult(max_val, path, nodes_visited[0])

    def _find_max_recursive(self, node: Node, path: List[int], nodes_visited: List[int]) -> int:
        if not node:
            return float('-inf')

        self.analyzer.record_comparison()
        nodes_visited[0] += 1
        path.append(node.value)

        current = node
        while current.right:
            self.analyzer.record_comparison()
            nodes_visited[0] += 1
            current = current.right
            path.append(current.value)

        return current.value

    @measure_performance("parallel_max")
    def find_max_parallel(self) -> MaxResult:
        if not self.root:
            raise ValueError("Tree is empty")

        nodes_visited = [0]
        path = [self.root.value]
        nodes_visited[0] += 1

        current = self.root
        max_value = current.value

        with ThreadPoolExecutor(max_workers=2) as executor:
            while current:
                self.analyzer.record_comparison()
                nodes_visited[0] += 1

                futures = []

                if current.left:
                    futures.append(executor.submit(
                        self._find_subtree_max,
                        current.left,
                        [0]
                    ))

                if current.right:
                    path.append(current.right.value)
                    current = current.right
                    max_value = current.value
                    continue

                for future in futures:
                    subtree_result = future.result()
                    nodes_visited[0] += subtree_result.nodes_visited
                    if subtree_result.value > max_value:
                        max_value = subtree_result.value
                        path = subtree_result.path

                break

        return MaxResult(max_value, path, nodes_visited[0])

    def _find_subtree_max(self, node: Node, nodes_visited: List[int]) -> MaxResult:
        if not node:
            return MaxResult(float('-inf'), [], nodes_visited[0])

        self.analyzer.record_comparison()
        nodes_visited[0] += 1
        path = [node.value]

        current = node
        while current.right:
            self.analyzer.record_comparison()
            nodes_visited[0] += 1
            current = current.right
            path.append(current.value)

        return MaxResult(current.value, path, nodes_visited[0])


def test_parallel_max_finder():
    tree = ParallelMaxFinder()

    test_cases = [
        [15, 10, 20, 8, 12, 17, 25],
        [50, 30, 70, 20, 40, 60, 80, 15, 25, 35, 45, 55, 65, 75, 85],
        [1, 2, 3, 4, 5, 6, 7],
        [7, 6, 5, 4, 3, 2, 1]
    ]

    results = []

    for i, values in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Input values: {values}")

        tree = ParallelMaxFinder()
        for value in values:
            tree.insert(value)

        print(f"Tree in-order traversal: {tree.inorder_traversal()}")

        seq_result = tree.find_max_sequential()
        print(f"\nSequential search:")
        print(f"Maximum value: {seq_result.value}")
        print(f"Path taken: {' -> '.join(map(str, seq_result.path))}")
        print(f"Nodes visited: {seq_result.nodes_visited}")

        par_result = tree.find_max_parallel()
        print(f"\nParallel search:")
        print(f"Maximum value: {par_result.value}")
        print(f"Path taken: {' -> '.join(map(str, par_result.path))}")
        print(f"Nodes visited: {par_result.nodes_visited}")

        assert seq_result.value == par_result.value, "Maximum values don't match!"

        results.append({
            'values': values,
            'sequential': seq_result,
            'parallel': par_result
        })

    print("\nGenerating performance visualizations...")
    BSTVisualizer.visualize_max_finder_performance(tree)

    return results


if __name__ == "__main__":
    results = test_parallel_max_finder()
    print("\nAnalysis complete! Check the generated visualization files.")