import socket

HOST = '127.0.0.1'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))

    # Send the request to the server
    client_socket.sendall(b"GET_INVOICE")

    # Receive the file data
    with open("downloaded_invoice.txt", "wb") as file:
        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            file.write(data)

    print("Invoice downloaded successfully.")

finally:
    client_socket.close()
    print("Client connection closed.")