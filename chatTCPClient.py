#Help Recieved: Dr. Park GitHub Repository, Lecture, ChatGPT to fix errors in code

import socket
import threading

SERVER_IP = '10.4.2.30'    #Raspberry Pi IP Address
SERVER_PORT = 12345         #PORT

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

nickname = input("Enter your nickname: ")
client.send(nickname.encode('utf-8'))

def receive_messages():
    '''Receive messages from the server.'''
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Disconnected from server.")
            client.close()
            break

def send_messages():
    '''Send messages to the server.'''
    while True:
        message = input()
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
