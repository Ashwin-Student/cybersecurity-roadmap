import socket

HOST = '127.0.0.1'
PORT = 5000

# Create the invoice file on the server
with open("invoice.txt", "w") as file:
    file.write("INVOICE\n")
    file.write("Invoice No: 101\n")
    file.write("Customer: Rahul\n")
    file.write("Amount: Rs. 2500\n")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Server is waiting for a client...")

    conn, addr = server_socket.accept()

    with conn:
        print("Connected by:", addr)

        request = conn.recv(1024).decode().strip()

        if request == "GET_INVOICE":
            with open("invoice.txt", "rb") as file:
                data = file.read()

            conn.sendall(data)
            print("Invoice sent successfully.")
        else:
            conn.sendall(b"Invalid request")

finally:
    server_socket.close()
    print("Server closed.")