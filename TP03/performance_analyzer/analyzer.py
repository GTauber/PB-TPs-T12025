from dataclasses import dataclass
from typing import Any, Dict, Tuple

import time
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any
import numpy as np
from .metrics import PerformanceMetrics


class PerformanceAnalyzer:

    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self._comparison_count = 0

    def start_operation(self, operation_name: str) -> float:
        self._comparison_count = 0
        return time.time()

    def record_comparison(self):
        self._comparison_count += 1

    def end_operation(self, operation_name: str, start_time: float,
                      elements_processed: int, additional_metrics: Dict[str, Any] = None) -> PerformanceMetrics:
        metrics = PerformanceMetrics(
            operation=operation_name,
            time_taken=time.time() - start_time,
            elements_processed=elements_processed,
            comparisons=self._comparison_count,
            additional_metrics=additional_metrics
        )
        self.metrics_history.append(metrics)
        return metrics


class PerformanceVisualizer:

    @staticmethod
    def create_comparison_plot(metrics_list: List[PerformanceMetrics],
                               plot_type: str = 'line',
                               title: str = 'Performance Analysis',
                               figsize: Tuple[float, float] = (15.0, 8.0)):
        plt.figure(figsize=figsize)

        operations = {}
        for metric in metrics_list:
            if metric.operation not in operations:
                operations[metric.operation] = {
                    'times': [],
                    'comparisons': [],
                    'elements': []
                }
            operations[metric.operation]['times'].append(metric.time_taken * 1000)  # ms
            operations[metric.operation]['comparisons'].append(metric.comparisons)
            operations[metric.operation]['elements'].append(metric.elements_processed)

        if plot_type == 'line':
            PerformanceVisualizer._create_line_plot(operations, title)
        elif plot_type == 'bar':
            PerformanceVisualizer._create_bar_plot(operations, title)
        elif plot_type == 'candlestick':
            PerformanceVisualizer._create_candlestick_plot(operations, title)
        elif plot_type == 'heatmap':
            PerformanceVisualizer._create_heatmap_plot(operations, title)

        plt.tight_layout()
        plt.savefig(f'performance_{plot_type}_{title.lower().replace(" ", "_")}.png')
        plt.close()

    @staticmethod
    def _create_line_plot(operations: Dict, title: str):
        plt.subplot(2, 1, 1)
        for op_name, op_data in operations.items():
            plt.plot(op_data['times'], label=f'{op_name} (time)')
        plt.ylabel('Time (ms)')
        plt.title(f'{title} - Execution time')
        plt.legend()

        plt.subplot(2, 1, 2)
        for op_name, op_data in operations.items():
            plt.plot(op_data['comparisons'], label=f'{op_name} (comparisons)')
        plt.ylabel('Number of comparisons')
        plt.xlabel('Operation Index')
        plt.legend()

    @staticmethod
    def _create_bar_plot(operations: Dict, title: str):
        avg_times = []
        avg_comparisons = []
        labels = []

        for op_name, op_data in operations.items():
            avg_times.append(np.mean(op_data['times']))
            avg_comparisons.append(np.mean(op_data['comparisons']))
            labels.append(op_name)

        x = np.arange(len(labels))
        width = 0.35

        plt.subplot(2, 1, 1)
        plt.bar(x - width / 2, avg_times, width, label='Average time (ms)')
        plt.xticks(x, labels)
        plt.ylabel('Time (ms)')
        plt.title(f'{title} - Performance Average')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.bar(x + width / 2, avg_comparisons, width, label='Average comparisons')
        plt.xticks(x, labels)
        plt.ylabel('Number of comparisons')
        plt.legend()

    @staticmethod
    def _create_candlestick_plot(operations: Dict, title: str):
        plt.subplot(2, 1, 1)
        data_times = [op_data['times'] for op_data in operations.values()]
        plt.boxplot(data_times, labels=operations.keys())
        plt.ylabel('Time (ms)')
        plt.title(f'{title} - Performance distribution')

        plt.subplot(2, 1, 2)
        data_comps = [op_data['comparisons'] for op_data in operations.values()]
        plt.boxplot(data_comps, labels=operations.keys())
        plt.ylabel('Comparisons number')

    @staticmethod
    def _create_heatmap_plot(operations: Dict, title: str):
        metrics_matrix = []
        for op_name, op_data in operations.items():
            metrics_matrix.append([
                np.mean(op_data['times']),
                np.mean(op_data['comparisons']),
                np.mean(op_data['elements'])
            ])

        plt.title(f'{title} - Performance heatmap')
        sns.heatmap(metrics_matrix,
                    xticklabels=['Time', 'Comparisons', 'Elements'],
                    yticklabels=list(operations.keys()),
                    annot=True,
                    fmt='.2f',
                    cmap='YlOrRd')