import socket
import tkinter as tk
from threading import Thread

# Configurações do cliente
BUFFER_SIZE = 1024
TIMEOUT = 2
seq_num = 0  # Inicializando o número de sequência

# Função para enviar mensagens
def send_message():
    global seq_num  # Declarando que vamos usar a variável global seq_num
    message = message_entry.get()
    target_ip = target_ip_entry.get()
    target_port = target_port_entry.get()

    if not message or not target_ip or not target_port:
        chat_log.insert(tk.END, "Por favor, insira todos os campos corretamente.\n")
        return

    max_retries = 5  # Definindo o número máximo de tentativas de retransmissão
    attempts = 0

    while attempts < max_retries:
        try:
            # Enviando mensagem com número de sequência e endereço do alvo
            data = f"{seq_num}{target_ip}|{target_port}|{message}"
            client_socket.sendto(data.encode(), (target_ip, int(target_port)))

            # Aguardando ACK do servidor
            ack, _ = client_socket.recvfrom(BUFFER_SIZE)
            if ack.decode() == f"ACK{seq_num}":
                chat_log.insert(tk.END, f"Eu: {message}\n")
                message_entry.delete(0, tk.END)
                seq_num = (seq_num + 1) % 2
                break
            else:
                print("ACK incorreto, retransmitindo pacote")
        except socket.timeout:
            print("Timeout, retransmitindo pacote")
            attempts += 1
    
    if attempts == max_retries:
        chat_log.insert(tk.END, "Erro: Não foi possível enviar a mensagem após várias tentativas.\n")

# Função para receber mensagens
def receive_messages():
    while True:
        try:
            data, _ = client_socket.recvfrom(BUFFER_SIZE)
            seq_num_recv = int(data.decode()[0])
            _, _, message = data.decode()[1:].split('|', 2)
            chat_log.insert(tk.END, f"Mensagem recebida: {message}\n")
        except:
            continue

# Função para iniciar o modo selecionado
def start_mode():
    mode = mode_var.get()
    local_ip = local_ip_entry.get()
    local_port = local_port_entry.get()

    if not local_ip or not local_port:
        chat_log.insert(tk.END, "Por favor, insira IP e Porta válidos.\n")
        return

    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Configurando a opção SO_REUSEADDR para reutilizar a porta
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    client_socket.bind((local_ip, int(local_port)))
    client_socket.settimeout(TIMEOUT)

    if mode == "send":
        send_button.config(state=tk.NORMAL)
    elif mode == "receive":
        receive_thread = Thread(target=receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Chat UDP - Cliente Único")

frame = tk.Frame(root)
scrollbar = tk.Scrollbar(frame)
chat_log = tk.Text(frame, height=20, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame.pack()

local_ip_label = tk.Label(root, text="Meu IP:")
local_ip_label.pack(padx=5, pady=5)
local_ip_entry = tk.Entry(root)
local_ip_entry.pack(padx=5, pady=5)

local_port_label = tk.Label(root, text="Minha Porta:")
local_port_label.pack(padx=5, pady=5)
local_port_entry = tk.Entry(root)
local_port_entry.pack(padx=5, pady=5)

target_ip_label = tk.Label(root, text="IP do Destinatário:")
target_ip_label.pack(padx=5, pady=5)
target_ip_entry = tk.Entry(root)
target_ip_entry.pack(padx=5, pady=5)

target_port_label = tk.Label(root, text="Porta do Destinatário:")
target_port_label.pack(padx=5, pady=5)
target_port_entry = tk.Entry(root)
target_port_entry.pack(padx=5, pady=5)

mode_var = tk.StringVar(value="send")
send_radio = tk.Radiobutton(root, text="Enviar", variable=mode_var, value="send")
send_radio.pack(anchor=tk.W)
receive_radio = tk.Radiobutton(root, text="Receber", variable=mode_var, value="receive")
receive_radio.pack(anchor=tk.W)

start_button = tk.Button(root, text="Iniciar", command=start_mode)
start_button.pack(padx=5, pady=5)

message_label = tk.Label(root, text="Mensagem:")
message_label.pack(padx=5, pady=5)
message_entry = tk.Entry(root, width=50)
message_entry.pack(padx=5, pady=5)

send_button = tk.Button(root, text="Enviar", command=send_message, state=tk.DISABLED)
send_button.pack(padx=5, pady=5)

# Iniciando o loop principal do Tkinter
root.mainloop()
