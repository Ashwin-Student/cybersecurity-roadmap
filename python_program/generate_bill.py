
total_cost=0
def generate_bill(item_name, price, tax_rate=18):
    '''if tax_rate == '':
        tax_rate = 18
    else:
        tax_rate = float(tax_rate)'''
    total_cost = price + (tax_rate / 100) * price

    return total_cost

'''list_name=[]
list_pr=[]
list_tx=[]

for i in range(0,3):
    name = input("Enter the name of item:")
    pr = float(input("Enter the price of product"))
    tx=input("Enter the tax")
    list_name+=[name]
    list_pr+=[pr]
    list_tx+=[tx]

for j in range(0,3):
 total_amount=generate_bill(list_name[j],list_pr[j],list_tx[j])
 print(f"Total amount{total_amount}")'''

for i in range(3):
    print("Total bill:",generate_bill("A", 20))
    print(generate_bill("b", 100, 5))
    print(generate_bill("c", 33, 22))
    break

