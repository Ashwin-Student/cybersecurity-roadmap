blood_group = ('A+','O+','B+','AB+','A-','A+','O+','O+','AB+','A+')

blood=input("Enter the boold group:")

if blood in blood_group:
    count1 = 0
    for b in blood_group:
        if blood == b:
            count1 += 1
    print(count1)