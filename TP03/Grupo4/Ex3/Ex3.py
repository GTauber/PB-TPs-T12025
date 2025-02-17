from typing import Optional, List, Dict, Tuple
import ipaddress
from TP03.performance_analyzer.analyzer import PerformanceAnalyzer, PerformanceVisualizer
from TP03.performance_analyzer.decorators import measure_performance


class IPTrieNode:
    def __init__(self):
        self.children: Dict[int, 'IPTrieNode'] = {}
        self.is_end: bool = False
        self.prefix: Optional[str] = None
        self.mask_length: Optional[int] = None
        self.prefix_bits: Optional[str] = None
        self.version: Optional[int] = None


class IPv6Trie:
    def __init__(self):
        self.root = IPTrieNode()
        self.analyzer = PerformanceAnalyzer()
        self.search_paths: List[Dict] = []

    def _ip_to_binary(self, ip: str) -> str:
        ip_int = int(ipaddress.IPv6Address(ip))
        return format(ip_int, '0128b')

    def _get_network_and_mask(self, prefix: str) -> Tuple[str, int, str]:
        network = ipaddress.IPv6Network(prefix, strict=False)
        network_addr = str(network.network_address)
        mask_length = network.prefixlen
        binary_ip = self._ip_to_binary(network_addr)
        return network_addr, mask_length, binary_ip

    def _format_prefix_bits(self, bits: str) -> str:
        groups = [bits[i:i + 16] for i in range(0, len(bits), 16)]
        return ':'.join(groups)

    @measure_performance("insert")
    def insert(self, prefix: str) -> None:
        try:
            network_addr, mask_length, binary_ip = self._get_network_and_mask(prefix)
        except ValueError as e:
            print(f"Invalid IPv6 prefix {prefix}: {e}")
            return

        current = self.root
        prefix_bits = ""

        for i in range(mask_length):
            self.analyzer.record_comparison()
            bit = int(binary_ip[i])
            prefix_bits += str(bit)

            if bit not in current.children:
                current.children[bit] = IPTrieNode()
            current = current.children[bit]

        current.is_end = True
        current.prefix = prefix
        current.mask_length = mask_length
        current.prefix_bits = prefix_bits
        current.version = 6

        self.analyzer.end_operation(
            "insert",
            self.analyzer.start_operation("insert"),
            mask_length,
            {"prefix": prefix, "mask_length": mask_length}
        )

    @measure_performance("longest_prefix_match")
    def longest_prefix_match(self, ip: str) -> Tuple[Optional[str], List[Dict]]:
        try:
            binary_ip = self._ip_to_binary(ip)
        except ValueError as e:
            print(f"Invalid IPv6 address {ip}: {e}")
            return None, []

        current = self.root
        matched_prefix = None
        search_path = []
        current_bits = ""

        for i in range(128):
            self.analyzer.record_comparison()

            path_entry = {
                'level': i,
                'bits_seen': self._format_prefix_bits(current_bits),
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
                'bits_seen': self._format_prefix_bits(current_bits),
                'current_match': matched_prefix,
                'is_prefix': True
            })

        return matched_prefix, search_path

    def visualize_performance(self) -> None:
        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='line',
            title='IPv6 Trie Operations Performance'
        )

        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='bar',
            title='IPv6 Trie Operation Distribution'
        )

        PerformanceVisualizer.create_comparison_plot(
            self.analyzer.metrics_history,
            plot_type='heatmap',
            title='IPv6 Prefix Analysis'
        )


def test_ipv6_prefix_matching():
    trie = IPv6Trie()

    prefixes = [
        "2001:db8::/32",
        "2001:db8:1234::/48",
        "2001:db8:1234:5678::/64",
        "::/0",
        "2001::/16"
    ]

    print("\nInserting IPv6 prefixes:")
    for prefix in prefixes:
        print(f"Adding prefix: {prefix}")
        trie.insert(prefix)

    test_ips = [
        "2001:db8:1234:5678::1",
        "2001:db8:1234::1",
        "2001:db8::1",
        "2001::1",
        "2002::1",
        "2001:db8:1234:5678:1:2:3:4"
    ]

    results = []
    print("\nTesting longest prefix matches:")
    for ip in test_ips:
        print(f"\nLooking up IP: {ip}")
        matched_prefix, search_path = trie.longest_prefix_match(ip)

        print(f"Matched prefix: {matched_prefix}")
        print("Search path:")
        for step in search_path:
            if step['is_prefix']:
                print(f"Level {step['level']}: Found prefix {step['current_match']}")

        results.append({
            'ip': ip,
            'matched_prefix': matched_prefix,
            'path_length': len(search_path)
        })

    print("\nTesting error cases:")
    error_cases = [
        "2001:zz::",
        "2001::ff::ff",
        "invalid_ip",
        "2001:db8/32"
    ]

    for invalid_ip in error_cases:
        print(f"\nTesting invalid IP: {invalid_ip}")
        matched_prefix, search_path = trie.longest_prefix_match(invalid_ip)
        print(f"Result: {matched_prefix}")

    print("\nGenerating performance visualizations...")
    trie.visualize_performance()

    return results


if __name__ == "__main__":
    results = test_ipv6_prefix_matching()
    print("\nAnalysis complete! Check the generated visualization files.")