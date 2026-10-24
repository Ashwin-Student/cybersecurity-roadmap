import re

list1 = ['employee@10company.in', 'admin@portal.com']
for i in list1:

    result = re.search(r'([^@]+)@', i)
    if result:
        print(result.group(1))
