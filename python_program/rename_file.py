import os


if os.path.exists('old_data.txt'):
    os.rename('old_data.txt','new_data.txt')
    print("Succcessfulyyy changedthe name")




else:
    print("file not found")
