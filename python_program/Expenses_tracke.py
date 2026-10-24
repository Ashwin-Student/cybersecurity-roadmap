E_list=[]


print('''
  Enter the Expenses.
  if you Enter the "0" after that we will not get an entry.
      ''')

while (True) :
    ex=float(input("Enter the expenses"))
    if ex != 0:
        E_list += [ex]
    else:
        break


total=0
for i in E_list:
    total+=i

if total > 5000:
    print("Your Expenses exceeds the predefined budget")
else:
    print("Your Expenses is with in the budget range")