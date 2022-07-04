import requests
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver

api_endpoint = 'https://www.developermail.com/api/v1/mailbox/'
		


created_email_address = requests.put(api_endpoint, headers = {'accept': 'application/json'}).json()['result'] # Create an Email Inbox

temp_email = api_endpoint + created_email_address['name'] # Make the Inbox URL

token  = created_email_address['token'] # Get the token need to retrieve messages

parameters = {'accept': 'application/json', 'X-MailboxToken':token, 'Content-Type': 'application/json'} # Insert the token in the requests header

print(created_email_address['name']) # Fetch just the name of the temporary email (i.e. zxi-0cx)
		

# Wait for email messages 

while True:
	print('\x1bc')
	print(created_email_address['name'] + '@developermail.com')
	try:
		temp_email_domains_message_id = requests.get(temp_email, headers = parameters).json()['result']
		mail_id = str(temp_email_domains_message_id).split("'")[1]
		get_email_message = requests.get(temp_email + "/messages/" + mail_id, headers = parameters).json()['result']
		soup = bs(get_email_message, 'html.parser')
		all_links = soup.find_all(href = True)
		confirmation_link = str(all_links).split('"')[1]
		print(confirmation_link)
		break
	except (ValueError, IndexError):
		print('Waiting for Email')
		time.sleep(2)



#browser = webdriver.Chrome()
#browser.set_window_size(300,600)
#browser.get(confirmation_link)


