import socket

BUFFER_SIZE = 1024

# Configuração do servidor (IP e Porta)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 12345))

clients = {}

print("Servidor rodando e aguardando mensagens...")

while True:
    data, addr = server_socket.recvfrom(BUFFER_SIZE)
    message = data.decode()

    # Registro de clientes
    if addr not in clients:
        clients[addr] = addr
        print(f"Cliente {addr} conectado.")

    # Verifica se o cliente enviou uma mensagem de saída
    if message.lower() == "sair":
        print(f"Cliente {addr} desconectado.")
        del clients[addr]
        continue

    # Enviar a mensagem para todos os outros clientes
    for client_addr in clients:
        if client_addr != addr:
            server_socket.sendto(message.encode(), client_addr)
