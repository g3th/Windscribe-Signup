import requests
import time
import sys

from bs4 import BeautifulSoup as bs
from selenium import webdriver


class EmailTest:

    def __init__(self):
        self.api_endpoint = 'https://www.developermail.com/api/v1/mailbox/'
        self.temp_email = ''
        self.created_email_address = ''
        self.token = ''
        self.parameters = ''
        self.confirmation_link = ''

    def create_mail(self):
        self.created_email_address = requests.put(self.api_endpoint, headers={'accept': 'application/json'}).json()[
            'result']  # Create an Email Inbox
        self.temp_email = self.api_endpoint + self.created_email_address['name']  # Make the Inbox URL
        self.token = self.created_email_address['token']  # Get the token needed to retrieve messages
        self.parameters = {'accept': 'application/json', 'X-MailboxToken': self.token,
                           'Content-Type': 'application/json'}  # Insert the token in the requests header
        print(self.created_email_address['name'])  # Fetch just the name of the temporary email (i.e. zxi-0cx)

    # Wait for email messages
    def get_link(self):
        while True:
            print("\x1bc")
            print(self.created_email_address['name'] + '@developermail.com')
            print(self.parameters)
            try:
                temp_email_domains_message_id = requests.get(self.temp_email, headers=self.parameters).json()['result']
                mail_id = str(temp_email_domains_message_id).split("'")[1]
                get_email_message = \
                    requests.get(self.temp_email + "/messages/" + mail_id, headers=self.parameters).json()['result']
                soup = bs(get_email_message, 'html.parser')
                all_links = soup.find_all('a', href=True)
                if len(all_links) != 0:
                    for i in all_links:
                        if 'https://windscribe.com/signup/confirmemail/' in str(i):
                            # This is highly cancerous and isn't needed in the actual application
                            unparsed = str(i)
                            a = unparsed.split("3D")[2].replace("=", '').replace(" ", '').replace("style", '').replace(
                                "'", '').replace('"', '')
                            b = unparsed.split('"')[2].replace("'", '').replace(" ", '').replace("3D", '')
                            self.confirmation_link = a + "/" + b
                            print(self.confirmation_link)
                    break
            except (ValueError, IndexError):
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



email = EmailTest()
email.create_mail()
email.get_link()
# browser = webdriver.Chrome()
# browser.set_window_size(300,600)
# browser.get(confirmation_link)
