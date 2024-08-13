import socket
import threading

def checksum(data):
    return sum(data) % 256

def rdt_send(sock, address, data, seq):
    packet = bytearray([seq]) + data
    cksum = checksum(packet)
    packet += bytearray([cksum])
    sock.sendto(packet, address)

def rdt_receive(sock):
    while True:
        packet, addr = sock.recvfrom(1024)
        seq = packet[0]
        cksum = packet[-1]
        data = packet[1:-1]
        
        if cksum == checksum(bytearray([seq]) + data):
            ack = (seq + 1) % 2  # Alterna entre 0 e 1
            sock.sendto(bytearray([ack]), addr)
            return data, addr, seq

def handle_client(sock, client1_addr, client2_addr):
    seq_expected = 0
    while True:
        data, addr, seq = rdt_receive(sock)
        if addr == client1_addr:
            rdt_send(sock, client2_addr, data, seq)
        elif addr == client2_addr:
            rdt_send(sock, client1_addr, data, seq)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 12345))
    
    print("Servidor pronto e escutando...")

    client1_addr = ('localhost', 12346)
    client2_addr = ('localhost', 12347)
    
    threading.Thread(target=handle_client, args=(server_socket, client1_addr, client2_addr)).start()

if __name__ == "__main__":
    main()
