import re

v_no = [
    'MH12AB1234',
    'MH12CD5678',
    'KA12EF1234',
    'RJ12XY1234',
    'MH12YZ1234'
]

for no in v_no:
    result = re.match('^MH', no)
    if result:
        print(no)



