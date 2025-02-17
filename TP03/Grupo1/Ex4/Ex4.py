from TP03.bst.binary_search_tree import BinarySearchTree
from TP03.bst.node import Node
from TP03.bst.visualization import BSTVisualizer
from TP03.performance_analyzer.decorators import measure_performance
import sys


class BSTValidator(BinarySearchTree):

    @measure_performance("validate")
    def is_valid_bst(self) -> bool:
        return self._is_valid_recursive(self.root, -sys.maxsize, sys.maxsize)

    def _is_valid_recursive(self, node: Node, min_val: int, max_val: int) -> bool:
        if not node:
            return True

        self.analyzer.record_comparison()
        if node.value <= min_val or node.value >= max_val:
            return False

        return (self._is_valid_recursive(node.left, min_val, node.value) and
                self._is_valid_recursive(node.right, node.value, max_val))

    def invalidate_node(self, target_value: int, new_value: int) -> None:
        node = self._find_node(self.root, target_value)
        if node:
            node.value = new_value

    def _find_node(self, node: Node, value: int) -> Node:
        if not node or node.value == value:
            return node

        if value < node.value:
            return self._find_node(node.left, value)
        return self._find_node(node.right, value)


def test_bst_validation():
    bst = BSTValidator()

    initial_values = [50, 30, 70, 20, 40, 60, 80]
    print("\nBuilding initial tree:")
    for value in initial_values:
        bst.insert(value)

    print(f"Initial in-order traversal: {bst.inorder_traversal()}")

    is_valid = bst.is_valid_bst()
    print(f"\nIs initial tree valid? {is_valid}")

    target_value = 30
    new_invalid_value = 55
    print(f"\nInvalidating tree by changing node {target_value} to {new_invalid_value}")
    bst.invalidate_node(target_value, new_invalid_value)

    print(f"Modified in-order traversal: {bst.inorder_traversal()}")

    is_valid = bst.is_valid_bst()
    print(f"Is modified tree valid? {is_valid}")

    BSTVisualizer.create_validation_performance_plots(bst)


if __name__ == "__main__":
    test_bst_validation()