import os
import requests
import subprocess
import shlex

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
		
			parse_ovpn_configuration_link = shlex.split('wget -O config.ovpn "'+self.ovpn_configuration_link+'"')
			subprocess.run((parse_ovpn_configuration_link), shell=False, stderr= subprocess.DEVNULL, stdout=subprocess.DEVNULL)

start = download_ovpn_config()

print(start.get_ovpn_configuration_link())
