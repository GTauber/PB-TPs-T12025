import math
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

    def count_primes(self, start: int, end: int) -> Tuple[int, List[int], float]:
        start_time = self.analyzer.start_operation("count_primes")

        sieve = [True] * (end + 1)
        sieve[0] = sieve[1] = False

        for i in range(2, int(math.sqrt(end)) + 1):
            self.analyzer.record_comparison()
            if sieve[i]:
                for j in range(i * i, end + 1, i):
                    sieve[j] = False

        primes = [num for num in range(max(2, start), end + 1) if sieve[num]]

        metrics = self.analyzer.end_operation(
            "count_primes",
            start_time,
            end - start + 1
        )
        return len(primes), primes, metrics.time_taken

    def visualize_performance(self):
        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='line',
            title='Prime Counting Performance'
        )

        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='bar',
            title='Prime Counting Operations'
        )


def run_prime_analysis(end: int = 100_000):
    counter = PrimeCounter()
    start = 1

    print(f"\nCounting primes from {start:,} to {end:,}")
    count, primes, execution_time = counter.count_primes(start, end)

    print(f"\nResults:")
    print(f"Found {count:,} prime numbers")
    print(f"Execution time: {execution_time:.4f} seconds")

    if len(primes) > 10:
        print("\nSample of primes found:")
        print("First 5:", primes[:5])
        print("Last 5:", primes[-5:])
    else:
        print("\nAll primes found:", primes)

    print("\nGenerating performance visualizations...")
    counter.visualize_performance()

    return count, primes, execution_time


if __name__ == "__main__":
    run_prime_analysis()