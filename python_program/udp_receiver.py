import socket

HOST = '0.0.0.0'
PORT = 5001

receiver_socket = socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM
)

try:
    receiver_socket.bind((HOST, PORT))
    print("UDP Receiver is listening...")

    for i in range(3):
        data, sender_address = receiver_socket.recvfrom(1024)

        alert = data.decode()
        print("Emergency Alert:", alert)
        print("Sender Address:", sender_address)
        print("-" * 30)

finally:
    receiver_socket.close()
    print("Receiver socket closed.")