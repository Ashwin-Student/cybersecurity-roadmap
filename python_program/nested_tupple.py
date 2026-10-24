nested_tupple=((1,2,3),(4,5,6),(7,8,9))

for t in nested_tupple:
    for t1 in t:
        if t1 % 2 == 0:
            print(t1)
       