no=int(input("enter an no:"))

if no < 1:
    print("Enter any postive no")
else :
    count = 0
    for i in range (1,(no//2)+1):

        if no%i == 0 :
            count +=1
    if count >1:
        print("no is not an prime no")
    else:
        print("no is an prime no")