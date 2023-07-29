import requests
import time
import sys

from header import titleHeader as title
from bs4 import BeautifulSoup as bs
from selenium import webdriver


class confirmation_email:

    def __init__(self):

        self.api_endpoint = 'https://www.developermail.com/api/v1/mailbox/'
        self.temp_email = ''
        self.parameters = ''
        self.confirmation_link = ''
        self.created_email_address = ''
        self.token = ''
        self.wait_counter = 0

    def create_an_email_address(self):
        print("Contacting Temp Email API endpoint")
        self.created_email_address = requests.put(self.api_endpoint, headers={'accept': 'application/json'}).json()[
            'result']
        self.temp_email = self.api_endpoint + self.created_email_address['name']
        self.token = self.created_email_address['token']
        self.parameters = {'accept': 'application/json', 'X-MailboxToken': self.token,'Content-Type': 'application/json'}
        print("Email created successfully")
        return self.created_email_address['name']

    def get_confirmation_link_email(self):
        while True:
            if self.wait_counter > 10:
                print("Something went wrong. Reloading.")
                time.sleep(3)
                break
            title()
            try:
                temp_mail_domains_message_id = requests.get(self.temp_email, headers=self.parameters).json()['result']
                mail_id = str(temp_mail_domains_message_id).split("'")[1]
                get_email_message = requests.get(self.temp_email + "/messages/" + mail_id, headers=self.parameters).json()['result']
                soup = bs(get_email_message, 'html.parser')
                all_links = soup.find_all('a', href=True)
                if len(all_links) != 0:
                    self.confirmation_link = str(all_links).split('"')[1].split('"')[0]
                    break
            except (ValueError, IndexError):
                self.wait_counter += 1
                print('Waiting for Email', end='')
                sys.stdout.flush()
                time.sleep(1)
                print('.', end='')
                sys.stdout.flush()
                time.sleep(1)
                print('.', end='')
                sys.stdout.flush()
                time.sleep(1)
                print('.', end='')
                sys.stdout.flush()
                time.sleep(1)

    def click_confirmation_link(self):
        browser = webdriver.Chrome()
        browser.set_window_size(300, 600)
        browser.get(self.confirmation_link)
        time.sleep(3)
        browser.close()
