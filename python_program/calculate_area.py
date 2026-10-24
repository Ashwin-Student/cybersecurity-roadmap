def calculate_area(length, width):
    if length == width:
        print("Area of the Square is ",length ** 2)
    else:
        print("Area of rectangle is ",  length * width)




len=int(input("Enter the length:"))
wid=int(input("Enter the width:"))
calculate_area(len,wid)


