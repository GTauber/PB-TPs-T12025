import subprocess
import argparse
import sys
import platform
import os
import shutil


def check_nmap_installed():
    if shutil.which("nmap") is not None:
        return True
    else:
        print("Erro: Nmap não encontrado.")
        print("Por favor, instale o Nmap antes de usar este script.")
        if platform.system() == "Windows":
            print("Download: https://nmap.org/download.html")
        elif platform.system() == "Linux":
            print("Instale com: sudo apt-get install nmap ou sudo yum install nmap")
        elif platform.system() == "Darwin":
            print("Instale com: brew install nmap")
        return False


def run_nmap_scan(target, arguments=None):
    if arguments is None:
        arguments = ["-sV"]

    cmd = ["nmap", target] + arguments

    print(f"Executando comando: {' '.join(cmd)}")
    print("Isso pode levar algum tempo, dependendo do alvo e das opções...")

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Erro ao executar Nmap: {stderr}")
            return None

        return stdout
    except Exception as e:
        print(f"Erro ao executar o comando: {e}")
        return None


def parse_nmap_output(output):
    if not output:
        return

    print("\nResultados da varredura Nmap:\n")
    print("-" * 60)

    print(output)
    print("-" * 60)

    open_ports = []
    for line in output.splitlines():
        if "open" in line and "tcp" in line:
            open_ports.append(line.strip())

    if open_ports:
        print("\nResumo de portas abertas:")
        for port in open_ports:
            print(f"  {port}")


def main():
    if not check_nmap_installed():
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Executa varredura de portas com Nmap via subprocess')
    parser.add_argument('target', help='Alvo da varredura (IP ou hostname)')
    parser.add_argument('--scan-type', '-t', choices=['basic', 'full', 'service', 'os'],
                        default='service', help='Tipo de varredura a ser realizada')

    args = parser.parse_args()

    scan_arguments = {
        'basic': ["-sS", "-F"],
        'full': ["-sS", "-p-"],
        'service': ["-sV"],
        'os': ["-sS", "-O"]
    }

    if args.scan_type in ['basic', 'full', 'os'] and os.geteuid() != 0:
        print("Aviso: Alguns tipos de varredura requerem privilégios de root/administrador.")
        print("Considere executar este script com 'sudo'.")

    output = run_nmap_scan(args.target, scan_arguments[args.scan_type])

    if output:
        parse_nmap_output(output)
    else:
        print("Falha ao executar a varredura. Verifique o alvo e suas permissões.")


if __name__ == "__main__":
    main()