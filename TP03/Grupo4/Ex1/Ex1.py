from TP03.Trie.trie import IPPrefixValidator, IPTrieVisualizer


def test_ipv4_validation():
    validator = IPPrefixValidator()

    test_cases = [
        {
            'prefix': '192.168.1.0/24',
            'valid_ips': [
                '192.168.1.1',
                '192.168.1.100',
                '192.168.1.254'
            ],
            'invalid_ips': [
                '192.168.2.1',
                '192.168.0.1',
                '10.0.0.1'
            ]
        },
        {
            'prefix': '10.0.0.0/8',
            'valid_ips': [
                '10.0.0.1',
                '10.10.10.10',
                '10.255.255.255'
            ],
            'invalid_ips': [
                '11.0.0.1',
                '9.255.255.255',
                '192.168.1.1'
            ]
        },
        {
            'prefix': '172.16.0.0/12',
            'valid_ips': [
                '172.16.0.1',
                '172.20.10.10',
                '172.31.255.255'
            ],
            'invalid_ips': [
                '172.32.0.1',
                '172.15.255.255',
                '192.168.1.1'
            ]
        }
    ]

    results = []

    print("\nTesting IPv4 prefix validation:")
    for i, test_case in enumerate(test_cases, 1):
        prefix = test_case['prefix']
        print(f"\nTest Case {i}: {prefix}")

        validator.add_prefix(prefix)

        print("\nTesting valid IPs:")
        for ip in test_case['valid_ips']:
            is_valid = validator.validate_ip_in_prefix(ip, prefix)
            match = validator.match_ip(ip)
            print(f"IP: {ip}")
            print(f"Valid: {is_valid}")
            print(f"Matching prefix: {match}")
            results.append({
                'prefix': prefix,
                'ip': ip,
                'expected': True,
                'actual': is_valid,
                'match': match
            })

        print("\nTesting invalid IPs:")
        for ip in test_case['invalid_ips']:
            is_valid = validator.validate_ip_in_prefix(ip, prefix)
            match = validator.match_ip(ip)
            print(f"IP: {ip}")
            print(f"Valid: {is_valid}")
            print(f"Matching prefix: {match}")
            results.append({
                'prefix': prefix,
                'ip': ip,
                'expected': False,
                'actual': is_valid,
                'match': match
            })

    print("\nTesting error cases:")
    error_cases = [
        ('invalid_ip', '192.168.1.0/24'),
        ('192.168.1.1', 'invalid_prefix'),
        ('256.256.256.256', '192.168.1.0/24'),
        ('192.168.1.1', '192.168.1.0/33')
    ]

    for ip, prefix in error_cases:
        print(f"\nTesting invalid input - IP: {ip}, Prefix: {prefix}")
        try:
            is_valid = validator.validate_ip_in_prefix(ip, prefix)
            print(f"Result: {is_valid}")
        except Exception as e:
            print(f"Caught error as expected: {e}")

    print("\nGenerating performance visualizations...")
    IPTrieVisualizer.create_performance_plots(validator)

    return results


if __name__ == "__main__":
    results = test_ipv4_validation()
    print("\nAnalysis complete! Check the generated visualization files.")