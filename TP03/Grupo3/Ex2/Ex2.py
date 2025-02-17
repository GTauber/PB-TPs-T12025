from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Event
from typing import List, Optional, Tuple
from TP03.performance_analyzer.decorators import measure_performance
from TP03.bst.binary_search_tree import BinarySearchTree
from TP03.bst.node import Node
from TP03.bst.visualization import BSTVisualizer


class ParallelDFSTree(BinarySearchTree):
    def __init__(self):
        super().__init__()
        self.path_lock = Lock()
        self.found_event = Event()

    @measure_performance("sequential_dfs")
    def sequential_dfs(self, target: int) -> Tuple[bool, List[int]]:
        path = []
        found = self._dfs_recursive(self.root, target, path)
        return found, path

    def _dfs_recursive(self, node: Optional[Node], target: int, path: List[int]) -> bool:
        if not node:
            return False

        self.analyzer.record_comparison()
        path.append(node.value)

        if node.value == target:
            return True

        if self._dfs_recursive(node.left, target, path):
            return True

        if self._dfs_recursive(node.right, target, path):
            return True

        path.pop()
        return False

    @measure_performance("parallel_dfs")
    def parallel_dfs(self, target: int) -> Tuple[bool, List[int]]:
        if not self.root:
            return False, []

        self.found_event.clear()
        shared_path = [self.root.value]

        self.analyzer.record_comparison()
        if self.root.value == target:
            return True, shared_path

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = []

            if self.root.left:
                futures.append(executor.submit(
                    self._parallel_dfs_recursive,
                    self.root.left,
                    target,
                    [self.root.value]
                ))

            if self.root.right:
                futures.append(executor.submit(
                    self._parallel_dfs_recursive,
                    self.root.right,
                    target,
                    [self.root.value]
                ))

            for future in futures:
                result = future.result()
                if result[0]:
                    return result

        return False, []

    def _parallel_dfs_recursive(self,
                                node: Node,
                                target: int,
                                current_path: List[int]) -> Tuple[bool, List[int]]:
        if not node or self.found_event.is_set():
            return False, []

        self.analyzer.record_comparison()
        current_path = current_path + [node.value]

        if node.value == target:
            self.found_event.set()
            return True, current_path

        if node.left:
            left_result = self._parallel_dfs_recursive(node.left, target, current_path)
            if left_result[0]:
                return left_result

        if node.right:
            right_result = self._parallel_dfs_recursive(node.right, target, current_path)
            if right_result[0]:
                return right_result

        return False, []


def test_parallel_dfs():
    tree = ParallelDFSTree()

    values = [8, 3, 10, 1, 6, 14, 4, 7, 13]
    print("\nBuilding test tree:")
    for value in values:
        tree.insert(value)

    print(f"Tree in-order traversal: {tree.inorder_traversal()}")

    test_values = [6, 13, 5, 14, 1, 7]
    sequential_results = []
    parallel_results = []

    print("\nComparing Sequential vs Parallel DFS:")
    for target in test_values:
        print(f"\nSearching for value: {target}")

        seq_found, seq_path = tree.sequential_dfs(target)
        sequential_results.append({
            'target': target,
            'found': seq_found,
            'path': seq_path
        })
        path_str = ' -> '.join(map(str, seq_path)) if seq_path else "Not found"
        print(f"Sequential DFS path: {path_str}")

        par_found, par_path = tree.parallel_dfs(target)
        parallel_results.append({
            'target': target,
            'found': par_found,
            'path': par_path
        })
        path_str = ' -> '.join(map(str, par_path)) if par_path else "Not found"
        print(f"Parallel DFS path: {path_str}")

        if seq_found and par_found:
            assert seq_path[-1] == par_path[-1] == target, "Invalid path: doesn't end at target"
            assert seq_path[0] == par_path[0] == tree.root.value, "Invalid path: doesn't start at root"

    print("\nGenerating performance visualizations...")
    BSTVisualizer.visualize_dfs_performance(tree, test_values)

    return sequential_results, parallel_results


if __name__ == "__main__":
    sequential_results, parallel_results = test_parallel_dfs()
    print("\nAnalysis complete! Check the generated visualization files.")