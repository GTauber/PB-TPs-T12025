import heapq
import matplotlib.pyplot as plt
import time
import random
import math


def prim(graph, start):
    mst = []
    visited = {start}
    edges = [(weight, start, neighbor) for neighbor, weight in graph[start]]
    heapq.heapify(edges)

    while edges and len(visited) < len(graph):
        weight, vertex1, vertex2 = heapq.heappop(edges)

        if vertex2 not in visited:
            visited.add(vertex2)
            mst.append((vertex1, vertex2, weight))

            for neighbor, w in graph[vertex2]:
                if neighbor not in visited:
                    heapq.heappush(edges, (w, vertex2, neighbor))

    return mst


def generate_random_graph(n_vertices, edge_density=0.5, min_weight=1, max_weight=10):
    vertices = [chr(65 + i) if i < 26 else f'V{i}' for i in range(n_vertices)]
    graph = {v: [] for v in vertices}

    for i in range(n_vertices):
        for j in range(i + 1, n_vertices):
            if random.random() < edge_density:
                weight = random.randint(min_weight, max_weight)
                graph[vertices[i]].append((vertices[j], weight))
                graph[vertices[j]].append((vertices[i], weight))

    return graph


def generate_grid_graph(rows, cols):
    graph = {}

    for i in range(rows):
        for j in range(cols):
            vertex = f"{i},{j}"
            graph[vertex] = []

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < rows and 0 <= nj < cols:
                    neighbor = f"{ni},{nj}"
                    weight = random.randint(1, 10)
                    graph[vertex].append((neighbor, weight))

    return graph


def analyze_complexity():
    sizes = [10, 20, 50, 100, 200, 500]
    times = []
    edge_counts = []

    for size in sizes:
        graph = generate_random_graph(size, edge_density=0.1)

        edge_count = sum(len(edges) for edges in graph.values()) // 2
        edge_counts.append(edge_count)

        start_vertex = list(graph.keys())[0]

        start_time = time.time()
        prim(graph, start_vertex)
        end_time = time.time()

        times.append(end_time - start_time)
        print(f"Tamanho: {size}, Arestas: {edge_count}, Tempo: {end_time - start_time:.6f}s")

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(sizes, times, 'go-', linewidth=2, markersize=8, label='Tempo Real')

    max_time = max(times)
    if max_time == 0:
        max_time = 0.001

    theoretical = []
    for i, size in enumerate(sizes):
        t = edge_counts[i] * math.log2(size)
        theoretical.append(t)

    normalization_factor = max_time / max(theoretical)
    theoretical = [t * normalization_factor for t in theoretical]

    plt.plot(sizes, theoretical, 'r--', linewidth=2, label='Complexidade Teórica O(E log V)')
    plt.title('Análise de Complexidade: Algoritmo de Prim')
    plt.xlabel('Número de Vértices (V)')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.loglog(sizes, times, 'go-', linewidth=2, markersize=8, label='Tempo Real (log-log)')
    plt.loglog(sizes, theoretical, 'r--', linewidth=2, label='Teórico (log-log)')
    plt.xlabel('Número de Vértices (V) - Escala Log')
    plt.ylabel('Tempo (segundos) - Escala Log')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("prim_complexity_analysis.png")
    plt.close()


def run_test(graph, start_vertex, test_name):
    print(f"\n=== Teste {test_name} ===")
    print(f"Número de vértices: {len(graph)}")
    print(f"Número de arestas: {sum(len(edges) for edges in graph.values()) // 2}")
    print(f"Vértice inicial: {start_vertex}")

    start_time = time.time()
    mst = prim(graph, start_vertex)
    end_time = time.time()

    total_weight = sum(weight for _, _, weight in mst)

    print(f"Tempo de execução: {end_time - start_time:.6f} segundos")
    print("Árvore Geradora Mínima:")

    edge_count = min(5, len(mst))
    for i in range(edge_count):
        u, v, w = mst[i]
        print(f"{u} - {v} com peso {w}")

    if len(mst) > 5:
        print(f"... e mais {len(mst) - 5} arestas")

    print(f"Peso total da MST: {total_weight}")

    return mst, total_weight, end_time - start_time


def main():
    random.seed(42)

    graph1 = {
        'A': [('B', 5), ('C', 3), ('D', 7)],
        'B': [('A', 5), ('C', 2), ('E', 1)],
        'C': [('A', 3), ('B', 2), ('D', 4), ('E', 6)],
        'D': [('A', 7), ('C', 4), ('E', 3)],
        'E': [('B', 1), ('C', 6), ('D', 3)]
    }
    run_test(graph1, 'A', "Grafo Pequeno")

    graph2 = generate_grid_graph(4, 4)
    run_test(graph2, "0,0", "Grafo em Grade 4x4")

    graph3 = generate_random_graph(100, edge_density=0.1)
    run_test(graph3, list(graph3.keys())[0], "Grafo Grande (100 vértices)")
    analyze_complexity()

if __name__ == "__main__":
    main()