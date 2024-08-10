import socket
import random

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

clients = {}
expected_seq_nums = {}

while True:
    # Recebendo dados do cliente
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    
    # Simulando perda de pacotes
    if simulate_packet_loss():
        print("Pacote perdido!")
        continue
    
    # Parse da mensagem recebida
    seq_num = int(data.decode()[0])
    target_ip, target_port, message = data.decode()[1:].split('|', 2)
    target_port = int(target_port)
    
    if client_address not in expected_seq_nums:
        expected_seq_nums[client_address] = 0
    
    # Verifica se o número de sequência é o esperado
    if seq_num == expected_seq_nums[client_address]:
        print(f"Mensagem recebida de {client_address}: {message}")
        ack = f"ACK{seq_num}"
        expected_seq_nums[client_address] = (expected_seq_nums[client_address] + 1) % 2
        
        # Roteamento da mensagem para o cliente alvo
        target_address = (target_ip, target_port)
        clients[target_address] = client_address
        server_socket.sendto(data, target_address)
    else:
        print("Número de sequência inesperado, reenviando ACK")
        ack = f"ACK{1 - expected_seq_nums[client_address]}"
    
    # Enviando ACK para o cliente original
    server_socket.sendto(ack.encode(), client_address)
