
list = []
n=int(input("Enter no you wnat to isert in list"))

for i in range (0,n):
    no=int(input("enter the no :"))
    list = list + [no]

max=float('-inf')
min=float('inf')

for item in list:
    if item > max :
        max = item

    elif item < min:
        min = item

print(f"max no is {max}")
print(f"min no is {min}")