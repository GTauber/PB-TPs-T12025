import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple

import numpy as np

from TP03.performance_analyzer.analyzer import PerformanceAnalyzer, PerformanceVisualizer


class ParallelSumAnalyzer:

    def __init__(self):
        self.analyzer = PerformanceAnalyzer()

    def _chunk_data(self, data: List[int], chunks: int) -> List[List[int]]:
        chunk_size = len(data) // chunks
        return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    def sequential_sum(self, data: List[int]) -> Tuple[int, float]:
        start_time = self.analyzer.start_operation("sequential")
        result = sum(data)
        metrics = self.analyzer.end_operation(
            "sequential",
            start_time,
            len(data)
        )
        return result, metrics.time_taken

    def process_pool_sum(self, data: List[int], num_processes: int) -> Tuple[int, float]:
        start_time = self.analyzer.start_operation("process_pool")
        chunks = self._chunk_data(data, num_processes)

        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            partial_sums = list(executor.map(sum, chunks))

        total_sum = sum(partial_sums)
        metrics = self.analyzer.end_operation(
            "process_pool",
            start_time,
            len(data)
        )
        return total_sum, metrics.time_taken

    def multiprocessing_sum(self, data: List[int], num_processes: int) -> Tuple[int, float]:
        start_time = self.analyzer.start_operation("multiprocessing")
        chunks = self._chunk_data(data, num_processes)

        with mp.Pool(processes=num_processes) as pool:
            partial_sums = pool.map(sum, chunks)

        total_sum = sum(partial_sums)
        metrics = self.analyzer.end_operation(
            "multiprocessing",
            start_time,
            len(data)
        )
        return total_sum, metrics.time_taken

    def numpy_sum(self, data: List[int]) -> Tuple[int, float]:
        start_time = self.analyzer.start_operation("numpy")
        np_array = np.array(data)
        result = np_array.sum()
        metrics = self.analyzer.end_operation(
            "numpy",
            start_time,
            len(data)
        )
        return result, metrics.time_taken

    def visualize_performance(self):
        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='line',
            title='Parallel Sum Performance Comparison'
        )

        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='bar',
            title='Average Performance by Method'
        )

        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='candlestick',
            title='Performance Distribution Analysis'
        )


def run_parallel_sum_analysis(max_num: int = 10_000_000, iterations: int = 5):
    analyzer = ParallelSumAnalyzer()
    num_processes = mp.cpu_count()
    data = list(range(1, max_num + 1))

    print(f"\nRunning analysis with {num_processes} CPU cores")
    print(f"Data size: {max_num:,} numbers")
    print(f"Number of iterations: {iterations}")

    methods = {
        "Sequential": lambda: analyzer.sequential_sum(data),
        "ProcessPool": lambda: analyzer.process_pool_sum(data, num_processes),
        "Multiprocessing": lambda: analyzer.multiprocessing_sum(data, num_processes),
        "NumPy": lambda: analyzer.numpy_sum(data)
    }

    results = {}
    for method_name, method_func in methods.items():
        print(f"\nTesting {method_name} method:")
        method_times = []

        for i in range(iterations):
            result, execution_time = method_func()
            method_times.append(execution_time)
            print(f"Iteration {i + 1}: {execution_time:.4f} seconds")

        avg_time = sum(method_times) / len(method_times)
        results[method_name] = {
            "result": result,
            "avg_time": avg_time,
            "min_time": min(method_times),
            "max_time": max(method_times)
        }
        print(f"Average time: {avg_time:.4f} seconds")

    print("\nGenerating performance visualizations...")
    analyzer.visualize_performance()

    return results


if __name__ == "__main__":
    results = run_parallel_sum_analysis()
    print("\nAnalysis complete! Check the generated visualization files.")