from collections import Counter

failed_attempts = Counter()

print("Enter login records (type 'END' to finish):")

while True:
    record = input()

    if record == "END":
        break

    ip, status = record.split()

    if status == "FAILED":
        failed_attempts[ip] += 1

print("\nSuspicious Login Attempts:")

for ip, count in failed_attempts.items():
    if count >= 3:
        print(f"IP Address: {ip}, Failed Attempts: {count}")