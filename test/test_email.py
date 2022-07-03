from bs4 import BeautifulSoup as bs

import requests


temp_mail = 'https://temporarymail.com/'

request = requests.post(temp_mail)
soup = bs(request.text, 'html.parser')

find = soup.find_all("div", class_="padding-top-10 emailInput")

print(find)

