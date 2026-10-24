list = [3.14, 34, 'Ashwin',42]
int_l=[]
fl=[]
st=[]

for item in list:
    t = type(item)
    if t == int:
        int_l+=[item]
    elif t == float:
        fl+=[item]
    elif t == str:
        st+=[item]
    else:
        print("list is not avaliable for this type")

print(int_l)
print(fl)
print(st)