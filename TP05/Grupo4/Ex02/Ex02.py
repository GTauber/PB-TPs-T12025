#!/usr/bin/env python3

try:
    from scapy.all import sniff, ARP
except ImportError as e:
    print(f"Erro ao importar Scapy: {e}")
    print("Por favor, instale o Scapy com: pip install scapy")
    print("Ou tente: pip install scapy==2.4.5")
    import sys

    sys.exit(1)

import argparse
import sys
import time
from datetime import datetime
import os


def check_admin():
    try:
        if os.name == 'nt':  # Windows
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except:
        return False


class ARPSpoofDetector:
    def __init__(self):
        self.ip_mac_mapping = {}
        self.alerts = set()

    def process_packet(self, packet):
        if packet.haslayer(ARP):
            arp = packet[ARP]

            if arp.op == 2:
                ip = arp.psrc
                mac = arp.hwsrc

                if ip in self.ip_mac_mapping:
                    stored_mac = self.ip_mac_mapping[ip]

                    if stored_mac != mac:
                        alert_key = f"{ip}:{stored_mac}:{mac}"

                        if alert_key not in self.alerts:
                            self.alerts.add(alert_key)
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            print(f"[{timestamp}] ALERTA: Possível ARP Spoofing detectado para IP {ip}!")
                            print(f"MAC anterior: {stored_mac}, MAC atual: {mac}")

                            self.ip_mac_mapping[ip] = mac
                else:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] Novo dispositivo detectado - IP: {ip}, MAC: {mac}")
                    self.ip_mac_mapping[ip] = mac


def start_monitoring(interface=None, packet_count=0):
    detector = ARPSpoofDetector()

    print(f"Iniciando monitoramento de pacotes ARP...")
    if interface:
        print(f"Interface: {interface}")
    print("Pressione Ctrl+C para interromper o monitoramento\n")

    try:
        sniff(
            filter="arp",
            prn=detector.process_packet,
            store=0,
            iface=interface,
            count=packet_count
        )
    except KeyboardInterrupt:
        print("\nMonitoramento interrompido pelo usuário.")
    except Exception as e:
        print(f"\nErro durante o monitoramento: {e}")


def main():
    print("Detector de ARP Spoofing usando Scapy")

    if 'ARP' not in globals():
        print("Erro: Não foi possível importar os módulos necessários do Scapy.")
        sys.exit(1)

    if not check_admin():
        print("AVISO: Este script deve ser executado com privilégios de administrador.")
        print("Por favor, reinicie como administrador/root.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Monitora a rede para detectar ARP Spoofing')
    parser.add_argument('--interface', '-i',
                        help='Interface de rede para monitoramento (ex: eth0, wlan0)')

    args = parser.parse_args()

    start_monitoring(interface=args.interface)


if __name__ == "__main__":
    main()