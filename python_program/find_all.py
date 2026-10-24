import re

sen = '''I am Ashwin Debare and I am Pursuing CDAC ITISS course. My phnone no is +91-3265756483
       and my freind is also there whos phne no is +91-3727783428'''

# re.findall automatically extracts all matches into a list
list1 = re.findall(r'\d{10}', sen)

print(list1)
