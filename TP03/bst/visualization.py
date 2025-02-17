from typing import List
import matplotlib.pyplot as plt
from TP03.performance_analyzer.analyzer import PerformanceVisualizer


class BSTVisualizer:

    @staticmethod
    def visualize_search_performance(bst, search_values: List[int]):
        PerformanceVisualizer.create_comparison_plot(
            bst.analyzer.metrics_history,
            plot_type='line',
            title='bst Search Performance Analysis'
        )

        plt.figure(figsize=(15, 6))

        plt.subplot(1, 2, 1)
        metrics = [m for m in bst.analyzer.metrics_history if m.operation == "search"]
        path_lengths = [m.comparisons for m in metrics]
        plt.bar(range(len(search_values)), path_lengths)
        plt.xlabel('Search Operation Index')
        plt.ylabel('Path Length (Comparisons)')
        plt.title('Search Path Lengths')

        for i, v in enumerate(search_values):
            plt.text(i, path_lengths[i], f'Value: {v}', ha='center', va='bottom')

        plt.subplot(1, 2, 2)
        search_times = [m.time_taken * 1000 for m in metrics]
        plt.bar(range(len(search_values)), search_times)
        plt.xlabel('Search Operation Index')
        plt.ylabel('Time (ms)')
        plt.title('Search Operation Times')

        plt.tight_layout()
        plt.savefig(f'bst_search_performance_{bst.analyzer.metrics_history[-1].time_taken}.png')

    @staticmethod
    def visualize_deletion_performance(bst):
        PerformanceVisualizer.create_comparison_plot(
            bst.analyzer.metrics_history,
            plot_type='line',
            title='bst Deletion Performance'
        )

        if hasattr(bst, 'tree_states') and bst.tree_states:
            plt.figure(figsize=(12, 6))
            for state in bst.tree_states:
                plt.plot(range(len(state['inorder'])),
                         state['inorder'],
                         label=f"After {state['operation']}")

            plt.title('Tree Structure Evolution')
            plt.xlabel('Node Index')
            plt.ylabel('Node Value')
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.savefig(f'bst_tree_evolution {bst.analyzer.metrics_history[-1].time_taken}.png')

    @staticmethod
    def create_validation_performance_plots(bst):
        PerformanceVisualizer.create_comparison_plot(
            bst.analyzer.metrics_history,
            plot_type='line',
            title='BST Validation Performance'
        )

        PerformanceVisualizer.create_comparison_plot(
            bst.analyzer.metrics_history,
            plot_type='bar',
            title='BST Operation Comparison'
        )

        plt.figure(figsize=(12, 6))
        validation_metrics = [m for m in bst.analyzer.metrics_history if m.operation == "validate"]

        plt.subplot(1, 2, 1)
        times = [m.time_taken * 1000 for m in validation_metrics]  # Convert to ms
        plt.plot(times, marker='o')
        plt.title('Validation Time Trend')
        plt.xlabel('Validation Operation')
        plt.ylabel('Time (ms)')

        plt.subplot(1, 2, 2)
        comparisons = [m.comparisons for m in validation_metrics]
        plt.plot(comparisons, marker='s', color='green')
        plt.title('Validation Comparisons')
        plt.xlabel('Validation Operation')
        plt.ylabel('Number of Comparisons')

        plt.tight_layout()
        plt.savefig('bst_validation_metrics.png')
        plt.close()

    @staticmethod
    def visualize_parallel_search_comparison(bst):
        plt.figure(figsize=(15, 10))

        seq_metrics = [m for m in bst.analyzer.metrics_history if m.operation == "search"]
        par_metrics = [m for m in bst.analyzer.metrics_history if m.operation == "parallel_search"]

        plt.subplot(2, 2, 1)
        seq_times = [m.time_taken * 1000 for m in seq_metrics]
        par_times = [m.time_taken * 1000 for m in par_metrics]
        plt.plot(seq_times, label='Sequential', marker='o')
        plt.plot(par_times, label='Parallel', marker='s')
        plt.title('Search Time Comparison')
        plt.xlabel('Search Operation')
        plt.ylabel('Time (ms)')
        plt.legend()

        plt.subplot(2, 2, 2)
        seq_comps = [m.comparisons for m in seq_metrics]
        par_comps = [m.comparisons for m in par_metrics]
        plt.plot(seq_comps, label='Sequential', marker='o')
        plt.plot(par_comps, label='Parallel', marker='s')
        plt.title('Number of Comparisons')
        plt.xlabel('Search Operation')
        plt.ylabel('Comparisons')
        plt.legend()

        plt.subplot(2, 2, 3)
        labels = ['Time (ms)', 'Comparisons']
        seq_avgs = [
            sum(seq_times) / len(seq_times),
            sum(seq_comps) / len(seq_comps)
        ]
        par_avgs = [
            sum(par_times) / len(par_times),
            sum(par_comps) / len(par_comps)
        ]

        x = range(len(labels))
        width = 0.35
        plt.bar([i - width / 2 for i in x], seq_avgs, width, label='Sequential')
        plt.bar([i + width / 2 for i in x], par_avgs, width, label='Parallel')
        plt.xticks(x, labels)
        plt.title('Average Performance Metrics')
        plt.legend()

        plt.subplot(2, 2, 4)
        speedup = [s / p for s, p in zip(seq_times, par_times)]
        plt.plot(speedup, marker='o', color='green')
        plt.axhline(y=1, color='r', linestyle='--', alpha=0.5)
        plt.title('Speedup Ratio (Sequential/Parallel)')
        plt.xlabel('Search Operation')
        plt.ylabel('Speedup Factor')

        plt.tight_layout()
        plt.savefig('parallel_search_comparison.png')
        plt.close()

    @staticmethod
    def visualize_dfs_performance(bst, test_values: List[int]):
        plt.figure(figsize=(15, 10))

        seq_metrics = [m for m in bst.analyzer.metrics_history if m.operation == "sequential_dfs"]
        par_metrics = [m for m in bst.analyzer.metrics_history if m.operation == "parallel_dfs"]

        plt.subplot(2, 2, 1)
        seq_times = [m.time_taken * 1000 for m in seq_metrics]
        par_times = [m.time_taken * 1000 for m in par_metrics]

        plt.plot(seq_times, 'b-o', label='Sequential')
        plt.plot(par_times, 'r-o', label='Parallel')
        plt.title('DFS Execution Time Comparison')
        plt.xlabel('Search Operation')
        plt.ylabel('Time (ms)')
        plt.legend()

        for i, value in enumerate(test_values):
            plt.annotate(f'Target: {value}',
                         (i, max(seq_times[i], par_times[i])),
                         xytext=(0, 10),
                         textcoords='offset points',
                         ha='center')

        plt.subplot(2, 2, 2)
        seq_comps = [m.comparisons for m in seq_metrics]
        par_comps = [m.comparisons for m in par_metrics]

        x = range(len(test_values))
        width = 0.35
        plt.bar([i - width / 2 for i in x], seq_comps, width, label='Sequential', color='blue', alpha=0.6)
        plt.bar([i + width / 2 for i in x], par_comps, width, label='Parallel', color='red', alpha=0.6)
        plt.title('Number of Comparisons per Search')
        plt.xlabel('Target Value')
        plt.ylabel('Comparisons')
        plt.xticks(x, test_values)
        plt.legend()

        plt.subplot(2, 2, 3)
        speedup = [s / p if p > 0 else 1 for s, p in zip(seq_times, par_times)]
        plt.plot(speedup, 'g-o')
        plt.axhline(y=1, color='r', linestyle='--', alpha=0.5)
        plt.title('Speedup Ratio (Sequential/Parallel)')
        plt.xlabel('Search Operation')
        plt.ylabel('Speedup Factor')

        plt.subplot(2, 2, 4)
        seq_lengths = [m.elements_processed for m in seq_metrics]
        par_lengths = [m.elements_processed for m in par_metrics]

        plt.scatter(seq_lengths, par_lengths)
        max_len = max(max(seq_lengths), max(par_lengths))
        plt.plot([0, max_len], [0, max_len], 'r--', alpha=0.5)
        plt.title('Path Length Comparison')
        plt.xlabel('Sequential Path Length')
        plt.ylabel('Parallel Path Length')

        plt.tight_layout()
        plt.savefig('dfs_performance_comparison.png')
        plt.close()

    @staticmethod
    def visualize_max_finder_performance(bst):
        plt.figure(figsize=(15, 10))

        seq_metrics = [m for m in bst.analyzer.metrics_history if m.operation == "sequential_max"]
        par_metrics = [m for m in bst.analyzer.metrics_history if m.operation == "parallel_max"]

        plt.subplot(2, 2, 1)
        seq_times = [m.time_taken * 1000 for m in seq_metrics]
        par_times = [m.time_taken * 1000 for m in par_metrics]

        plt.plot(seq_times, 'b-o', label='Sequential')
        plt.plot(par_times, 'r-o', label='Parallel')
        plt.title('Maximum Finding Execution Time')
        plt.xlabel('Test Case')
        plt.ylabel('Time (ms)')
        plt.legend()

        plt.subplot(2, 2, 2)
        seq_comps = [m.comparisons for m in seq_metrics]
        par_comps = [m.comparisons for m in par_metrics]

        x = range(len(seq_metrics))
        width = 0.35
        plt.bar([i - width / 2 for i in x], seq_comps, width, label='Sequential', color='blue', alpha=0.6)
        plt.bar([i + width / 2 for i in x], par_comps, width, label='Parallel', color='red', alpha=0.6)
        plt.title('Number of Comparisons')
        plt.xlabel('Test Case')
        plt.ylabel('Comparisons')
        plt.legend()

        plt.subplot(2, 2, 3)
        speedup = [s / p if p > 0 else 1 for s, p in zip(seq_times, par_times)]
        plt.plot(speedup, 'g-o')
        plt.axhline(y=1, color='r', linestyle='--', alpha=0.5)
        plt.title('Speedup Ratio (Sequential/Parallel)')
        plt.xlabel('Test Case')
        plt.ylabel('Speedup Factor')

        plt.subplot(2, 2, 4)
        seq_nodes = [m.elements_processed for m in seq_metrics]
        par_nodes = [m.elements_processed for m in par_metrics]

        plt.scatter(seq_nodes, par_nodes)
        max_nodes = max(max(seq_nodes), max(par_nodes))
        plt.plot([0, max_nodes], [0, max_nodes], 'r--', alpha=0.5)
        plt.title('Nodes Visited Comparison')
        plt.xlabel('Sequential Nodes')
        plt.ylabel('Parallel Nodes')

        plt.tight_layout()
        plt.savefig('max_finder_performance.png')
        plt.close()