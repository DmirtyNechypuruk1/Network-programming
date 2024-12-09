#1 Echo-сервер
#Цей сервер приймає з'єднання від клієнта та повертає йому отримані дані.

import socket

def start_echo_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server is running on {host}:{port}")
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode()}")
                conn.sendall(data)

if __name__ == "__main__":
    start_echo_server()

#########################################################################################################################################

#2 Echo-клієнт
#Цей клієнт підключається до сервера, надсилає текстове повідомлення та отримує відповідь (код з першого завдання повинен бути запущений)

import socket

def start_echo_client(host='127.0.0.1', port=65432, message="Hello, Server!"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")

if __name__ == "__main__":
    start_echo_client()

 ##########################################################################################################################################

#3 Модифікований сервер для роботи з багатьма клієнтами, сервер обробляє клієнтів послідовно(сервер працює постійно)

import socket

def start_persistent_echo_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server is running on {host}:{port}")
        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print(f"Connection with {addr} closed.")
                        break
                    print(f"Received from {addr}: {data.decode()}")
                    conn.sendall(data)

if __name__ == "__main__":
    start_persistent_echo_server()





