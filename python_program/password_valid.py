import re

while True:
    password = input("Create a password: ")


    has_digit = re.search(r'\d', password)


    has_upper = re.search(r'[A-Z]', password)

    if has_digit and has_upper:
        print("Password accepted! Strong password created.")
        break
    else:
        print("Password rejected! Your password must contain:")
        if not has_digit:
            print(" - At least 1 digit")
        if not has_upper:
            print(" - At least 1 uppercase letter")
        print("Please try again.\n")
