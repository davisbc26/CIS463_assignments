#Help Recieved: Dr. Park GitHub Repository, Lecture, ChatGPT to fix errors in code

import socket
import threading

SERVER_IP = '10.4.2.30'   #Raspberry Pi IP Address
SERVER_PORT = 12345        #PORT

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen(5)

clients = {}  # Store clients as {nickname: socket}
nicknames = []  # List of nicknames
stop_flag = threading.Event()  # Flag for stopping server

#Broadcast method
def broadcast(message, sender_socket=None):
    """Send a message to all clients except the sender."""
    for client in clients.values():
        if client != sender_socket:
            client.send(message)

# Whisper method
def whisper(message, sender, target_nickname):
    """Send a private message to a specific client."""
    if target_nickname in clients:
        target_socket = clients[target_nickname]
        target_socket.send(f"[Whisper from {sender}]: {message}".encode('utf-8'))
    else:
        sender_socket = clients[sender]
        sender_socket.send(f"User {target_nickname} not found.".encode('utf-8'))

def served_handle(client, nickname):
    """Handle messages from a client."""
    while not stop_flag.is_set():
        try:
            message = client.recv(1024).decode('utf-8')
            if message.lower() == 'exit':  # Handle client exit
                print(f"{nickname} disconnected.")
                client.send("You have been disconnected.".encode('utf-8'))
                client.close()
                del clients[nickname]
                nicknames.remove(nickname)
                broadcast(f"{nickname} has left the chat.".encode('utf-8'))
                break
            elif message.startswith("/w "):  # Whisper feature
                parts = message.split(" ", 2)
                if len(parts) < 3:
                    client.send("Usage: /w <nickname> <message>".encode('utf-8'))
                else:
                    _, target_nickname, private_message = parts
                    whisper(private_message, nickname, target_nickname)
            else:
                print(f"{nickname}: {message}")
                broadcast(f"{nickname}: {message}".encode('utf-8'))
        except:
            del clients[nickname]
            nicknames.remove(nickname)
            client.close()
            broadcast(f"{nickname} has left the chat.".encode('utf-8'))
            break

if __name__ == '__main__':
    print('Server is up and listening...')

    while True:
        client_conn, address = server.accept()
        print(f'Connected with {str(address)}')

        client_conn.send("NICKNAME".encode('utf-8'))
        nickname = client_conn.recv(1024).decode('utf-8')

        # Ensure unique nicknames
        if nickname in nicknames:
            client_conn.send("Nickname already taken. Choose another.".encode('utf-8'))
            client_conn.close()
            continue

        print(f'Nickname: {nickname}')
        clients[nickname] = client_conn
        nicknames.append(nickname)

        broadcast(f"{nickname} has joined the chat.".encode('utf-8'))
        client_conn.send("Connected to the server! Type 'exit' to leave. Use '/w <nickname> <message>' to whisper.".encode('utf-8'))

        thread = threading.Thread(target=served_handle, args=(client_conn, nickname))
        thread.start()