def find_maximum(numbers_list):
    max=0
    for l in numbers_list:
        if l > max:
            max = l
    return max


print("enter 5 integers for the list")


list1=[]
for i in range(0,5):
    no = int(input("Enter the no:"))
    list1+=[no]


print("Max element in list is:",find_maximum(list1))



