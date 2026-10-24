g_balance = 0

def check_balance():
    return g_balance

def deposite(amount):
    global g_balance
    g_balance += amount
    return g_balance

def withdraw(amount):
    global g_balance
    if amount > g_balance:
        print("Amount is exceeding the balance")
        return g_balance
    else:
        g_balance -= amount
        return g_balance

while True:
    print('''
      1. to check the balance
      2. to deposite
      3. to withdraw
      4. to exit
    ''')
    c = input("enter your choice: ")

    match c:
        case "1":
            print(f"Current Balance: {check_balance()}")

        case "2":
            a = float(input("enter the amount: "))
            print(f"Updated Balance: {deposite(a)}")

        case "3":
            a = float(input("enter the amount: "))
            print(f"Updated Balance: {withdraw(a)}")

        case "4":
            print("Thank you for using the banking system!")
            break

        case _:
            print("Invalid choice! Please choose 1, 2, 3, or 4.")
