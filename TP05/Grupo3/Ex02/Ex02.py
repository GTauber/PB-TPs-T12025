import socket
import ssl
import sys

def monkey_patch_socket(sock):
    original_sendall = sock.sendall
    original_recv = sock.recv

    def sendall_with_logging(data, *args, **kwargs):
        print(f"Interceptado (envio): {data}")
        return original_sendall(data, *args, **kwargs)

    def recv_with_logging(bufsize, *args, **kwargs):
        data = original_recv(bufsize, *args, **kwargs)
        print(f"Interceptado (recebido): {data}")
        return data

    sock.sendall = sendall_with_logging
    sock.recv = recv_with_logging

    return sock


def tls_client_with_logging(host='localhost', port=8443, message="Mensagem segura com logging de pacotes"):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    original_wrap_socket = context.wrap_socket

    def wrap_socket_with_logging(*args, **kwargs):
        ssl_sock = original_wrap_socket(*args, **kwargs)
        return monkey_patch_socket(ssl_sock)

    context.wrap_socket = wrap_socket_with_logging

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        tls_socket = context.wrap_socket(client_socket, server_hostname=host)
        tls_socket.connect((host, port))
        print("Cliente: conexão estabelecida")

        tls_socket.sendall(message.encode('utf-8'))

        response = tls_socket.recv(1024)
        print(f"Cliente: recebido: {response.decode('utf-8')}")

    except Exception as e:
        print(f"Erro no cliente: {e}")
    finally:
        client_socket.close()


class TLSLogger:
    def __init__(self, sock):
        self.socket = sock
        self.applied = False

    def __getattr__(self, name):
        if name == 'sendall':
            return self.sendall_with_logging
        elif name == 'recv':
            return self.recv_with_logging
        return getattr(self.socket, name)

    def sendall_with_logging(self, data, *args, **kwargs):
        print(f"Interceptado (envio): {data}")
        return self.socket.sendall(data, *args, **kwargs)

    def recv_with_logging(self, bufsize, *args, **kwargs):
        data = self.socket.recv(bufsize, *args, **kwargs)
        print(f"Interceptado (recebido): {data}")
        return data


def tls_client_with_logging_alt(host='localhost', port=8443, message="Mensagem segura com logging de pacotes"):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        tls_socket = context.wrap_socket(client_socket, server_hostname=host)
        tls_socket.connect((host, port))

        logging_socket = TLSLogger(tls_socket)

        print("Cliente: conexão estabelecida")

        logging_socket.sendall(message.encode('utf-8'))

        response = logging_socket.recv(1024)
        print(f"Cliente: recebido: {response.decode('utf-8')}")

    except Exception as e:
        print(f"Erro no cliente: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = sys.argv[1]
        tls_client_with_logging(message=message)
    else:
        tls_client_with_logging()