class Train_Ticket:
    def __init__(self, passenger_name, age):
        self.pas = passenger_name
        self.ag = age

    def ver(self):

        for i, j in zip(self.pas, self.ag):
            print(f"Name: {i}")
            print(f"Age: {j}")

passenger_name = []
age = []
i = 0
while i < 3:
    i += 1
    l = input("Enter the name of passenger: ")
    a = input("Enter the age of passenger: ")
    passenger_name += [l]
    age += [a]

ticket = Train_Ticket(passenger_name, age)
ticket.ver()
