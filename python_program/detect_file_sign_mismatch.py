signatures = {
    "FF D8 FF": "jpg",
    "89 50 4E 47 0D 0A 1A 0A": "png",
    "25 50 44 46": "pdf"
}

n = int(input("Enter number of files: "))

for i in range(1, n + 1):
    filename = input(f"File {i}: ")
    signature = input("Signature: ").upper()

    extension = filename.split(".")[-1].lower()
    detected_format = signatures.get(signature)

    print(f"File: {filename}")

    if detected_format == extension:
        print("Status: Signature matches extension")
    else:
        print("Status: WARNING - Signature does not match extension")
        if detected_format:
            print(f"Detected Format: {detected_format.upper()}")