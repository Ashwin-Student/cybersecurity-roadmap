cities_tuple=('pune','mumbai','nagpur','nashik')

cities_list = list(cities_tuple)


for index,city in enumerate(cities_list):
    if city == 'mumbai':
        cities_list[index] = 'thane'

cities_tuple2=tuple(cities_list)
print(cities_tuple2)