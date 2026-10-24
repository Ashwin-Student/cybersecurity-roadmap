indicators = ["UNION SELECT", "OR 1=1"]

requests = []

n = int(input("Enter number of requests: "))

for i in range(n):
    requests.append(input())

print("\nSuspicious Requests:")

for request in requests:
    for indicator in indicators:
        if indicator.lower() in request.lower():
            print(request)
            print("Indicator:", indicator)
            break