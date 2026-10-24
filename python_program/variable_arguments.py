
def calculate_total_expenses(*expenses):
    total = 0


    for amount in expenses:
        total += amount

    if total > 10000:
        return print("Warning")
    else:
        return print("In the budget")




weekly_spending = [132,235,2336]
print(calculate_total_expenses(*weekly_spending))
