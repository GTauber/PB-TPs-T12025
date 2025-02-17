import ipaddress
from typing import Optional, Dict, Tuple

from TP03.performance_analyzer.analyzer import PerformanceAnalyzer, PerformanceVisualizer
from TP03.performance_analyzer.decorators import measure_performance


class TrieNode:
    def __init__(self):
        self.children: Dict[int, 'TrieNode'] = {}
        self.is_end: bool = False
        self.prefix: Optional[str] = None
        self.mask_length: Optional[int] = None


class IPTrie:

    def __init__(self):
        self.root = TrieNode()
        self.analyzer = PerformanceAnalyzer()

    def _ip_to_binary(self, ip: str) -> str:
        ip_obj = ipaddress.ip_address(ip)
        if isinstance(ip_obj, ipaddress.IPv4Address):
            return format(int(ip_obj), '032b')
        else:
            return format(int(ip_obj), '0128b')

    def _get_network_and_mask(self, prefix: str) -> Tuple[str, int]:
        network = ipaddress.ip_network(prefix, strict=False)
        return str(network.network_address), network.prefixlen

    @measure_performance("insert")
    def insert(self, prefix: str) -> None:
        network_addr, mask_length = self._get_network_and_mask(prefix)
        binary_ip = self._ip_to_binary(network_addr)

        current = self.root
        for i in range(mask_length):
            self.analyzer.record_comparison()
            bit = int(binary_ip[i])
            if bit not in current.children:
                current.children[bit] = TrieNode()
            current = current.children[bit]

        current.is_end = True
        current.prefix = prefix
        current.mask_length = mask_length

    @measure_performance("contains")
    def contains_prefix(self, prefix: str) -> bool:
        network_addr, mask_length = self._get_network_and_mask(prefix)
        binary_ip = self._ip_to_binary(network_addr)

        current = self.root
        for i in range(mask_length):
            self.analyzer.record_comparison()
            bit = int(binary_ip[i])
            if bit not in current.children:
                return False
            current = current.children[bit]

        return current.is_end and current.mask_length == mask_length

    @measure_performance("match")
    def match_ip(self, ip: str) -> Optional[str]:
        binary_ip = self._ip_to_binary(ip)

        current = self.root
        matched_prefix = None

        for i in range(len(binary_ip)):
            self.analyzer.record_comparison()

            if current.is_end:
                matched_prefix = current.prefix

            bit = int(binary_ip[i])
            if bit not in current.children:
                break
            current = current.children[bit]

        if current.is_end:
            matched_prefix = current.prefix

        return matched_prefix


class IPPrefixValidator:

    def __init__(self):
        self.trie = IPTrie()

    @measure_performance("validate")
    def validate_ip_in_prefix(self, ip: str, prefix: str) -> bool:
        try:
            ip_obj = ipaddress.ip_address(ip)
            network = ipaddress.ip_network(prefix, strict=False)
            return ip_obj in network
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def add_prefix(self, prefix: str) -> None:
        self.trie.insert(prefix)

    def match_ip(self, ip: str) -> Optional[str]:
        return self.trie.match_ip(ip)

    def contains_prefix(self, prefix: str) -> bool:
        return self.trie.contains_prefix(prefix)


class IPTrieVisualizer:

    @staticmethod
    def create_performance_plots(validator: IPPrefixValidator):
        PerformanceVisualizer.create_comparison_plot(
            validator.trie.analyzer.metrics_history,
            plot_type='line',
            title='IP Trie Operations Performance'
        )

        PerformanceVisualizer.create_comparison_plot(
            validator.trie.analyzer.metrics_history,
            plot_type='bar',
            title='Average Operation Time'
        )

        PerformanceVisualizer.create_comparison_plot(
            validator.trie.analyzer.metrics_history,
            plot_type='heatmap',
            title='Performance Metrics Heatmap'
        )