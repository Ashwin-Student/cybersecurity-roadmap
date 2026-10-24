import os


current_dir = os.getcwd()

if 'python' in current_dir.lower():
    print("You are in python project folder.")
else:
    print("standard folder")
