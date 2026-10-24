grocery_items = {'Rice':100,'Wheat':200,'Bajra':100,'dal':154,'chana':215}

def des(p):
    discount = p - 0.1 * p
    return discount

for product, price in grocery_items.items():
    if price > 100:
        print(f"10% discount is applied on your prodcut{product}")
        grocery_items[product] = des(price)


print(grocery_items)        