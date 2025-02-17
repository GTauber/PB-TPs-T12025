import ipaddress
from typing import Optional, List, Dict, Tuple

from matplotlib import pyplot as plt

from TP03.performance_analyzer.analyzer import PerformanceAnalyzer, PerformanceVisualizer
from TP03.performance_analyzer.decorators import measure_performance


class IPv4TrieNode:

    def __init__(self):
        self.children: Dict[int, 'IPv4TrieNode'] = {}
        self.is_end: bool = False
        self.prefix: Optional[str] = None
        self.mask_length: Optional[int] = None
        self.prefix_bits: Optional[str] = None


class IPv4Trie:
    def __init__(self):
        self.root = IPv4TrieNode()
        self.analyzer = PerformanceAnalyzer()
        self.search_paths: List[Dict] = []

    def _ip_to_binary(self, ip: str) -> str:
        ip_int = int(ipaddress.IPv4Address(ip))
        return format(ip_int, '032b')

    def _get_network_and_mask(self, prefix: str) -> Tuple[str, int, str]:
        network = ipaddress.IPv4Network(prefix, strict=False)
        network_addr = str(network.network_address)
        mask_length = network.prefixlen
        binary_ip = self._ip_to_binary(network_addr)
        return network_addr, mask_length, binary_ip

    @measure_performance("insert")
    def insert(self, prefix: str) -> None:
        try:
            network_addr, mask_length, binary_ip = self._get_network_and_mask(prefix)
        except ValueError as e:
            print(f"Invalid prefix {prefix}: {e}")
            return

        current = self.root
        prefix_bits = ""

        for i in range(mask_length):
            self.analyzer.record_comparison()
            bit = int(binary_ip[i])
            prefix_bits += str(bit)

            if bit not in current.children:
                current.children[bit] = IPv4TrieNode()
            current = current.children[bit]

        current.is_end = True
        current.prefix = prefix
        current.mask_length = mask_length
        current.prefix_bits = prefix_bits

        self.analyzer.end_operation(
            "insert",
            time.time(),
            mask_length,
            {"prefix": prefix, "mask_length": mask_length}
        )

    @measure_performance("longest_prefix_match")
    def longest_prefix_match(self, ip: str) -> Tuple[Optional[str], List[Dict]]:
        try:
            binary_ip = self._ip_to_binary(ip)
        except ValueError as e:
            print(f"Invalid IP {ip}: {e}")
            return None, []

        current = self.root
        matched_prefix = None
        search_path = []
        current_bits = ""

        for i in range(32):
            self.analyzer.record_comparison()

            path_entry = {
                'level': i,
                'bits_seen': current_bits,
                'current_match': matched_prefix,
                'is_prefix': current.is_end
            }
            search_path.append(path_entry)

            if current.is_end:
                matched_prefix = current.prefix

            bit = int(binary_ip[i])
            current_bits += str(bit)

            if bit not in current.children:
                break
            current = current.children[bit]

        if current.is_end:
            matched_prefix = current.prefix
            search_path.append({
                'level': len(binary_ip),
                'bits_seen': current_bits,
                'current_match': matched_prefix,
                'is_prefix': True
            })

        return matched_prefix, search_path

    def visualize_performance(self) -> None:
        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='line',
            title='IPv4 Trie Operations Performance'
        )

        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='bar',
            title='IPv4 Trie Operation Distribution'
        )

        self._visualize_prefix_distribution()

    def _visualize_prefix_distribution(self) -> None:
        prefix_lengths = [m.additional_metrics.get('mask_length', 0)
                          for m in self.analyzer.metrics_history
                          if m.operation == 'insert']

        plt.figure(figsize=(10, 6))
        plt.hist(prefix_lengths, bins=32, range=(0, 32), alpha=0.7)
        plt.title('Distribution of Prefix Lengths')
        plt.xlabel('Prefix Length')
        plt.ylabel('Count')
        plt.grid(True, alpha=0.3)
        plt.savefig('prefix_length_distribution.png')
        plt.close()


def test_ipv4_longest_prefix_match():
    trie = IPv4Trie()

    prefixes = [
        "192.168.0.0/16",
        "192.168.1.0/24",
        "10.0.0.0/8",
        "192.168.1.128/25",
        "0.0.0.0/0"
    ]

    print("\nInserting prefixes:")
    for prefix in prefixes:
        print(f"Adding prefix: {prefix}")
        trie.insert(prefix)

    test_ips = [
        "192.168.1.100",
        "192.168.1.200",
        "192.168.2.1",
        "10.10.10.10",
        "8.8.8.8",
        "192.168.1.129"
    ]

    results = []
    print("\nTesting longest prefix matches:")
    for ip in test_ips:
        print(f"\nLooking up IP: {ip}")
        matched_prefix, search_path = trie.longest_prefix_match(ip)

        print(f"Matched prefix: {matched_prefix}")
        print("Search path:")
        for step in search_path:
            prefix_str = step['current_match'] if step['is_prefix'] else 'No prefix'
            print(f"Level {step['level']}: {step['bits_seen']} -> {prefix_str}")

        results.append({
            'ip': ip,
            'matched_prefix': matched_prefix,
            'path_length': len(search_path)
        })

    print("\nTesting error cases:")
    error_cases = [
        "256.256.256.256",
        "invalid_ip",
        "192.168.1"
    ]

    for invalid_ip in error_cases:
        print(f"\nTesting invalid IP: {invalid_ip}")
        matched_prefix, search_path = trie.longest_prefix_match(invalid_ip)
        print(f"Result: {matched_prefix}")

    print("\nGenerating performance visualizations...")
    trie.visualize_performance()

    return results


if __name__ == "__main__":
    import time

    results = test_ipv4_longest_prefix_match()
    print("\nAnalysis complete! Check the generated visualization files.")