import socket

RECEIVER_IP = '127.0.0.1'
RECEIVER_PORT = 5001

emergency_services = [
    "112: National Emergency",
    "100: Police",
    "108: Ambulance"
]

sender_socket = socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM
)

try:
    for alert in emergency_services:
        sender_socket.sendto(
            alert.encode(),
            (RECEIVER_IP, RECEIVER_PORT)
        )
        print("Alert sent:", alert)

finally:
    sender_socket.close()
    print("Sender socket closed.")