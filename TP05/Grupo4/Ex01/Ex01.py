from scapy.layers.l2 import ARP, Ether, srp
import argparse
import sys
import time


def check_admin():
    try:
        import os
        if os.name == 'nt':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except:
        return False


def arp_scan(ip_range):
    arp = ARP(pdst=ip_range)

    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether / arp

    print(f"Iniciando varredura ARP no intervalo {ip_range}...")
    start_time = time.time()

    try:
        result = srp(packet, timeout=3, verbose=0)[0]

        print(f"\nDispositivos ativos encontrados: {len(result)}")
        print("IP\t\t\tMAC")
        print("-" * 40)

        hosts_found = []
        for sent, received in result:
            hosts_found.append({'ip': received.psrc, 'mac': received.hwsrc})
            print(f"{received.psrc}\t\t{received.hwsrc}")

        print(f"\nVarredura concluída em {time.time() - start_time:.2f} segundos")
        return hosts_found

    except Exception as e:
        print(f"Erro durante a varredura: {e}")
        return []


def main():
    if not check_admin():
        print("AVISO: Este script deve ser executado com privilégios de administrador.")
        print("Por favor, reinicie como administrador/root.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Realiza varredura ARP na rede local')
    parser.add_argument('--range', '-r', default='192.168.1.0/24',
                        help='Intervalo de IPs para varredura (ex: 192.168.1.0/24)')

    args = parser.parse_args()

    arp_scan(args.range)


if __name__ == "__main__":
    main()