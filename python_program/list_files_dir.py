import os


list1 = os.listdir()

for i in list1:

    if os.path.isfile(i):
        print(f"File: {i}")


    elif os.path.isdir(i):
        print(f"Dir: {i}")

    else:
        print(f"Not a file nor dir: {i}")
