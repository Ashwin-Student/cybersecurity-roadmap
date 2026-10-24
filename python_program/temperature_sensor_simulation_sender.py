import socket
import random
import time

RECEIVER_IP = '127.0.0.1'
RECEIVER_PORT = 5002

sender_socket = socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM
)

try:
    while True:
        temperature = random.uniform(20, 45)

        message = f"{temperature:.2f}"
        sender_socket.sendto(
            message.encode(),
            (RECEIVER_IP, RECEIVER_PORT)
        )

        print("Temperature sent:", message, "°C")
        time.sleep(2)

except KeyboardInterrupt:
    print("\nSensor stopped.")

finally:
    sender_socket.close()