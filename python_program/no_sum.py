import re

inp = input("Enter the string which contains numbers and characters: ")

result = re.findall(r'\d+', inp)

total = 0


for i in result:
    total += int(i)

print(f"The sum of all numbers is: {total}")
