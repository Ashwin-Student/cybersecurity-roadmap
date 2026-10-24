import re


date = '10-07-2004'


result = re.sub(r'-','/',date)

print(result)