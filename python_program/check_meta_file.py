import os

path = input("Enter the file or dir name: ")

if os.path.exists(path):
    size = os.path.getsize(path)

    total_size_kb = round(size / 1024, 2)


    if os.path.isfile(path):
        print(f"File size: {total_size_kb} KB")
    else:
        print(f"Directory metadata size: {total_size_kb} KB (Note: Does not include contents)")
else:
    print("invalid_path")
