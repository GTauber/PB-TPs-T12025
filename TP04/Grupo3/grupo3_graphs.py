import matplotlib.pyplot as plt
import time
import random
import string
import networkx as nx

from TP04.Grupo3.grupo3 import Graph


def generate_random_graph(n_nodes, edge_probability=0.1):
    nodes = list(string.ascii_uppercase[:n_nodes])
    edges = []

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if random.random() < edge_probability:
                edges.append((nodes[i], nodes[j]))

    return nodes, edges


def visualize_example_graph():
    print("Visualizing Example Graph")
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')]
    G = nx.Graph()
    G.add_edges_from(edges)

    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=500, font_size=15, font_weight='bold')

    plt.title("Example Graph")
    plt.savefig("example_graph.png")
    plt.show()


def visualize_traversals():
    print("Visualizing Graph Traversals")
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')]

    graph = Graph(is_directed=False)
    graph.build_from_edges(edges)

    dfs_result = graph.dfs('A')
    bfs_result = graph.bfs('A')

    G = nx.Graph()
    G.add_edges_from(edges)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    node_colors = ['red' if node == 'A' else 'lightblue' for node in G.nodes()]
    edge_colors = []

    for i in range(len(dfs_result) - 1):
        if (dfs_result[i], dfs_result[i + 1]) in G.edges() or (dfs_result[i + 1], dfs_result[i]) in G.edges():
            edge_colors.append('red')
        else:
            edge_colors.append('black')

    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            node_size=500, font_size=15, font_weight='bold')

    # Add traversal order
    for i, node in enumerate(dfs_result):
        plt.text(pos[node][0], pos[node][1] + 0.1, str(i + 1),
                 fontsize=12, ha='center')

    plt.title("DFS Traversal from A")

    plt.subplot(1, 2, 2)
    node_colors = ['red' if node == 'A' else 'lightblue' for node in G.nodes()]

    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            node_size=500, font_size=15, font_weight='bold')

    # Add traversal order
    for i, node in enumerate(bfs_result):
        plt.text(pos[node][0], pos[node][1] + 0.1, str(i + 1),
                 fontsize=12, ha='center')

    plt.title("BFS Traversal from A")

    plt.tight_layout()
    plt.savefig("traversals.png")
    plt.show()


def compare_performance():
    print("Comparing DFS and BFS Performance")
    sizes = [10, 50, 100, 200, 500]
    dfs_times = []
    bfs_times = []

    for size in sizes:
        nodes, edges = generate_random_graph(min(size, 26), 0.1)

        if size > 26:
            extra_nodes = [f"Node{i}" for i in range(size - 26)]
            all_nodes = nodes + extra_nodes

            for node in extra_nodes:
                connect_to = random.sample(all_nodes, min(5, len(all_nodes)))
                for target in connect_to:
                    if node != target:
                        edges.append((node, target))

            nodes = all_nodes

        graph = Graph(is_directed=False)
        graph.build_from_edges(edges)

        start = time.time()
        graph.dfs(nodes[0])
        end = time.time()
        dfs_times.append(end - start)

        start = time.time()
        graph.bfs(nodes[0])
        end = time.time()
        bfs_times.append(end - start)

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, dfs_times, 'o-', label='DFS')
    plt.plot(sizes, bfs_times, 's-', label='BFS')
    plt.title('DFS vs BFS Performance')
    plt.xlabel('Number of nodes')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.savefig("performance_comparison.png")
    plt.show()

visualize_example_graph()
visualize_traversals()
compare_performance()