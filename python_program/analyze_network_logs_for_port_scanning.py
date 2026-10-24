from collections import defaultdict

port_records = defaultdict(set)

n = int(input("Enter number of network records: "))

for i in range(n):
    source_ip, destination_ip, port = input().split()
    port_records[source_ip].add(port)

print("\nPotential Port Scanning Activity:")

found = False

for source_ip, ports in port_records.items():
    if len(ports) >= 5:
        print(f"Source IP: {source_ip}")
        print(f"Distinct Destination Ports: {len(ports)}")
        print("Status: Requires Investigation")
        found = True

if not found:
    print("No potential port scanning activity detected.")