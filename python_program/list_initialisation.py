


vehicle_list=['tractor','cycle','car','bike','scooter']


vehicle=input("Enter your vehicle type:")

for index,item in enumerate(vehicle_list):
    if  item == vehicle:
        vehicle_list[index] = 'Electric Vehicle'
        break
else:
    print("Not found")
 #   elif item != vehicle:

print(vehicle_list)
