import socket
import sys
import signal
import argparse
import datetime


class UDPClient:
    def __init__(self, server_host, server_port, timeout=5):
        self.server_host = server_host
        self.server_port = server_port
        self.timeout = timeout
        self.client_socket = None
        self.running = False

    def start(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            self.client_socket.settimeout(self.timeout)

            self.running = True
            print(f"Cliente UDP iniciado, pronto para enviar mensagens para {self.server_host}:{self.server_port}")
            print("Digite 'hora' para obter a hora do servidor")
            print("Digite 'data' para obter a data do servidor")
            print("Digite 'sair' para encerrar")

            signal.signal(signal.SIGINT, self.handle_shutdown)
            signal.signal(signal.SIGTERM, self.handle_shutdown)

            self.message_loop()

        except socket.error as e:
            print(f"Erro ao criar socket: {e}")
            self.stop()

    def message_loop(self):
        while self.running:
            try:
                message = input("\nDigite uma mensagem: ")

                if message.lower() == "sair":
                    print("Encerrando cliente...")
                    self.running = False
                    break

                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                self.client_socket.sendto(message.encode('utf-8'), (self.server_host, self.server_port))
                print(f"[{current_time}] Mensagem enviada: {message}")

                try:
                    data, server = self.client_socket.recvfrom(1024)
                    response = data.decode('utf-8')
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{current_time}] Resposta do servidor: {response}")
                except socket.timeout:
                    print("Timeout: Servidor não respondeu dentro do tempo limite.")

            except EOFError:
                self.running = False
                break
            except KeyboardInterrupt:
                pass
            except socket.error as e:
                print(f"Erro de comunicação: {e}")

    def handle_shutdown(self, sig, frame):
        print("\nEncerrando cliente...")
        self.stop()
        sys.exit(0)

    def stop(self):
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        print("Cliente encerrado.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cliente UDP simples')
    parser.add_argument('-H', '--host', default='localhost', help='Endereço do servidor (padrão: localhost)')
    parser.add_argument('-p', '--port', type=int, default=9999, help='Porta do servidor (padrão: 9999)')
    parser.add_argument('-t', '--timeout', type=int, default=5, help='Timeout em segundos (padrão: 5)')

    args = parser.parse_args()

    client = UDPClient(args.host, args.port, args.timeout)
    client.start()