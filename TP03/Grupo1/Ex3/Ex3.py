from TP03.bst.binary_search_tree import BinarySearchTree
from TP03.bst.visualization import BSTVisualizer


def test_bst_search():
    bst = BinarySearchTree()
    initial_values = [50, 30, 70, 20, 40, 60, 80]

    print("Building initial tree:")
    for value in initial_values:
        bst.insert(value)
    print(f"Tree in-order traversal: {bst.inorder_traversal()}")

    search_values = [40, 45, 70, 90]
    results = []

    print("\nPerforming searches:")
    for value in search_values:
        found, path = bst.search(value)
        results.append((value, found, path))
        print(f"\nSearching for {value}:")
        print(f"Found: {found}")
        print(f"Search path: {' -> '.join(map(str, path))}")

    print("\nGenerating search performance visualizations...")
    BSTVisualizer.visualize_search_performance(bst, [v for v, _, _ in results])


if __name__ == "__main__":
    test_bst_search()