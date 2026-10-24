import re

sen = input("enter the sentence :")
result = re.search("abc", sen)

if result:
    print("Exits")
else:
    print("Not exits.")