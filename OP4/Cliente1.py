import socket
import threading
from tkinter import *

def receive_messages():
    while True:
        try:
            message, _ = client_socket.recvfrom(BUFFER_SIZE)
            listbox.insert(END, f"Recebido: {message.decode()}")
        except:
            print("Erro ao receber mensagem.")
            break

def send_message():
    message = entry.get()
    client_socket.sendto(message.encode(), server_address)
    listbox.insert(END, f"Eu: {message}")
    entry.delete(0, END)

def on_close():
    client_socket.sendto("sair".encode(), server_address)
    client_socket.close()
    root.destroy()

# Configuração do Cliente 1
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(("0.0.0.0", 54321))  # Permitir que o cliente se conecte de qualquer interface
server_address = ("192.168.0.19", 12345) # Substitua "192.168.0.19" pelo IP do servidor
BUFFER_SIZE = 1024

# Interface Gráfica
root = Tk()
root.title("Cliente 1")

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

# Thread para receber mensagens
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
