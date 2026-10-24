no=int(input("enter an multiple digit no:"))
print(f"your enter no is {no}")


count=0
mod=0
while no > 0:
    mod = no%10
    count = count + mod
    no = no // 10
print(f"sum of digits of no is {count}")

