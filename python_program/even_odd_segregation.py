

list = [1,7423,13,34,354,9,24,7,19,20]
even=[]
odd=[]

for i in list:
    if i % 2 == 0:
        even +=[i]
    else:
        odd+=[i]
print(even)
print(odd)