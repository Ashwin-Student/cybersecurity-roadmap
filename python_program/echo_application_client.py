
import socket

HOST = '127.0.0.1'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))

    message = input("Enter a string message: ")
    client_socket.sendall(message.encode())

    response = client_socket.recv(1024).decode()
    print("\nModified message received from server:")
    print(response)

finally:
    client_socket.close()
    print("Client socket closed.")