class Walet:
    def __init__(self,initial_balance):

       self.balance = initial_balance

    def add_money(self,amount):
        self.balance = self.balance + amount
        return self.balance

    def spend_money(self,amount):
        if amount > self.balance:
            print("amount is invlaid")
        else:
            self.balance = self.balance - amount
            return self.balance

p1 = Walet(2000)
print(p1.balance)
print("amount deposited is",p1.add_money(10000))
print("amount withdraw is ",p1.spend_money(1000))
