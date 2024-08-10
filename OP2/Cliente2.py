import socket
import time

# Configurações do cliente
SERVER_IP = "127.0.1.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024
TIMEOUT = 2

# Criando o socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

seq_num = 0

# Endereço do cliente alvo
target_ip = input("Digite o IP do destinatário: ")
target_port = input("Digite a porta do destinatário: ")

while True:
    message = input("Digite a mensagem para o destinatário: ")
    
    if not message:
        break
    
    while True:
        # Enviando mensagem com número de sequência e endereço do alvo
        data = f"{seq_num}{target_ip}|{target_port}|{message}"
        client_socket.sendto(data.encode(), (SERVER_IP, SERVER_PORT))
        
        try:
            # Aguardando ACK do servidor
            ack, server_address = client_socket.recvfrom(BUFFER_SIZE)
            if ack.decode() == f"ACK{seq_num}":
                print("ACK recebido, enviando próximo pacote")
                seq_num = (seq_num + 1) % 2
                break
            else:
                print("ACK incorreto, retransmitindo pacote")
        except socket.timeout:
            print("Timeout, retransmitindo pacote")
