import socket
import threading
import tkinter as tk

def receive_messages(sock):
    while True:
        message, _ = sock.recvfrom(1024)
        chat_log.insert(tk.END, f"Cliente1: {message.decode()}\n")

def send_message():
    message = message_entry.get()
    sock.sendto(message.encode(), ('localhost', 12345))
    chat_log.insert(tk.END, f"Você: {message}\n")
    message_entry.delete(0, tk.END)

# Configuração do cliente
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 5002))  # Porta do Cliente2

# Interface Gráfica
root = tk.Tk()
root.title("Cliente2 - Chat UDP")

chat_log = tk.Text(root)
chat_log.pack()

message_entry = tk.Entry(root)
message_entry.pack()

send_button = tk.Button(root, text="Enviar", command=send_message)
send_button.pack()

# Thread para receber mensagens
receive_thread = threading.Thread(target=receive_messages, args=(sock,))
receive_thread.daemon = True
receive_thread.start()

root.mainloop()

