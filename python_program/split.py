import re

name='pune,mumbai;nagpur.amravati'

result = re.split(r'[ ,;.]', name)

print(result)