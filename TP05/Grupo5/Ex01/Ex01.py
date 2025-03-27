import dns.resolver
import argparse
import sys


def check_dns_library():
    try:
        import dns.resolver
        return True
    except ImportError:
        print("Erro: A biblioteca dnspython não está instalada.")
        print("Instale-a com: pip install dnspython")
        return False


def get_dns_records(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(answer) for answer in answers]
    except dns.resolver.NXDOMAIN:
        print(f"Erro: O domínio {domain} não existe.")
        return []
    except dns.resolver.NoAnswer:
        print(f"Aviso: Não há registros do tipo {record_type} para {domain}.")
        return []
    except dns.exception.DNSException as e:
        print(f"Erro ao consultar registros {record_type}: {e}")
        return []


def collect_dns_info(domain):
    results = {}

    record_types = ['A', 'MX', 'NS', 'AAAA', 'TXT', 'CNAME', 'SOA']

    for record_type in record_types:
        records = get_dns_records(domain, record_type)
        if records:
            results[record_type] = records

    return results


def display_results(domain, results):
    print(f"\nInformações DNS para o domínio: {domain}\n")

    if not results:
        print("Nenhum registro DNS encontrado ou domínio inválido.")
        return

    for record_type, records in results.items():
        print(f"Registros {record_type}:")

        if record_type == 'MX':
            for record in records:
                parts = record.split(' ')
                if len(parts) > 1:
                    priority = parts[0]
                    server = ' '.join(parts[1:])
                    print(f"  {priority} {server}")
                else:
                    print(f"  {record}")
        else:
            for record in records:
                print(f"  {record}")
        print()


def main():
    if not check_dns_library():
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Coleta informações DNS de um domínio (similar ao DNSRecon)')
    parser.add_argument('domain', help='Domínio a ser consultado (ex: example.com)')

    args = parser.parse_args()
    domain = args.domain

    print(f"Coletando informações DNS para {domain}...")
    results = collect_dns_info(domain)
    display_results(domain, results)


if __name__ == "__main__":
    main()