class Product:
    def __init__(self, name, price):
        self.name =name
        self.price = price


    def apply_discount(self):
        if self.price > 1500:
            self.price = self.price - 0.1 * self.price
            print("10% discount is applied")
            return self.price
        else:
            print("no discount")

c1 = Product('bwf',14712)
c1.apply_discount()
print(c1.price)