import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple

import numpy as np

from TP03.performance_analyzer.analyzer import PerformanceAnalyzer, PerformanceVisualizer


class MatrixMultiplier:

    def __init__(self):
        self.analyzer = PerformanceAnalyzer()

    def _multiply_row(self, args: Tuple[List[float], List[List[float]], int]) -> List[float]:
        row_a, matrix_b, row_idx = args
        result = []
        n = len(matrix_b[0])

        for j in range(n):
            element = sum(row_a[k] * matrix_b[k][j] for k in range(len(row_a)))
            result.append(element)

        return row_idx, result

    def sequential_multiply(self, matrix_a: List[List[float]],
                            matrix_b: List[List[float]]) -> Tuple[List[List[float]], float]:
        start_time = self.analyzer.start_operation("sequential")

        if len(matrix_a[0]) != len(matrix_b):
            raise ValueError("Matrix dimensions don't match for multiplication")

        n, m, p = len(matrix_a), len(matrix_a[0]), len(matrix_b[0])
        result = [[0] * p for _ in range(n)]

        for i in range(n):
            for j in range(p):
                result[i][j] = sum(matrix_a[i][k] * matrix_b[k][j] for k in range(m))
                self.analyzer.record_comparison()

        metrics = self.analyzer.end_operation(
            "sequential",
            start_time,
            n * m * p
        )
        return result, metrics.time_taken

    def parallel_multiply(self, matrix_a: List[List[float]],
                          matrix_b: List[List[float]],
                          num_processes: int) -> Tuple[List[List[float]], float]:
        start_time = self.analyzer.start_operation("parallel")

        if len(matrix_a[0]) != len(matrix_b):
            raise ValueError("Matrix dimensions don't match for multiplication")

        n = len(matrix_a)
        tasks = [(row, matrix_b, i) for i, row in enumerate(matrix_a)]

        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            results = list(executor.map(self._multiply_row, tasks))

        results.sort(key=lambda x: x[0])
        result_matrix = [row for _, row in results]

        metrics = self.analyzer.end_operation(
            "parallel",
            start_time,
            len(matrix_a) * len(matrix_b[0]) * len(matrix_b)
        )
        return result_matrix, metrics.time_taken

    def numpy_multiply(self, matrix_a: List[List[float]],
                       matrix_b: List[List[float]]) -> Tuple[List[List[float]], float]:
        start_time = self.analyzer.start_operation("numpy")

        np_a = np.array(matrix_a)
        np_b = np.array(matrix_b)
        result = np.dot(np_a, np_b)

        metrics = self.analyzer.end_operation(
            "numpy",
            start_time,
            len(matrix_a) * len(matrix_b[0]) * len(matrix_b)
        )
        return result.tolist(), metrics.time_taken

    def visualize_performance(self):
        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='line',
            title='Matrix Multiplication Performance'
        )

        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='bar',
            title='Average Execution Time by Method'
        )

        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='heatmap',
            title='Performance Metrics Heatmap'
        )


def generate_random_matrix(rows: int, cols: int) -> List[List[float]]:
    return [[np.random.rand() for _ in range(cols)] for _ in range(rows)]


def print_matrix(matrix: List[List[float]], name: str = ""):
    print(f"\n{name}:")
    for row in matrix:
        print([f"{x:.2f}" for x in row])


def run_matrix_multiplication_analysis(matrix_size: int = 3, iterations: int = 5):
    multiplier = MatrixMultiplier()
    num_processes = mp.cpu_count()

    print(f"\nRunning analysis with {num_processes} CPU cores")
    print(f"Matrix size: {matrix_size}x{matrix_size}")
    print(f"Number of iterations: {iterations}")

    matrix_a = generate_random_matrix(matrix_size, matrix_size)
    matrix_b = generate_random_matrix(matrix_size, matrix_size)

    print_matrix(matrix_a, "Matrix A")
    print_matrix(matrix_b, "Matrix B")

    methods = {
        "Sequential": lambda: multiplier.sequential_multiply(matrix_a, matrix_b),
        "Parallel": lambda: multiplier.parallel_multiply(matrix_a, matrix_b, num_processes),
        "NumPy": lambda: multiplier.numpy_multiply(matrix_a, matrix_b)
    }

    results = {}
    for method_name, method_func in methods.items():
        print(f"\nTesting {method_name} method:")
        method_times = []
        result_matrix = None

        for i in range(iterations):
            result_matrix, execution_time = method_func()
            method_times.append(execution_time)
            print(f"Iteration {i + 1}: {execution_time:.4f} seconds")

        avg_time = sum(method_times) / len(method_times)
        results[method_name] = {
            "result": result_matrix,
            "avg_time": avg_time,
            "min_time": min(method_times),
            "max_time": max(method_times)
        }
        print(f"Average time: {avg_time:.4f} seconds")
        print_matrix(result_matrix, f"{method_name} Result")

    print("\nGenerating performance visualizations...")
    multiplier.visualize_performance()

    return results


if __name__ == "__main__":
    results_small = run_matrix_multiplication_analysis(matrix_size=3)

    results_large = run_matrix_multiplication_analysis(matrix_size=50)

    print("\nAnalysis complete! Check the generated visualization files.")