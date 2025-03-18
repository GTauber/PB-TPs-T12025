import socket
import threading
import sys
import argparse
import signal


class TCPClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = None
        self.running = False

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            print(f"Conectando ao servidor {self.server_host}:{self.server_port}...")
            self.client_socket.connect((self.server_host, self.server_port))

            self.running = True
            print("Conectado! Digite suas mensagens (ou 'sair' para encerrar):")

            signal.signal(signal.SIGINT, self.handle_shutdown)
            signal.signal(signal.SIGTERM, self.handle_shutdown)

            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

            self.send_messages()

        except socket.error as e:
            print(f"Erro ao conectar: {e}")
            self.disconnect()

    def receive_messages(self):
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    print("\nConexão encerrada pelo servidor.")
                    self.running = False
                    break

                message = data.decode('utf-8')
                print(message, end='')

            except socket.error as e:
                if self.running:
                    print(f"\nErro ao receber mensagem: {e}")
                self.running = False
                break

    def send_messages(self):
        while self.running:
            try:
                message = input()

                if not self.running:
                    break

                self.client_socket.send(message.encode('utf-8'))

                if message.lower() == "sair":
                    import time
                    time.sleep(0.5)
                    self.running = False
                    break

            except EOFError:
                self.running = False
                break
            except KeyboardInterrupt:
                pass
            except socket.error as e:
                print(f"Erro ao enviar mensagem: {e}")
                self.running = False
                break

    def handle_shutdown(self, sig, frame):
        print("\nEncerrando conexão...")
        self.disconnect()
        sys.exit(0)

    def disconnect(self):
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            print("Desconectado do servidor.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cliente TCP simples')
    parser.add_argument('-H', '--host', default='localhost', help='Endereço do servidor (padrão: localhost)')
    parser.add_argument('-p', '--port', type=int, default=8888, help='Porta do servidor (padrão: 8888)')

    args = parser.parse_args()

    client = TCPClient(args.host, args.port)
    client.connect()