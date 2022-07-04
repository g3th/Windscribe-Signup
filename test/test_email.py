import requests

from bs4 import BeautifulSoup as bs
from selenium import webdriver

temp_mail = 'https://www.developermail.com/api/v1/mailbox/'



parameters = {'accept': 'application/json', 'X-MailboxToken':'85E4D5C1506886DC5A4434186F770AB3C79FA67B', 'Content-Type': 'application/json'}

message_id = []

temp_mail_domains_message_id = requests.get(temp_mail, headers = parameters).json()['result']

while True:

	try:
	
		print('Checking for Emails')
		mail_id = str(temp_mail_domains_message_id).split("'")[1]
		get_email_message = requests.get(temp_mail + "/messages/" + mail_id, headers = parameters).json()['result']
		soup = bs(get_email_message, 'html.parser')
		all_links = soup.find_all(href = True)
		print(all_links)
		break
				
	except (ValueError, IndexError):
		time.sleep(1)

#confirmation_link = str(all_links).split('"')[1]

#browser = webdriver.Chrome()
#browser.set_window_size(300,600)
#browser.get(confirmation_link)


