import os
import requests
import subprocess
import shlex
import json
from pathlib import Path
from bs4 import BeautifulSoup as soup
from random import randint

configuration_download_page_links = []
page = 'https://www.vpngate.net/en/'

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
			parse_ovpn_configuration_link = shlex.split('wget -O config.ovpn "'+ download +'"')
			subprocess.run((parse_ovpn_configuration_link), shell=False, stderr= subprocess.DEVNULL, stdout=subprocess.DEVNULL)
			
class connect_to_vpn:

			def __init__(self):
				
				self.ovpn_config = shlex.split ('nmcli connection import type openvpn file ' + str(Path(__file__).parent) + '/config.ovpn')
				self.connect = shlex.split('nmcli connection up config')
				self.delete_connection = shlex.split('nmcli connection delete id config')				
			def set_up_nmcli_connection(self):
			
				try:
					subprocess.run ((self.ovpn_config), shell = False, stdout = subprocess.DEVNULL)
					subprocess.run ((self.connect), shell= False, stdout = subprocess.DEVNULL)				
				except:
					print("Error")
					
			def delete_connection(self):
				
				subprocess.run((self.delete_connection), shell = False, stdout = subprocess.DEVNULL)

temp_mail_api_endpoint ='https://www.1secmail.com/api/v1/'

created_mailbox = requests.get(temp_mail_api_endpoint, params = {'action':'genRandomMailbox','count':'1'})

mailbox_login = str(created_mailbox.text).split('"')[1].split("@")[0]
mailbox_domain = str(created_mailbox.text).split('"')[1].split("@")[1]
				
get_email_messages = requests.get(temp_mail_api_endpoint, params = {'action':'getMessages','login': mailbox_login,'domain': mailbox_domain})

print(get_email_messages.content)

#request_mail = requests.get(page, params = {'action':'readMessage','login':'m1dq7xugccn','domain':'1secmail.com','id':'216467055'}).json()

#print(json.dumps(request_mail,indent=2))







