import re


inp = input("Enter he sentence")

result = re.sub('\s+', ' ', inp)
print(inp)