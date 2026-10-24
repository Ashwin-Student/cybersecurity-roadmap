import re

pan_pattern = r'[A-Z]{5}\d{4}[A-Z]{1}'

while True:

    pan_no = input("Enter your Indian PAN Card number (or type 'exit' to quit): ").upper()

    if pan_no == 'EXIT':
        print("Exiting validation program.")
        break

    result = re.fullmatch(pan_pattern, pan_no)

    if result:
        print(f"Verification Successful! '{pan_no}' is a valid PAN number format.\n")
        break
    else:
        print(f"Verification Failed! '{pan_no}' is invalid. Please try again.\n")
