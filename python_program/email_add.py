import re

e_list = []


for i in range(3):
    e = input("Enter the email address: ")
    e_list += [e]

print("\n--- Validation Results ---")


for email in e_list:

    result = re.search(r'@.*\.+(com|in|org)$', email)

    if result:
        print(f"{email} -> Valid")
    else:
        print(f"{email} -> Invalid try again")
