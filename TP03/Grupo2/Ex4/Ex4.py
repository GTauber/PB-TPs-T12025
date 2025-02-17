import math
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple

from TP03.performance_analyzer.analyzer import PerformanceAnalyzer, PerformanceVisualizer


class PrimeCounter:

    def __init__(self):
        self.analyzer = PerformanceAnalyzer()

    def is_prime(self, n: int) -> bool:
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        for i in range(3, int(math.sqrt(n)) + 1, 2):
            self.analyzer.record_comparison()
            if n % i == 0:
                return False
        return True

    def sequential_count(self, start: int, end: int) -> Tuple[int, List[int], float]:
        start_time = self.analyzer.start_operation("sequential")
        primes = []

        for num in range(start, end + 1):
            if self.is_prime(num):
                primes.append(num)

        metrics = self.analyzer.end_operation(
            "sequential",
            start_time,
            end - start + 1
        )
        return len(primes), primes, metrics.time_taken

    def _process_range(self, range_tuple: Tuple[int, int]) -> List[int]:
        start, end = range_tuple
        return [num for num in range(start, end + 1) if self.is_prime(num)]

    def parallel_count(self, start: int, end: int, num_processes: int) -> Tuple[int, List[int], float]:
        start_time = self.analyzer.start_operation("parallel")

        chunk_size = (end - start + 1) // num_processes
        ranges = [(i, min(i + chunk_size - 1, end))
                  for i in range(start, end + 1, chunk_size)]

        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            results = list(executor.map(self._process_range, ranges))

        all_primes = [prime for chunk in results for prime in chunk]

        metrics = self.analyzer.end_operation(
            "parallel",
            start_time,
            end - start + 1
        )
        return len(all_primes), sorted(all_primes), metrics.time_taken

    def visualize_comparison(self):
        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='line',
            title='Sequential vs Parallel Performance'
        )

        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='bar',
            title='Average Execution Time Comparison'
        )

        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='candlestick',
            title='Performance Distribution Analysis'
        )


def run_performance_comparison(end: int = 100_000, iterations: int = 3):
    counter = PrimeCounter()
    num_processes = mp.cpu_count()
    start = 1

    print(f"\nComparing sequential vs parallel prime counting")
    print(f"Range: {start:,} to {end:,}")
    print(f"Number of CPU cores available: {num_processes}")
    print(f"Number of iterations: {iterations}")

    results = {
        "Sequential": [],
        "Parallel": []
    }

    for i in range(iterations):
        print(f"\nIteration {i + 1}:")

        seq_count, seq_primes, seq_time = counter.sequential_count(start, end)
        results["Sequential"].append({
            "count": seq_count,
            "time": seq_time
        })
        print(f"Sequential: {seq_time:.4f} seconds")

        par_count, par_primes, par_time = counter.parallel_count(start, end, num_processes)
        results["Parallel"].append({
            "count": par_count,
            "time": par_time
        })
        print(f"Parallel: {par_time:.4f} seconds")

        assert seq_count == par_count, "Error: Methods found different number of primes"
        assert seq_primes == par_primes, "Error: Methods found different prime numbers"

    print("\nPerformance Statistics:")
    for method in results:
        times = [r["time"] for r in results[method]]
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"\n{method} Method:")
        print(f"Average time: {avg_time:.4f} seconds")
        print(f"Best time: {min_time:.4f} seconds")
        print(f"Worst time: {max_time:.4f} seconds")

    print("\nGenerating performance visualizations...")
    counter.visualize_comparison()

    return results


if __name__ == "__main__":
    results = run_performance_comparison()

    results_large = run_performance_comparison(end=500_000, iterations=2)

    print("\nAnalysis complete! Check the generated visualization files.")