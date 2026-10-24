import socket

HOST = '127.0.0.1'
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Server is listening...")

    conn, addr = server_socket.accept()

    with conn:
        print("Connected by:", addr)

        message = conn.recv(1024).decode()
        print("Received from client:", message)

        modified_message = (
            "Uppercase: " + message.upper() +
            "\nLowercase: " + message.lower()
        )

        conn.sendall(modified_message.encode())
        print("Response sent to client.")

finally:
    server_socket.close()
    print("Server socket closed.")