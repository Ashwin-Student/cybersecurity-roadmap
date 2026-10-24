

main_tupple=()
i=0
tup=()

while(i<3):
    name = input("enter the product_name:",)
    price=float(input("enter the price:",))

    tup= (name,price)
    main_tupple+=(tup,)
    i += 1

for p in main_tupple:
    if p[1] > 500:
        print(f"product name abive 500 is{p[0]}")




