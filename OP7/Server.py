import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 12345))
    print("Servidor UDP iniciado. Aguardando mensagens...")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        print(f"Recebido de {client_address}: {message.decode()}")

        # Enviar mensagem para o outro cliente (simulando um chat entre Cliente1 e Cliente2)
        if client_address[1] == 5001:  # Cliente1
            server_socket.sendto(message, ('localhost', 5002))  # Cliente2
        elif client_address[1] == 5002:  # Cliente2
            server_socket.sendto(message, ('localhost', 5001))  # Cliente1

if __name__ == "__main__":
    start_server()
