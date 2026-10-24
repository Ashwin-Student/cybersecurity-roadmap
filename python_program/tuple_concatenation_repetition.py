even_no=(2,4,6,8)
odd_no=(1,3,5,7)

total_no = even_no + odd_no

result=()

while(True):
    no = int(input("enter the no to multiply the tuplle elements:"))
    if no == 0 or no < 0:
        break
    else:
        for t in total_no:
            rs = t * no
            result+=(rs,)
        print(result)

