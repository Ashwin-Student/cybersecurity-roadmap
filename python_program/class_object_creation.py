

class Vehicle:
    def __init__(self, brand, wheel):
        self.brand = brand
        self.wheel = wheel




    def verif(self):
        print(f"brand of an car is{self.brand} and its wheel is{self.wheel}")


v1 = Vehicle('Tata', 4)

print(v1.brand)
print(v1.wheel)
v1.verif()
