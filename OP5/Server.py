import socket
import hashlib

BUFFER_SIZE = 1024

def compute_checksum(data):
    """Computa o checksum para os dados."""
    return hashlib.md5(data).hexdigest()

# Configuração do servidor (IP e Porta)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 12345))

expected_seq_num = 0

print("Servidor rodando e aguardando mensagens...")

while True:
    data, addr = server_socket.recvfrom(BUFFER_SIZE)
    received_checksum, seq_num, message = data.decode().split('|', 2)
    
    seq_num = int(seq_num)
    computed_checksum = compute_checksum(message.encode())
    
    if received_checksum == computed_checksum:
        if seq_num == expected_seq_num:
            print(f"Mensagem recebida corretamente: {message} de {addr}")
            ack_msg = f"ACK{seq_num}"
            server_socket.sendto(ack_msg.encode(), addr)
            expected_seq_num = 1 - expected_seq_num  # Alterna entre 0 e 1
        else:
            print(f"Mensagem duplicada recebida: {message} de {addr}")
            ack_msg = f"ACK{1 - seq_num}"  # Reenvia o último ACK
            server_socket.sendto(ack_msg.encode(), addr)
    else:
        print("Erro de checksum, descartando pacote.")
        nack_msg = f"NACK{seq_num}"
        server_socket.sendto(nack_msg.encode(), addr)
