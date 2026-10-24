import re

text = input("Enter the sentence: ")


result = re.sub(r'[^0-9]', '', text)

print(result)
