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

def receive_messages():
    while True:
        try:
            message, _ = client_socket.recvfrom(BUFFER_SIZE)
            ack_num = int(message.decode()[3])
            if ack_num == seq_num:
                listbox.insert(END, "ACK recebido corretamente!")
                break  # Sair do loop de recebimento de mensagens
            else:
                listbox.insert(END, "ACK incorreto, aguardando retransmissão...")
        except:
            print("Erro ao receber mensagem.")
            break

def send_message():
    global seq_num, timeout_flag
    message = entry.get()
    checksum = compute_checksum(message.encode())
    packet = f"{checksum}|{seq_num}|{message}"
    
    while True:
        client_socket.sendto(packet.encode(), server_address)
        listbox.insert(END, f"Enviado: {message}")
        start_time = time.time()
        
        # Thread para receber ACK
        ack_thread = threading.Thread(target=receive_messages)
        ack_thread.start()

        # Espera até o timeout ou receber ACK correto
        while time.time() - start_time < TIMEOUT:
            if ack_thread.is_alive():
                continue
            else:
                break
        else:
            listbox.insert(END, "Timeout, retransmitindo pacote.")
            continue  # Tenta enviar novamente em caso de timeout
        
        ack_thread.join()
        seq_num = 1 - seq_num  # Alterna entre 0 e 1
        break  # Sai do loop após enviar com sucesso
    
    entry.delete(0, END)

def on_close():
    client_socket.close()
    root.destroy()

# Configuração do Cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(("127.0.0.1", ))  # Substitua pela porta do cliente correspondente
server_address = ("192.168.0.21", 2468)  # Substitua pelo IP do servidor
seq_num = 0  # Número de sequência inicial
timeout_flag = False

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

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
