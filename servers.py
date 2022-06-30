import os
import requests
import subprocess
import json

from pathlib import Path
from bs4 import BeautifulSoup as soup
from random import randint

configuration_download_page_links = []
page = 'https://www.vpngate.net/en/'
temp_mail_api_endpoint ='https://www.1secmail.com/api/v1/'

class download_ovpn_config:
	
	def __init__(self):

		self.vpn_gate_request = requests.get(page)
		self.parse_vpn_gate_request = soup(self.vpn_gate_request.text, 'html.parser')
		self.obtain_all_page_links = self.parse_vpn_gate_request.find_all(href = True)

	def get_all_page_links(self):

		self.all_page_links = list(self.obtain_all_page_links)
		for link in self.all_page_links:
			if 'do_openvpn.aspx' in str(link):
				configuration_download_page_links.append(str(link).split('"')[1].replace('&amp;','&'))

		return configuration_download_page_links

	def get_ovpn_configuration_link(self):

		config_download_page_links = download_ovpn_config.get_all_page_links(self)
		download_page_request = requests.get(page+configuration_download_page_links[randint(0,len(configuration_download_page_links)-1)])
		download_page_links = soup(download_page_request.text,'html.parser')
		obtain_download_page_links = download_page_links.find_all(href = True)
		ovpn_configuration_link = page[:-4] + str(obtain_download_page_links[35:36]).split('"')[1].replace('&amp;','&')
		return ovpn_configuration_link

	def download_config(self):

		download = download_ovpn_config.get_ovpn_configuration_link(self)
		parse_ovpn_configuration_link = ['wget', '-O', 'config.ovpn', '"', download, '"']		
		subprocess.run(parse_ovpn_configuration_link, shell=False, stderr= subprocess.DEVNULL, stdout=subprocess.DEVNULL)
					
class connect_to_vpn:

	def __init__(self):
	
		self.ovpn_config = ['nmcli','connection','import','type','openvpn','file', str(Path(__file__).parent)+'/config.ovpn']
		self.connect = ['nmcli','connection','up','config']
		self.delete_connection = ['nmcli','connection','delete','id','config']
				
	def set_up_nmcli_connection(self):
	
		ping_command = ['ping','-c1','8.8.8.8']	
		nmcli_add_vpn = subprocess.run (self.ovpn_config, shell = False)#, stdout = subprocess.DEVNULL, stderr = subprocess.PIPE)
		nmcli_connect_vpn = subprocess.run (self.connect, shell= False)#, stdout = subprocess.DEVNULL, stderr = subprocess.PIPE)
		ping_the_connection = subprocess.run(ping_command, shell=False)#, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		return nmcli_connect_vpn.stderr, ping_the_connection.stdout
				
	def delete_connection(self):
		
		subprocess.run(self.delete_connection, shell = False)#, stdout = subprocess.DEVNULL)
				
class create_and_store_a_mailbox:
	
	def __init__(self):
		
		self.temp_mail_api_endpoint ='https://www.1secmail.com/api/v1/'
		self.temp_mailbox_path = str(Path(__file__).parent)+'/temp_mailboxes'
		self.created_mailbox = requests.get(temp_mail_api_endpoint, params = {'action':'genRandomMailbox','count':'1'})
				
	def write_mailbox_to_file(self):
		
		with open('temp_mailboxes','a') as mailboxes:				
			self.mailbox = str(self.created_mailbox.text)
			mailboxes.write(self.mailbox+"\n")
				
	def create_mailbox(self):
		
		if os.path.exists(self.temp_mailbox_path):
			user_prompt = input ('Mailbox exists. Create another? (y/n) ')
			if user_prompt == 'y':
				create_and_store_a_mailbox.write_mailbox_to_file(self)
			else:
				pass
		else:
			create_and_store_a_mailbox.write_mailbox_to_file(self)
						
	def check_email(self):
	
		mailboxes_list = []		
		with open('temp_mailboxes','r') as fetch_mailboxes:
			for lines in fetch_mailboxes:
				mailboxes_list.append(lines)			
		for box in mailboxes_list:
			fetch_email_message_id = requests.get(temp_mail_api_endpoint, params = {'action':'getMessages','login':box.split('"')[1].split("@")[0] ,'domain': box.split('"')[1].split("@")[1]}).json()			
			email_message_id = fetch_email_message_id[0]['id']
			get_email_message = requests.get(temp_mail_api_endpoint, params = {'action':'readMessage','login':box.split('"')[1].split("@")[0] ,'domain': box.split('"')[1].split("@")[1], 'id':email_message_id}).json()			
			for lines in get_email_message['body']:
				if '<a href' in lines:
					print (lines)
