import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def checksum(data):
    return sum(data) % 256

def rdt_send(sock, address, data, seq):
    packet = bytearray([seq]) + data
    cksum = checksum(packet)
    packet += bytearray([cksum])
    sock.sendto(packet, address)
    
    # Aguarda o ACK
    while True:
        ack_packet, _ = sock.recvfrom(1024)
        ack = ack_packet[0]
        if ack == seq:
            break

def rdt_receive(sock, expected_seq):
    while True:
        packet, _ = sock.recvfrom(1024)
        if len(packet) < 3:  # Garantir que o pacote tenha pelo menos seq, dados e checksum
            continue
        
        seq = packet[0]
        cksum = packet[-1]
        data = packet[1:-1]
        
        if cksum == checksum(bytearray([seq]) + data) and seq == expected_seq:
            ack = seq  # Envia ACK com o número de sequência correspondente
            sock.sendto(bytearray([ack]), _)
            return data.decode(), (seq + 1) % 2  # Alterna a sequência

def receive_messages(sock, text_area, expected_seq):
    while True:
        data, expected_seq = rdt_receive(sock, expected_seq)
        if data:
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, f"Outro: {data}\n")
            text_area.config(state=tk.DISABLED)

def send_message(sock, address, text_entry, seq):
    message = text_entry.get()
    rdt_send(sock, address, message.encode(), seq)
    text_entry.delete(0, tk.END)
    return (seq + 1) % 2  # Alterna a sequência após envio

def create_gui(sock, address):
    window = tk.Tk()
    window.title("Chat Cliente")

    text_area = scrolledtext.ScrolledText(window)
    text_area.pack(padx=20, pady=5)
    text_area.config(state=tk.DISABLED)

    text_entry = tk.Entry(window, width=50)
    text_entry.pack(padx=20, pady=5)

    seq = 0  # Sequência inicial

    send_button = tk.Button(window, text="Enviar", command=lambda: send_message(sock, address, text_entry, seq))
    send_button.pack(padx=20, pady=5)

    threading.Thread(target=receive_messages, args=(sock, text_area, seq)).start()

    window.mainloop()

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Binding a uma porta específica para este cliente
    client_socket.bind(('localhost', 12346))  # Modifique para o Cliente 2 ('localhost', 12347)
    
    server_address = ('localhost', 12345)

    create_gui(client_socket, server_address)

if __name__ == "__main__":
    main()
