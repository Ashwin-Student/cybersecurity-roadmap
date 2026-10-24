import re

inp = input("Enter the 10-digit mobile no: ")

result = re.search(r'\b[6-9]\d{9}\b', inp)


if result:
    print("Valid mobile no")
else:
    print("Invalid mob no")
