import socket

HOST = '127.0.0.1'
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Server is listening......")

    conn, addr = server_socket.accept()

    with conn:
        print("Connection is established with", addr)


        while True:

            msg = conn.recv(1024).decode().strip()

            if not msg or msg.lower() == 'bye':
                print("Client said bye or disconnected. Closing chat.")
                break

            print(f"Client: {msg}")


            server_msg = input("Server: ")
            conn.sendall(server_msg.encode())


            if server_msg.lower() == 'bye':
                print("You typed bye. Closing chat.")
                break

finally:
    server_socket.close()
    print("Server socket is closed.")
