class Shopping_Cart:
    def __init__(self, item_list):
        self.list1 = item_list

    def add_items(self,item_name):
        self.list1.append(item_name)


    def Display_cart(self):
             for i in self.list1:
                 print(i)

itm_list=[]
c1 = Shopping_Cart(itm_list)

c1.add_items("hfhvc")
c1.Display_cart()