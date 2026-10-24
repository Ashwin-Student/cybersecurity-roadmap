import re


web_list = [
    'https://www.acts.cdac.in',
    'https://www.firewall.com'
]

for web in web_list:

    result = re.search(r'www\.(.*)', web)

    if result:

        print(result.group(1))
