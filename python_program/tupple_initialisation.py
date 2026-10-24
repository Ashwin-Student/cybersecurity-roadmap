





employee_detail=([1,'Ash','manager'],[2,'Ath','employee'],[3,'bha','employee'])


emp1, emp2, emp3 = employee_detail

for emp in employee_detail:
    if emp[2] == 'manager':
        print("you have an special welcome, your are an manager")
    else:
        print("Welcome!, you are an employee")