import socket
import threading
import datetime
import sys
import signal


class TCPServer:
    def __init__(self, host='0.0.0.0', port=8888, max_clients=5):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.server_socket = None
        self.active_clients = []
        self.running = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.host, self.port))

            self.server_socket.listen(self.max_clients)
            self.running = True

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Servidor iniciado em {self.host}:{self.port}")
            print(f"[{current_time}] Aguardando conexões...")

            signal.signal(signal.SIGINT, self.handle_shutdown)
            signal.signal(signal.SIGTERM, self.handle_shutdown)

            self.accept_connections()

        except socket.error as e:
            print(f"Erro ao iniciar o servidor: {e}")
            self.stop()

    def accept_connections(self):
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()

                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()

                self.active_clients.append((client_socket, client_address, client_thread))

            except socket.error as e:
                if self.running:
                    print(f"Erro ao aceitar conexão: {e}")
                break

    def handle_client(self, client_socket, client_address):
        ip, port = client_address
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Nova conexão estabelecida com {ip}:{port}")

        try:
            welcome_msg = f"Bem-vindo ao servidor TCP! Você está conectado de {ip}:{port}\n"
            client_socket.send(welcome_msg.encode('utf-8'))

            while self.running:
                data = client_socket.recv(1024)
                if not data:
                    break

                message = data.decode('utf-8').strip()
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{current_time}] Mensagem de {ip}:{port}: {message}")

                if message.lower() == "sair":
                    client_socket.send("Até logo!\n".encode('utf-8'))
                    break

                response = f"Mensagem recebida: {message}\n"
                client_socket.send(response.encode('utf-8'))

        except socket.error as e:
            if self.running:
                print(f"Erro na comunicação com {ip}:{port}: {e}")
        finally:
            client_socket.close()
            self.active_clients = [c for c in self.active_clients if c[0] != client_socket]
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Conexão com {ip}:{port} encerrada")

    def handle_shutdown(self, sig, frame):
        print("\nEncerrando o servidor...")
        self.stop()
        sys.exit(0)

    def stop(self):
        self.running = False

        for client_socket, client_address, _ in self.active_clients:
            try:
                client_socket.close()
            except:
                pass

        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass

        print("Servidor encerrado.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Servidor TCP simples')
    parser.add_argument('-H', '--host', default='0.0.0.0', help='Endereço IP do servidor (padrão: 0.0.0.0)')
    parser.add_argument('-p', '--port', type=int, default=8888, help='Porta do servidor (padrão: 8888)')
    parser.add_argument('-c', '--max-clients', type=int, default=5, help='Número máximo de clientes (padrão: 5)')

    args = parser.parse_args()

    server = TCPServer(args.host, args.port, args.max_clients)
    server.start()