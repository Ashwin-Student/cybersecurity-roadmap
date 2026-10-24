import socket

HOST = '0.0.0.0'
PORT = 5002

receiver_socket = socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM
)

try:
    receiver_socket.bind((HOST, PORT))
    print("Temperature receiver is listening...")

    while True:
        data, sender_address = receiver_socket.recvfrom(1024)

        temperature = float(data.decode())

        print(f"Temperature received: {temperature:.2f} °C")
        print("Sender address:", sender_address)

        if temperature > 35:
            print("High Temperature Alert")
        else:
            print("Normal")

        print("-" * 30)

except KeyboardInterrupt:
    print("\nReceiver stopped.")

finally:
    receiver_socket.close()