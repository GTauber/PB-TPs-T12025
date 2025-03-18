import socket
import datetime
import signal
import sys
import argparse


class UDPServer:
    def __init__(self, host='0.0.0.0', port=9999, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.server_socket = None
        self.running = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            self.server_socket.bind((self.host, self.port))
            self.running = True

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Servidor UDP iniciado em {self.host}:{self.port}")
            print(f"[{current_time}] Aguardando mensagens...")

            signal.signal(signal.SIGINT, self.handle_shutdown)
            signal.signal(signal.SIGTERM, self.handle_shutdown)

            self.receive_messages()

        except socket.error as e:
            print(f"Erro ao iniciar o servidor: {e}")
            self.stop()

    def receive_messages(self):
        while self.running:
            try:
                data, client_address = self.server_socket.recvfrom(self.buffer_size)

                message = data.decode('utf-8').strip()
                ip, port = client_address
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{current_time}] Mensagem de {ip}:{port}: {message}")

                if message.lower() == "hora":
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    response = f"Hora atual do servidor: {current_time}"
                elif message.lower() == "data":
                    current_date = datetime.datetime.now().strftime("%d/%m/%Y")
                    response = f"Data atual do servidor: {current_date}"
                else:
                    response = f"Mensagem recebida: {message}"

                self.server_socket.sendto(response.encode('utf-8'), client_address)

            except socket.error as e:
                if self.running:
                    print(f"Erro ao receber mensagem: {e}")

    def handle_shutdown(self, sig, frame):
        print("\nEncerrando o servidor...")
        self.stop()
        sys.exit(0)

    def stop(self):
        """Para o servidor"""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        print("Servidor encerrado.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Servidor UDP simples')
    parser.add_argument('-H', '--host', default='0.0.0.0', help='Endereço IP do servidor (padrão: 0.0.0.0)')
    parser.add_argument('-p', '--port', type=int, default=9999, help='Porta do servidor (padrão: 9999)')
    parser.add_argument('-b', '--buffer', type=int, default=1024, help='Tamanho do buffer (padrão: 1024)')

    args = parser.parse_args()

    server = UDPServer(args.host, args.port, args.buffer)
    server.start()