import requests
import subprocess
import concurrent.futures

from bs4 import BeautifulSoup as soup

configuration_download_page_links = []
vpngate = 'https://www.vpngate.net/en/'

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

def get_ovpn_configuration_link(page_link):

	config_download_page_links = page_link
	download_page_request = requests.get(config_download_page_links)
	download_page_links = soup(download_page_request.text,'html.parser')
	obtain_download_page_links = download_page_links.find_all(href = True)
	ovpn_configuration_link = page[:-4] + str(obtain_download_page_links[35:36]).split('"')[1].replace('&amp;','&')
	return ovpn_configuration_link

def scrape_download_links_list(config_link):
	downloading_links_list=[]
	with open('openvpn_config_url_list', 'r') as downloading_links:
		for link in downloading_links.readlines():
			downloading_links_list.append(config_link(link))
	downloading_links.close()
	return download_links_list

def download_config(config_url,file_number):
	download = config_url
	fetch_configuration_file_bytes = requests.get(config_url).content
	with open('config'+str(file_number)+'.ovpn','wb') as open_vpn_file:
		open_vpn_file.write(fetch_configuration_file_bytes)


page = 'https://www.vpngate.net/en/'

links_list = download_ovpn_config()

downloading_links_list=[]

futures_list = []
downloading_urls = []
configuration_number = 1
with concurrent.futures.ThreadPoolExecutor() as executor:

	with open('openvpn_config_url_list','a') as openvpn_urls:
		for link in links_list.get_all_page_links():
			executor.map(openvpn_urls.write, vpngate+link+"\n")
			
	with open('openvpn_config_url_list','r') as configs:
		for line in configs.readlines():
			thread = executor.submit(get_ovpn_configuration_link, line)
			futures_list.append(thread)
			
		for returned_value in futures_list:
			result = returned_value.result()
			downloading_urls.append(result)
			
		for url in downloading_urls:
			executor.submit(download_config, url, str(configuration_number))
			configuration_number +=1



			

#download_config('openvpn_config_url_list')
