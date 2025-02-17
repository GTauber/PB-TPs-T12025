from typing import List, Optional

from TP03.performance_analyzer.analyzer import PerformanceAnalyzer, PerformanceVisualizer
from TP03.performance_analyzer.decorators import measure_performance


class Node:
    def __init__(self, value: int):
        self.value = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None


class BinarySearchTree:
    def __init__(self):
        self.root: Optional[Node] = None
        self.analyzer = PerformanceAnalyzer()

    @measure_performance("insert")
    def insert(self, value: int) -> None:
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node: Node, value: int) -> Node:
        self.analyzer.record_comparison()
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)
        return node

    @measure_performance("inorder")
    def inorder_traversal(self) -> List[int]:
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node: Optional[Node], result: List[int]):
        if node:
            self.analyzer.record_comparison()
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    @measure_performance("preorder")
    def preorder_traversal(self) -> List[int]:
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node: Optional[Node], result: List[int]):
        if node:
            self.analyzer.record_comparison()
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    @measure_performance("postorder")
    def postorder_traversal(self) -> List[int]:
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node: Optional[Node], result: List[int]):
        if node:
            self.analyzer.record_comparison()
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)

    def visualize_performance(self, plot_type: str = 'line'):
        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type=plot_type,
            title='Binary Search Tree Performance',
        )


if __name__ == "__main__":
    bst = BinarySearchTree()
    test_values = [50, 30, 70, 20, 40, 60, 80]

    print("Inserting values:", test_values)
    for value in test_values:
        bst.insert(value)

    inorder_result = bst.inorder_traversal()
    preorder_result = bst.preorder_traversal()
    postorder_result = bst.postorder_traversal()

    print("\nResults:")
    print(f"In-order: {' '.join(map(str, inorder_result))}")
    print(f"Pre-order: {' '.join(map(str, preorder_result))}")
    print(f"Post-order: {' '.join(map(str, postorder_result))}")

    print("\nGenerating views and charts")
    print("\n1. Lines chart")
    bst.visualize_performance('line')

    print("\n2. Bar chart")
    bst.visualize_performance('bar')

    print("\n3. Candlestick chart")
    bst.visualize_performance('candlestick')

    print("\n4. Heatmap chart")
    bst.visualize_performance('heatmap')