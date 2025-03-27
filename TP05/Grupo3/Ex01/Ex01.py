import socket
import ssl
import os
import subprocess
import sys


def generate_self_signed_cert(cert_file="server.crt", key_file="server.key"):
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print(f"Certificado já existe: {cert_file} e {key_file}")
        return

    print("Gerando certificado autoassinado...")
    cmd = [
        "openssl", "req", "-x509", "-newkey", "rsa:4096", "-nodes",
        "-out", cert_file, "-keyout", key_file,
        "-days", "365", "-subj", "/CN=localhost"
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Certificado gerado: {cert_file} e {key_file}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao gerar certificado: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Erro: OpenSSL não encontrado. Instale o OpenSSL para continuar.")
        sys.exit(1)


def start_tls_server(host='localhost', port=8443, cert_file="server.crt", key_file="server.key"):
    generate_self_signed_cert(cert_file, key_file)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Servidor TLS ativo em {host}:{port}")

        while True:
            client_socket, addr = server_socket.accept()
            tls_socket = context.wrap_socket(client_socket, server_side=True)

            try:
                print(f"Conexão estabelecida com {addr}")

                data = tls_socket.recv(1024)
                if not data:
                    break

                message = data.decode('utf-8')
                print(f"Recebido: {message}")

                tls_socket.sendall(data)

            except Exception as e:
                print(f"Erro na comunicação: {e}")
            finally:
                tls_socket.close()

    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    except Exception as e:
        print(f"Erro no servidor: {e}")
    finally:
        server_socket.close()


def tls_client(host='localhost', port=8443, message="Olá, servidor TLS!"):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

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


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        start_tls_server()
    elif len(sys.argv) > 1 and sys.argv[1] == "client":
        message = "Olá, servidor TLS!"
        if len(sys.argv) > 2:
            message = sys.argv[2]
        tls_client(message=message)
    else:
        print("Uso: python script.py server|client [mensagem]")