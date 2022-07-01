import os
import requests
import subprocess
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
		print('Downloading Open VPN config file...')
		download = download_ovpn_config.get_ovpn_configuration_link(self)
		parse_ovpn_configuration_link = ['wget', '-O', 'config.ovpn', '"', download, '"']		
		subprocess.run(parse_ovpn_configuration_link, shell=False, stderr= subprocess.DEVNULL, stdout=subprocess.DEVNULL)
		
	def delete_config(self):
		
		os.remove('config.ovpn')
					
class connect_to_vpn:

	def __init__(self):
	
		self.ovpn_config = ['nmcli','connection','import','type','openvpn','file', str(Path(__file__).parent)+'/config.ovpn']
		self.connect = ['nmcli','connection','up','config']
		self.delete_connection = ['nmcli','connection','delete','id','config']
				
	def set_up_nmcli_connection(self):
			
		nmcli_add_vpn = subprocess.run (self.ovpn_config, shell = False)
		nmcli_connect_vpn = subprocess.run (self.connect, shell= False, stdout = subprocess.PIPE, stderr = subprocess.PIPE)	
		return nmcli_connect_vpn.stderr
		
	def ping_connection(self):
	
		ping_command = ['ping','-c1','8.8.8.8']	
		ping_the_connection = subprocess.run(ping_command, shell=False, stdout=subprocess.PIPE)
		
		return ping_the_connection.stdout
		
	def fetch_IPaddr(self):
	
		fetch_current_ip_address = requests.get('http://httpbin.org/ip')
		human_readable_ip_address = fetch_current_ip_address.text.split('"')[3].strip(" ")
		
		return human_readable_ip_address
		
	def delete_nmcli_connection(self):
		
		subprocess.run(self.delete_connection, shell = False)#, stdout = subprocess.DEVNULL)
