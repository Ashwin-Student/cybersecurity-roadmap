class Employee:
    def __init__(self, emp_id, name, department):
        self.emp_id = emp_id
        self.name = name
        self.department = department

    def verify(self):
        print(f"emp_id is {self.emp_id}, name is {self.name} and department is {self.department}")


e1 = Employee(1,'ufidwf','it')
e2= Employee(2,'hwpbvq','sales')

e1.verify()
e2.verify()