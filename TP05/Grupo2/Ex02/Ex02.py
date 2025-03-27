import math
import random
import time
import matplotlib.pyplot as plt
import numpy as np


def calculate_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def calculate_total_distance(route, cities):
    total = 0
    for i in range(len(route) - 1):
        total += calculate_distance(cities[route[i]], cities[route[i + 1]])
    total += calculate_distance(cities[route[-1]], cities[route[0]])
    return total


def nearest_neighbor_tsp(cities, start_city=None):
    if start_city is None:
        start_city = next(iter(cities.keys()))

    unvisited = list(cities.keys())
    current_city = start_city
    unvisited.remove(current_city)
    route = [current_city]

    while unvisited:
        nearest_city = min(unvisited, key=lambda city: calculate_distance(cities[current_city], cities[city]))
        route.append(nearest_city)
        current_city = nearest_city
        unvisited.remove(nearest_city)

    return route


def brute_force_tsp(cities):
    from itertools import permutations

    cities_keys = list(cities.keys())
    start_city = cities_keys[0]
    rest_cities = cities_keys[1:]

    best_route = None
    best_distance = float('inf')

    for perm in permutations(rest_cities):
        route = [start_city] + list(perm)
        distance = calculate_total_distance(route, cities)

        if distance < best_distance:
            best_distance = distance
            best_route = route

    return best_route, best_distance


def generate_random_cities(n, min_coord=0, max_coord=100):
    cities = {}
    for i in range(n):
        city_name = chr(65 + i) if i < 26 else f'Cidade{i + 1}'
        cities[city_name] = (random.uniform(min_coord, max_coord), random.uniform(min_coord, max_coord))
    return cities


def plot_route(cities, route, title):
    plt.figure(figsize=(10, 8))

    x = [cities[city][0] for city in cities]
    y = [cities[city][1] for city in cities]
    plt.scatter(x, y, c='blue', s=100)

    for city, coords in cities.items():
        plt.annotate(city, (coords[0], coords[1]), xytext=(5, 5), textcoords='offset points')

    for i in range(len(route) - 1):
        plt.plot([cities[route[i]][0], cities[route[i + 1]][0]],
                 [cities[route[i]][1], cities[route[i + 1]][1]], 'r-')

    plt.plot([cities[route[-1]][0], cities[route[0]][0]],
             [cities[route[-1]][1], cities[route[0]][1]], 'r-')

    plt.title(title)
    plt.grid(True)
    plt.savefig(f"{title.replace(' ', '_').lower()}.png")
    plt.close()


def analyze_complexity():
    sizes = [10, 20, 30, 40, 50, 75, 100, 150, 200]
    times = []

    for size in sizes:
        cities = generate_random_cities(size)

        start_time = time.time()
        nearest_neighbor_tsp(cities)
        end_time = time.time()

        execution_time = end_time - start_time
        times.append(execution_time)

        print(f"Tamanho: {size}, Tempo: {execution_time:.6f}s")

    plt.figure(figsize=(12, 10))

    plt.subplot(2, 1, 1)
    plt.plot(sizes, times, 'bo-', linewidth=2, markersize=8, label='Tempo Real')

    n_squared = [n ** 2 for n in sizes]
    max_time = max(times)
    max_theoretical = max(n_squared)
    theoretical_times = [t * (max_time / max_theoretical) for t in n_squared]

    z = np.polyfit(n_squared, times, 1)
    p = np.poly1d(z)
    r_squared = 1 - np.sum((np.array(times) - p(n_squared)) ** 2) / np.sum((np.array(times) - np.mean(times)) ** 2)

    plt.plot(sizes, theoretical_times, 'r--', linewidth=2, label='Complexidade Teórica O(n²)')
    plt.title(f'Análise de Complexidade: Heurística do Vizinho Mais Próximo\nR² = {r_squared:.4f}')
    plt.xlabel('Número de Cidades (n)')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.loglog(sizes, times, 'bo-', linewidth=2, label='Tempo Real (log-log)')
    plt.loglog(sizes, theoretical_times, 'r--', linewidth=2, label='Complexidade Teórica O(n²)')
    plt.title('Análise de Complexidade (Escala Log-Log)')
    plt.xlabel('Número de Cidades (n) - Escala Log')
    plt.ylabel('Tempo (segundos) - Escala Log')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('tsp_complexity_analysis.png')
    plt.close()

    return r_squared


def run_test(cities, test_name, compare_with_optimal=False):
    print(f"\n=== Teste {test_name} ===")
    print("Cidades:")
    for city, coords in cities.items():
        print(f"• {city}: {coords}")

    start_time = time.time()
    route = nearest_neighbor_tsp(cities)
    nn_time = time.time() - start_time

    total_distance = calculate_total_distance(route, cities)

    print("\nRota encontrada (Vizinho Mais Próximo):")
    print(" -> ".join(route) + f" -> {route[0]}")
    print(f"Distância total: {total_distance:.2f}")
    print(f"Tempo de execução: {nn_time:.6f} segundos")

    plot_route(cities, route, f"TSP - {test_name}")

    if compare_with_optimal and len(cities) <= 10:
        print("\nCalculando solução ótima (força bruta)...")
        start_time = time.time()
        optimal_route, optimal_distance = brute_force_tsp(cities)
        bf_time = time.time() - start_time

        print("Rota ótima (Força Bruta):")
        print(" -> ".join(optimal_route) + f" -> {optimal_route[0]}")
        print(f"Distância total: {optimal_distance:.2f}")
        print(f"Tempo de execução: {bf_time:.6f} segundos")

        efficiency = (optimal_distance / total_distance) * 100
        print(f"\nEficiência da heurística: {efficiency:.2f}%")

        plot_route(cities, optimal_route, f"TSP Ótimo - {test_name}")

        return {
            "nn": {"route": route, "distance": total_distance, "time": nn_time},
            "optimal": {"route": optimal_route, "distance": optimal_distance, "time": bf_time, "efficiency": efficiency}
        }

    return {
        "nn": {"route": route, "distance": total_distance, "time": nn_time}
    }


def main():
    random.seed(42)

    example_cities = {
        'A': (0, 0),
        'B': (1, 5),
        'C': (5, 2),
        'D': (6, 6),
        'E': (8, 3)
    }
    run_test(example_cities, "Exemplo", compare_with_optimal=True)

    circle_cities = {}
    n_cities = 8
    radius = 10
    for i in range(n_cities):
        angle = 2 * math.pi * i / n_cities
        city_name = chr(65 + i)
        circle_cities[city_name] = (radius * math.cos(angle), radius * math.sin(angle))
    run_test(circle_cities, "Cidades em Círculo", compare_with_optimal=True)

    random_cities = generate_random_cities(50)
    run_test(random_cities, "50 Cidades Aleatórias")

    analyze_complexity()


if __name__ == "__main__":
    main()