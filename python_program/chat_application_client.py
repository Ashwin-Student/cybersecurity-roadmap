import socket

HOST = '127.0.0.1'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))
    print("Connected to server.")

    while True:

        client_msg = input("Client: ")
        client_socket.sendall(client_msg.encode())

        if client_msg.lower() == 'bye':
            print("You typed bye. Exiting.")
            break


        msg = client_socket.recv(1024).decode().strip()

        if not msg or msg.lower() == 'bye':
            print("Server said bye or disconnected. Exiting.")
            break

        print(f"Server: {msg}")

finally:
    client_socket.close()
    print("Client connection closed.")
