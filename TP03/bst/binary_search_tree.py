from typing import List, Optional, Dict, Tuple

from TP03.performance_analyzer.analyzer import PerformanceAnalyzer
from TP03.performance_analyzer.decorators import measure_performance
from .node import Node


class BinarySearchTree:
    def __init__(self):
        self.root: Optional[Node] = None
        self.analyzer = PerformanceAnalyzer()
        self.tree_states: List[Dict] = []

    @measure_performance("search")
    def search(self, value: int) -> Tuple[bool, List[int]]:
        path = []
        found = self._search_recursive(self.root, value, path)
        return found, path

    def _search_recursive(self, node: Optional[Node], value: int, path: List[int]) -> bool:
        if not node:
            return False

        self.analyzer.record_comparison()
        path.append(node.value)

        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value, path)
        else:
            return self._search_recursive(node.right, value, path)

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

    @measure_performance("delete")
    def delete(self, value: int) -> None:
        self.root = self._delete_recursive(self.root, value)

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