import heapq
import matplotlib.pyplot as plt
import time
import random
import math


def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


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


def analyze_complexity():
    sizes = [5, 10, 15, 20, 25, 30]
    times = []

    for size in sizes:
        graph = generate_random_graph(size, edge_density=0.3)
        start_vertex = list(graph.keys())[0]

        start_time = time.time()
        dijkstra(graph, start_vertex)
        end_time = time.time()

        times.append(end_time - start_time)

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, 'bo-', linewidth=2, markersize=8, label='Tempo Real')

    max_time = max(times)
    if max_time == 0:
        max_time = 0.001

    last_size = sizes[-1]
    last_theoretical = (last_size + (last_size * last_size * 0.3)) * math.log2(last_size)
    normalization_factor = max_time / last_theoretical

    theoretical = [(size + (size * size * 0.3)) * math.log2(size) * normalization_factor for size in sizes]
    plt.plot(sizes, theoretical, 'r--', linewidth=2, label='Complexidade Teórica O(E + V log V)')

    plt.title('Análise de Complexidade: Algoritmo de Dijkstra')
    plt.xlabel('Número de Vértices (V)')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)

    plt.figtext(0.5, 0.01, f'Fator de normalização: {normalization_factor:.10f}', ha='center')

    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig("dijkstra_complexity.png")
    plt.close()


def main():
    graph1 = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 5)],
        'C': [('A', 4), ('B', 2), ('D', 1)],
        'D': [('B', 5), ('C', 1)]
    }

    start_vertex = 'A'
    print("Teste 1: Grafo Original")
    distances = dijkstra(graph1, start_vertex)

    for vertex in sorted(distances):
        print(f"Distância até {vertex}: {distances[vertex]}")

    graph2 = generate_random_graph(8, edge_density=0.4)
    start_vertex2 = list(graph2.keys())[0]

    print("\nTeste 2: Grafo Aleatório")
    distances2 = dijkstra(graph2, start_vertex2)

    for vertex in sorted(distances2):
        print(f"Distância até {vertex}: {distances2[vertex]}")

    analyze_complexity()


if __name__ == "__main__":
    main()