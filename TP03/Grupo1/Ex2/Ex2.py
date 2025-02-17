from typing import List, Optional, Dict

from matplotlib import pyplot as plt

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
        self.tree_states: List[Dict] = []  # Store tree states for analysis

    def _save_tree_state(self, operation: str):
        current_state = {
            'operation': operation,
            'inorder': self.inorder_traversal()
        }
        self.tree_states.append(current_state)

    @measure_performance("insert")
    def insert(self, value: int) -> None:
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
        self._save_tree_state(f"insert_{value}")

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

    @measure_performance("delete")
    def delete(self, value: int) -> None:
        self.root = self._delete_recursive(self.root, value)
        self._save_tree_state(f"delete_{value}")

    def _delete_recursive(self, node: Optional[Node], value: int) -> Optional[Node]:
        if not node:
            return None

        self.analyzer.record_comparison()
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            successor_value = self._find_min_value(node.right)
            node.value = successor_value
            node.right = self._delete_recursive(node.right, successor_value)

        return node

    def _find_min_value(self, node: Node) -> int:
        current = node
        while current.left:
            self.analyzer.record_comparison()
            current = current.left
        return current.value

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

    def visualize_deletion_performance(self):
        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='line',
            title='bst Operations Performance'
        )

        plt.figure(figsize=(12, 6))
        for i, state in enumerate(self.tree_states):
            plt.subplot(2, 1, 1)
            plt.plot(range(len(state['inorder'])), state['inorder'],
                     label=f"After {state['operation']}")

        plt.title('Tree Structure Evolution')
        plt.xlabel('Node Index')
        plt.ylabel('Node Value')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()


def test_bst_deletion():
    bst = BinarySearchTree()
    initial_values = [50, 30, 70, 20, 40, 60, 80]

    print("Initial tree construction:")
    for value in initial_values:
        bst.insert(value)
        print(f"After inserting {value}: {bst.inorder_traversal()}")

    nodes_to_delete = [20, 30, 50]
    print("\nDeletion test cases:")
    for value in nodes_to_delete:
        print(f"\nDeleting {value}:")
        print(f"Before deletion: {bst.inorder_traversal()}")
        bst.delete(value)
        print(f"After deletion:  {bst.inorder_traversal()}")

    bst.visualize_deletion_performance()


if __name__ == "__main__":
    test_bst_deletion()