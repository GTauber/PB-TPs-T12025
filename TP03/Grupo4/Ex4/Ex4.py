import ipaddress
import random
import time
from typing import List, Optional, Dict

import matplotlib.pyplot as plt
from TP03.performance_analyzer.analyzer import PerformanceAnalyzer
from TP03.performance_analyzer.decorators import measure_performance


class IPv4TrieNode:
    def __init__(self):
        self.children = {0: None, 1: None}
        self.prefix = None
        self.network = None
        self.mask_length = None


class IPv4Trie:
    def __init__(self):
        self.root = IPv4TrieNode()
        self.analyzer = PerformanceAnalyzer()

    def _ip_to_binary(self, ip: str) -> str:
        ip_obj = ipaddress.IPv4Address(ip)
        return format(int(ip_obj), '032b')

    @measure_performance("insert")
    def insert(self, prefix: str) -> None:
        try:
            network = ipaddress.IPv4Network(prefix, strict=False)
            binary_ip = format(int(network.network_address), '032b')
            mask_length = network.prefixlen

            current = self.root
            for i in range(mask_length):
                self.analyzer.record_comparison()
                bit = int(binary_ip[i])
                if current.children[bit] is None:
                    current.children[bit] = IPv4TrieNode()
                current = current.children[bit]

            current.prefix = prefix
            current.network = network
            current.mask_length = mask_length
        except ValueError:
            return

    @measure_performance("search")
    def search(self, ip: str) -> Optional[str]:
        try:
            ip_obj = ipaddress.IPv4Address(ip)
            binary_ip = self._ip_to_binary(str(ip_obj))

            current = self.root
            best_match = None

            for i in range(len(binary_ip)):
                self.analyzer.record_comparison()
                if current.prefix is not None:
                    best_match = current.prefix

                bit = int(binary_ip[i])
                if current.children[bit] is None:
                    break
                current = current.children[bit]

            if current.prefix is not None:
                best_match = current.prefix

            return best_match
        except ValueError:
            return None


class PrefixSearchComparator:
    def __init__(self):
        self.analyzer = PerformanceAnalyzer()
        self.trie = IPv4Trie()
        self.prefix_list: List[str] = []

    def generate_random_prefix(self) -> str:
        octet1 = random.randint(1, 223)
        octet2 = random.randint(0, 255)
        octet3 = random.randint(0, 255)
        octet4 = random.randint(0, 255)
        mask = random.randint(8, 24)
        return f"{octet1}.{octet2}.{octet3}.{octet4}/{mask}"

    def generate_test_data(self, num_prefixes: int) -> List[str]:
        prefixes = set()
        while len(prefixes) < num_prefixes:
            prefix = self.generate_random_prefix()
            try:
                ipaddress.IPv4Network(prefix, strict=False)
                prefixes.add(prefix)
            except ValueError:
                continue

        self.prefix_list = list(prefixes)
        for prefix in self.prefix_list:
            self.trie.insert(prefix)
        return self.prefix_list

    @measure_performance("linear_search")
    def linear_search(self, ip: str) -> Optional[str]:
        try:
            ip_obj = ipaddress.IPv4Address(ip)
            best_match = None
            best_prefix_len = -1

            for prefix in self.prefix_list:
                self.analyzer.record_comparison()
                network = ipaddress.IPv4Network(prefix, strict=False)
                if ip_obj in network:
                    prefix_len = network.prefixlen
                    if prefix_len > best_prefix_len:
                        best_match = prefix
                        best_prefix_len = prefix_len
            return best_match
        except ValueError:
            return None

    @measure_performance("trie_search")
    def trie_search(self, ip: str) -> Optional[str]:
        return self.trie.search(ip)

    def run_performance_comparison(self, num_prefixes: int, num_tests: int) -> Dict:
        print(f"\nGenerating {num_prefixes} random prefixes...")
        prefixes = self.generate_test_data(num_prefixes)

        test_ips = []
        for prefix in random.sample(prefixes, min(num_tests, len(prefixes))):
            network = ipaddress.IPv4Network(prefix, strict=False)
            host_bits = random.getrandbits(32 - network.prefixlen)
            ip = network.network_address + host_bits
            test_ips.append(str(ip))

        print(f"\nRunning {num_tests} test searches...")
        results = {
            'linear': {'times': [], 'comparisons': []},
            'trie': {'times': [], 'comparisons': []}
        }

        for i, ip in enumerate(test_ips, 1):
            print(f"\nTest {i}: Searching for IP {ip}")

            start_time = time.time()
            self.linear_search(ip)
            linear_time = time.time() - start_time
            results['linear']['times'].append(linear_time)

            start_time = time.time()
            self.trie_search(ip)
            trie_time = time.time() - start_time
            results['trie']['times'].append(trie_time)

            linear_metrics = [m for m in self.analyzer.metrics_history if m.operation == "linear_search"][-1]
            trie_metrics = [m for m in self.analyzer.metrics_history if m.operation == "trie_search"][-1]
            results['linear']['comparisons'].append(linear_metrics.comparisons)
            results['trie']['comparisons'].append(trie_metrics.comparisons)

        return results

    def visualize_results(self, results: dict) -> None:
        plt.figure(figsize=(15, 10))

        plt.subplot(2, 2, 1)
        plt.plot(results['linear']['times'], label='Linear', color='blue')
        plt.plot(results['trie']['times'], label='Trie', color='red')
        plt.title('Search Time Comparison')
        plt.xlabel('Test Case')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 2, 2)
        plt.plot(results['linear']['comparisons'], label='Linear', color='blue')
        plt.plot(results['trie']['comparisons'], label='Trie', color='red')
        plt.title('Number of Comparisons')
        plt.xlabel('Test Case')
        plt.ylabel('Comparisons')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 2, 3)
        ratios = [l / t if t > 0 else 1 for l, t in zip(results['linear']['times'], results['trie']['times'])]
        plt.plot(ratios, color='green')
        plt.axhline(y=1, color='r', linestyle='--', alpha=0.5)
        plt.title('Performance Ratio (Linear/Trie)')
        plt.xlabel('Test Case')
        plt.ylabel('Ratio')
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 2, 4)
        plt.boxplot([results['linear']['times'], results['trie']['times']],
                    labels=['Linear', 'Trie'])
        plt.title('Distribution of Search Times')
        plt.ylabel('Time (seconds)')
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('search_performance_comparison.png')
        plt.close()


def run_comparison_test():
    comparator = PrefixSearchComparator()
    test_sizes = [100, 1000, 10000]
    all_results = {}

    for size in test_sizes:
        print(f"\n=== Testing with {size} prefixes ===")
        results = comparator.run_performance_comparison(
            num_prefixes=size,
            num_tests=min(100, size)
        )

        all_results[size] = results
        comparator.visualize_results(results)

        linear_avg = sum(results['linear']['times']) / len(results['linear']['times'])
        trie_avg = sum(results['trie']['times']) / len(results['trie']['times'])
        linear_comps = sum(results['linear']['comparisons']) / len(results['linear']['comparisons'])
        trie_comps = sum(results['trie']['comparisons']) / len(results['trie']['comparisons'])

        print(f"\nResults for {size} prefixes:")
        print(f"Average Linear Search Time: {linear_avg:.6f} seconds")
        print(f"Average Trie Search Time: {trie_avg:.6f} seconds")
        print(f"Average Linear Comparisons: {linear_comps:.2f}")
        print(f"Average Trie Comparisons: {trie_comps:.2f}")
        print(f"Speed Improvement: {linear_avg / trie_avg:.2f}x")

    return all_results


if __name__ == "__main__":
    results = run_comparison_test()
    print("\nAnalysis complete! Check the generated visualization files.")