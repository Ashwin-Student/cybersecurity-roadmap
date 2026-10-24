import re

text = input("Enter the text para: ")


result = re.findall(r'\b\w{5}\b', text)

print(result)
