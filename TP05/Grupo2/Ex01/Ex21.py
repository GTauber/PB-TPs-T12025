import matplotlib.pyplot as plt
import random
import time
import math
import numpy as np


def knapsack_greedy(items, capacity):
    items_with_ratio = []
    for item_id, (weight, value) in items.items():
        ratio = value / weight
        items_with_ratio.append((item_id, weight, value, ratio))

    items_with_ratio.sort(key=lambda x: x[3], reverse=True)

    total_weight = 0
    total_value = 0
    selected_items = []

    for item_id, weight, value, ratio in items_with_ratio:
        if total_weight + weight <= capacity:
            selected_items.append((item_id, weight, value))
            total_weight += weight
            total_value += value

    return selected_items, total_weight, total_value


def knapsack_brute_force(items, capacity):
    def generate_all_subsets(item_ids):
        if not item_ids:
            return [[]]

        first = item_ids[0]
        rest = generate_all_subsets(item_ids[1:])

        return rest + [[first] + subset for subset in rest]

    item_ids = list(items.keys())
    all_subsets = generate_all_subsets(item_ids)

    best_value = 0
    best_subset = []

    for subset in all_subsets:
        total_weight = sum(items[item_id][0] for item_id in subset)
        total_value = sum(items[item_id][1] for item_id in subset)

        if total_weight <= capacity and total_value > best_value:
            best_value = total_value
            best_subset = subset

    selected_items = [(item_id, items[item_id][0], items[item_id][1]) for item_id in best_subset]
    total_weight = sum(weight for _, weight, _ in selected_items)

    return selected_items, total_weight, best_value


def generate_random_items(n, min_weight=1, max_weight=20, min_value=10, max_value=200):
    items = {}
    for i in range(1, n + 1):
        weight = random.randint(min_weight, max_weight)
        value = random.randint(min_value, max_value)
        items[f"item{i}"] = (weight, value)
    return items


def run_test(items, capacity, test_name):
    print(f"\n=== Teste {test_name} ===")
    print(f"Capacidade da mochila: {capacity}")
    print("Itens disponíveis:")
    for item_id, (weight, value) in items.items():
        ratio = value / weight
        print(f"• {item_id}: peso {weight}, valor {value}, ratio {ratio:.2f}")

    print("\nSolução Gulosa:")
    start_time = time.time()
    selected_greedy, weight_greedy, value_greedy = knapsack_greedy(items, capacity)
    greedy_time = time.time() - start_time

    for item_id, weight, value in selected_greedy:
        print(f"• {item_id}: peso {weight}, valor {value}")

    print(f"Peso total: {weight_greedy}/{capacity}")
    print(f"Valor total: {value_greedy}")
    print(f"Tempo de execução: {greedy_time:.6f} segundos")

    if len(items) <= 20:
        print("\nSolução Força Bruta (ótima):")
        start_time = time.time()
        selected_optimal, weight_optimal, value_optimal = knapsack_brute_force(items, capacity)
        optimal_time = time.time() - start_time

        for item_id, weight, value in selected_optimal:
            print(f"• {item_id}: peso {weight}, valor {value}")

        print(f"Peso total: {weight_optimal}/{capacity}")
        print(f"Valor total: {value_optimal}")
        print(f"Tempo de execução: {optimal_time:.6f} segundos")

        print(f"\nEficiência da heurística: {value_greedy / value_optimal * 100:.2f}%")

        return {
            "greedy": {"value": value_greedy, "time": greedy_time},
            "optimal": {"value": value_optimal, "time": optimal_time}
        }
    else:
        return {
            "greedy": {"value": value_greedy, "time": greedy_time}
        }


def analyze_performance():
    sizes = [5, 10, 15, 20, 25, 30]
    greedy_times = []
    optimal_times = []
    efficiency_ratios = []

    for size in sizes:
        items = generate_random_items(size)
        capacity = sum(weight for weight, _ in items.values()) // 2

        print(f"\nAnalisando desempenho para {size} itens...")

        start_time = time.time()
        _, _, value_greedy = knapsack_greedy(items, capacity)
        greedy_time = time.time() - start_time
        greedy_times.append(greedy_time)

        if size <= 20:
            start_time = time.time()
            _, _, value_optimal = knapsack_brute_force(items, capacity)
            optimal_time = time.time() - start_time
            optimal_times.append(optimal_time)

            efficiency = value_greedy / value_optimal * 100
            efficiency_ratios.append(efficiency)
            print(f"Eficiência: {efficiency:.2f}%, Tempo guloso: {greedy_time:.6f}s, Tempo ótimo: {optimal_time:.6f}s")
        else:
            optimal_times.append(None)
            efficiency_ratios.append(None)
            print(f"Tempo guloso: {greedy_time:.6f}s, Solução ótima não calculada (muito grande)")

    plt.figure(figsize=(12, 15))

    plt.subplot(3, 1, 1)
    plt.plot(sizes, greedy_times, 'bo-', label='Heurística Gulosa')

    valid_optimal = [(sizes[i], optimal_times[i]) for i in range(len(sizes)) if optimal_times[i] is not None]
    if valid_optimal:
        plt.plot([x for x, _ in valid_optimal], [y for _, y in valid_optimal], 'ro-', label='Força Bruta')

    plt.yscale('log')
    plt.title('Tempo de Execução (escala log)')
    plt.xlabel('Número de Itens')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 2)
    valid_efficiency = [(sizes[i], efficiency_ratios[i]) for i in range(len(sizes)) if efficiency_ratios[i] is not None]
    if valid_efficiency:
        plt.plot([x for x, _ in valid_efficiency], [y for _, y in valid_efficiency], 'go-')
        plt.axhline(y=100, color='r', linestyle='--', label='Solução Ótima (100%)')
        plt.title('Eficiência da Heurística Gulosa')
        plt.xlabel('Número de Itens')
        plt.ylabel('Eficiência (%)')
        plt.ylim(0, 110)
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    plt.savefig('knapsack_performance.png')
    plt.close()


def analyze_complexity_comparison():
    sizes = list(range(10, 1001, 10))
    greedy_times = []

    for size in sizes:
        items = generate_random_items(size)
        capacity = sum(weight for weight, _ in items.values()) // 2

        if size % 100 == 0:
            print(f"Testando com {size} itens...")

        start_time = time.time()
        knapsack_greedy(items, capacity)
        end_time = time.time()

        greedy_times.append(end_time - start_time)

    n_log_n = [n * math.log2(n) for n in sizes]
    max_time = max(greedy_times)
    max_theoretical = max(n_log_n)
    normalized_theoretical = [t * (max_time / max_theoretical) for t in n_log_n]

    z = np.polyfit(n_log_n, greedy_times, 1)
    p = np.poly1d(z)
    r_squared = 1 - np.sum((np.array(greedy_times) - p(n_log_n)) ** 2) / np.sum(
        (np.array(greedy_times) - np.mean(greedy_times)) ** 2)

    plt.figure(figsize=(12, 10))

    plt.subplot(2, 1, 1)
    plt.plot(sizes, greedy_times, 'bo-', label='Tempo Real')
    plt.plot(sizes, normalized_theoretical, 'r--', label='Complexidade Teórica O(n log n)')
    plt.title(f'Comparação de Complexidade: Algoritmo Guloso para o Problema da Mochila\nR² = {r_squared:.4f}')
    plt.xlabel('Número de Itens (n)')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.loglog(sizes, greedy_times, 'bo-', label='Tempo Real (log-log)')
    plt.loglog(sizes, normalized_theoretical, 'r--', label='Complexidade Teórica O(n log n)')
    plt.title('Comparação de Complexidade (Escala Log-Log)')
    plt.xlabel('Número de Itens (n) - Escala Log')
    plt.ylabel('Tempo (segundos) - Escala Log')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('knapsack_complexity_comparison.png')
    plt.close()

    print(f"Análise de complexidade concluída. R² = {r_squared:.4f}")


def main():
    random.seed(42)

    test1_items = {
        "item1": (2, 40),
        "item2": (3, 50),
        "item3": (5, 100),
        "item4": (4, 90)
    }
    run_test(test1_items, 8, "Exemplo")

    test2_items = {
        "A": (1, 10),
        "B": (2, 25),
        "C": (3, 30),
        "D": (4, 45),
        "E": (5, 50),
        "F": (6, 55),
        "G": (7, 65),
        "H": (8, 70),
    }
    run_test(test2_items, 15, "Itens com Valores Progressivos")

    test3_items = generate_random_items(30)
    run_test(test3_items, sum(weight for weight, _ in test3_items.values()) // 3, "Conjunto Grande (30 itens)")

    print("\nIniciando análise de desempenho...")
    analyze_performance()

    print("\nIniciando análise de complexidade...")
    analyze_complexity_comparison()

if __name__ == "__main__":
    main()