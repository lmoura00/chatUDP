import socket
import random
import time

# Configurações do servidor
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# Função para simular perda de pacotes
def simulate_packet_loss(probability=0.1):
    return random.random() < probability

# Criando o socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

print("Servidor RDT 3.0 aguardando mensagens...")

expected_seq_num = 0

while True:
    # Recebendo dados do cliente
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    
    # Simulando perda de pacotes
    if simulate_packet_loss():
        print("Pacote perdido!")
        continue

    seq_num = int(data.decode()[0])
    message = data.decode()[1:]
    
    if seq_num == expected_seq_num:
        print(f"Recebido do cliente: {message}")
        ack = f"ACK{seq_num}"
        expected_seq_num = (expected_seq_num + 1) % 2
    else:
        print("Número de sequência inesperado, reenviando ACK")
        ack = f"ACK{1 - expected_seq_num}"

    # Enviando ACK para o cliente
    server_socket.sendto(ack.encode(), client_address)
