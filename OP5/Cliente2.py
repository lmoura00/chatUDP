import socket
import threading
import hashlib
import time
from tkinter import *

TIMEOUT = 5  # Timeout para reenvio (em segundos)
BUFFER_SIZE = 1024

def compute_checksum(data):
    """Computa o checksum para os dados."""
    return hashlib.md5(data).hexdigest()

def receive_ack():
    """Recebe o ACK e verifica se é o correto."""
    global ack_received, ack_num
    while True:
        try:
            message, _ = client_socket.recvfrom(BUFFER_SIZE)
            if message.decode().startswith("ACK"):
                ack_num = int(message.decode()[3])
                if ack_num == seq_num:
                    ack_received = True
                    break
            else:
                listbox.insert(END, f"Recebido: {message.decode()}")
        except:
            break

def send_message():
    global seq_num, ack_received
    message = entry.get()
    checksum = compute_checksum(message.encode())
    packet = f"{checksum}|{seq_num}|{message}"
    
    ack_received = False
    while not ack_received:
        client_socket.sendto(packet.encode(), server_address)
        listbox.insert(END, f"Enviado: {message}")
        
        # Thread para receber ACK e mensagens
        ack_thread = threading.Thread(target=receive_ack)
        ack_thread.start()

        # Espera até o timeout ou receber o ACK correto
        ack_thread.join(timeout=TIMEOUT)
        
        if not ack_received:
            listbox.insert(END, "Timeout, retransmitindo pacote.")
    
    seq_num = 1 - seq_num  # Alterna entre 0 e 1
    entry.delete(0, END)

def receive_messages():
    """Recebe mensagens continuamente e exibe no Tkinter."""
    while True:
        try:
            message, _ = client_socket.recvfrom(BUFFER_SIZE)
            if not message.decode().startswith("ACK"):
                listbox.insert(END, f"Recebido: {message.decode()}")
        except:
            break

def on_close():
    client_socket.close()
    root.destroy()

# Configuração do Cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(("0.0.0.0", 54321))  # Porta do Cliente 1
server_address = ("192.168.0.19", 12345)  # Substitua pelo IP do servidor
seq_num = 0  # Número de sequência inicial
ack_received = False
ack_num = -1

# Interface Gráfica
root = Tk()
root.title("Cliente 2")

frame = Frame(root)
scrollbar = Scrollbar(frame)
listbox = Listbox(frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(side=LEFT, fill=BOTH)
listbox.pack()
frame.pack()

entry = Entry(root, width=40)
entry.pack(pady=10)

send_button = Button(root, text="Enviar", command=send_message)
send_button.pack()

# Thread para receber mensagens continuamente
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True  # Permite fechar o Tkinter corretamente
receive_thread.start()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
