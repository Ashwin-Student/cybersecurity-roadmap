employee_record = (('abc@123','abc','it',1000000000),('pqr@123','pqr','mech',100000),('xyz@123','xyz','it',100000))

total=0
for e in employee_record:
    if  e[2] == 'it' and e[3] > 75000:
        total += e[3]
print(total)

