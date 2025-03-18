import matplotlib.pyplot as plt
import numpy as np
import time
from typing import List, Tuple, Callable, Dict, Any


class HeapAnalyzer:
    @staticmethod
    def measure_execution_time(func: Callable, *args, **kwargs) -> Tuple[float, Any]:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return end_time - start_time, result

    @staticmethod
    def analyze_operation(operation_func: Callable,
                          sizes: List[int],
                          setup_func: Callable = None,
                          trials: int = 5) -> Tuple[List[int], List[float]]:
        times = []

        for size in sizes:
            total_time = 0
            for _ in range(trials):
                if setup_func:
                    env = setup_func(size)
                else:
                    env = {}

                execution_time, _ = HeapAnalyzer.measure_execution_time(
                    operation_func, **env
                )
                total_time += execution_time

            avg_time = total_time / trials
            times.append(avg_time)
            print(f"Size {size}: {avg_time:.6f} seconds")

        return sizes, times

    @staticmethod
    def plot_time_complexity(sizes: List[int],
                             times: List[float],
                             operation: str = "Heap Operation",
                             expected_complexity: str = "O(n)",
                             filename: str = "heap_operation_time.png") -> None:

        plt.figure(figsize=(10, 6))
        plt.plot(sizes, times, 'o-', label='Measured time')

        if expected_complexity == "O(n)":
            coeffs = np.polyfit(sizes, times, 1)
            theoretical_times = [coeffs[0] * size + coeffs[1] for size in sizes]
            plt.plot(sizes, theoretical_times, '--', label='O(n) reference')
        elif expected_complexity == "O(log n)":
            coeffs = np.polyfit(np.log(sizes), times, 1)
            theoretical_times = [coeffs[0] * np.log(size) + coeffs[1] for size in sizes]
            plt.plot(sizes, theoretical_times, '--', label='O(log n) reference')
        elif expected_complexity == "O(n log n)":
            coeffs = np.polyfit(np.array(sizes) * np.log(sizes), times, 1)
            theoretical_times = [coeffs[0] * (size * np.log(size)) + coeffs[1] for size in sizes]
            plt.plot(sizes, theoretical_times, '--', label='O(n log n) reference')

        plt.title(f'Time Complexity of {operation}')
        plt.xlabel('Input Size (n)')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True)

        plt.savefig(filename)
        plt.close()
        print(f"Plot saved as: {filename}")

    @staticmethod
    def visualize_multiple_operations(operations_data: Dict[str, Tuple[List[int], List[float], str]],
                                      title: str = "Heap Operations Comparison",
                                      filename: str = "heap_operations_comparison.png") -> None:
        plt.figure(figsize=(12, 7))

        for operation, (sizes, times, _) in operations_data.items():
            plt.plot(sizes, times, 'o-', label=f'{operation}')

        plt.title(title)
        plt.xlabel('Input Size (n)')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True)

        plt.savefig(filename)
        plt.close()
        print(f"Comparison plot saved as: {filename}")