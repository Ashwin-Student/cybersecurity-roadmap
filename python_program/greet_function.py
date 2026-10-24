

def greet_users():
    while(True):
        name=input("Enter your name or if you want to quite type'quite':")
        if name == 'quite' or name == 'Quite':
            break
        else:
            print(f"Hello, {name}. Welcome to Our Company.")


greet_users()