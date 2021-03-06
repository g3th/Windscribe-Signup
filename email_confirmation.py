import requests
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver

class confirmation_email:

	def __init__(self):
		
		self.api_endpoint = 'https://www.developermail.com/api/v1/mailbox/'
		
	def create_an_email_address(self):

		self.created_email_address = requests.put(self.api_endpoint, headers = {'accept': 'application/json'}).json()['result']
		self.temp_email = self.api_endpoint + self.created_email_address['name']
		self.token  = self.created_email_address['token']
		self.parameters = {'accept': 'application/json', 'X-MailboxToken':self.token, 'Content-Type': 'application/json'}
		
		return self.created_email_address['name']
		
	def get_confirmation_link_email(self):
	
		while True:
			
			try:

				temp_mail_domains_message_id = requests.get(self.temp_email, headers = self.parameters).json()['result']
				mail_id = str(temp_mail_domains_message_id).split("'")[1]
				get_email_message = requests.get(self.temp_email + "/messages/" + mail_id, headers = self.parameters).json()['result']
				soup = bs(get_email_message, 'html.parser')
				all_links = soup.find_all(href = True)
				self.confirmation_link = str(all_links).split('"')[1]
				break
				
			except (ValueError, IndexError):
				print('Waiting for Email')
				time.sleep(2)

		
	def click_confirmation_link(self):
	
		browser = webdriver.Chrome()
		browser.set_window_size(300,600)
		browser.get(self.confirmation_link);time.sleep(3)
		browser.close()
