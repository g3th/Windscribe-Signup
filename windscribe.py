#!/usr/bin/python3

import servers
import time
import os
import requests
import shutil
import concurrent.futures

from header import titleHeader
from bs4 import BeautifulSoup as soup
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, InvalidSessionIdException
from random import randint
from pathlib import Path
from generator import password_generator, username_generator, write_credentials_to_file
from registration import registration_process
from email_confirmation import confirmation_email

vpngate = 'https://www.vpngate.net/en/'
browser_screenshot_file_path = 'config_files/my_screenshot.png'
captcha_screenshot_file_path = 'config_files/captcha_image.png'
file_path = str(Path(__file__).parent)
p=password_generator()
u=username_generator()
connect = servers.connect_to_vpn()
open_vpn = servers.download_ovpn_config()
tempmail = confirmation_email()

if __name__ == '__main__':

	downloading_links_list=[]
	futures_list = []
	downloading_urls = []
	configuration_number = 1
		
	titleHeader()

	shutil.rmtree(file_path + '/config_files')
	os.makedirs(file_path + '/config_files')

	with open('config_files/openvpn_config_url_list','a') as openvpn_urls:
		print('Scraping Web Pages directing to OVPN.config-download-pages')
		for link in open_vpn.get_all_page_links():
			openvpn_urls.write(vpngate + link + "\n")
	openvpn_urls.close()
		
	with concurrent.futures.ThreadPoolExecutor() as executor:						
			with open('config_files/openvpn_config_url_list','r') as configs:
				
				for line in configs.readlines():
					thread = executor.submit(servers.get_ovpn_configuration_link, line)
					futures_list.append(thread)
					
				print('Creating OVPN.config download pages list')	
				
				for returned_value in futures_list:
					result = returned_value.result()
					downloading_urls.append(result)
					
				print('Downloading OVPN configuration files')
					
				for url in downloading_urls:
					executor.submit(servers.download_config, url, str(configuration_number))
					configuration_number += 1

	index = 10 # Start Index at chosen location (i.e. index = 40), as long as not exceeding number of total downloaded vpn configs
	number_of_created_accounts = 0

	while number_of_created_accounts < 5:

		flag = 0
		titleHeader()	
		print('Connecting to VPN...')		
		if 'Error' in str(connect.set_up_nmcli_connection(index)):
			print('Connection Refused'); time.sleep(0.5); flag = 1				
		if '0 received' in str(connect.ping_connection()):
			print('Connection Timed Out'); time.sleep(0.5); flag = 1
		
		elif flag == 0:
			print('Connection Successful. Current IP: {}'.format(connect.fetch_IPaddr()[0] + ' - City: ' + connect.fetch_IPaddr()[1]))
			try:
			
				registration = registration_process()			
				username = u.generate_a_username()
				password = p.generate_password(10)		
				email = str(tempmail.create_an_email_address())+'@developermail.com'				
				registration.enter_signup_credentials(username, password, email)
				time.sleep(2)
				registration.take_browser_screenshot(browser_screenshot_file_path)
				registration.resize_the_screenshot()
				captcha_result = registration.read_captcha_by_ocr(captcha_screenshot_file_path).strip()
				
				if registration.enter_captcha(captcha_result) == True:
					print('Tesseract read it wrong, restarting...')
					registration.close_browser()
					
				else:
					tempmail.get_confirmation_link_email()	
					tempmail.click_confirmation_link()
					registration.delete_all_screenshots(browser_screenshot_file_path, captcha_screenshot_file_path)		
					write_credentials_to_file(username, password, email)
					registration.close_browser()
					number_of_created_accounts +=1
					
			except (NoSuchElementException, ElementNotInteractableException):				
				print('Abuse Detected/IUAM or Connection aborted \nClosing Browser, Changing VPN...')			
		
		index +=1
		connect.delete_nmcli_connection()
		connect.delete_list_elements()
