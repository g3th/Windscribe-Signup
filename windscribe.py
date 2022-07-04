import servers
import time
import os
import shutil

from header import titleHeader
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from random import randint
from pathlib import Path
from generator import password_generator, username_generator, write_credentials_to_file
from registration import registration_process
from email_confirmation import confirmation_email

vpngate = 'https://www.vpngate.net/en/'
browser_screenshot_file_path = 'config_files/my_screenshot.png'
captcha_screenshot_file_path = 'config_files/captcha_image.png'

print('\x1bc')

file_path = str(Path(__file__).parent)
p=password_generator()
u=username_generator()

open_vpn = servers.download_ovpn_config()
connect = servers.connect_to_vpn()
tempmail = confirmation_email()


# Check valid VPN Gate Addresses
# Please comment these out if VPN Gate is down, as you will need to use your own VPN/Proxies
# in order to avoid Cloudflare IUAM block.

while True:
	
	if os.path.exists(file_path+'/config_files/openvpn_config_url_list'):
		existing_urls = open('config_files/openvpn_config_url_list','r')
		links_list = len(existing_urls.readlines())
		existing_urls.close()
		break
	else:
		links_list = open_vpn.get_all_page_links()
		with open('config_files/openvpn_config_url_list','a') as openvpn_urls:
			for link in links_list:
				openvpn_urls.write(link+"\n")
		openvpn_urls.close()
		links_list = len(links_list)
		break

number_of_created_accounts = 0

# Check Valid VPN, Connect, Create Accounts

while number_of_created_accounts < 5:

	flag = 0
	
	print('\x1bc')
	titleHeader()
	
	with open('config_files/openvpn_config_url_list','r') as urls_file:
		page_link = vpngate + urls_file.readlines()[randint(0 , links_list-1)]
		
	url = servers.get_ovpn_configuration_link(page_link)
	servers.download_config(url)
	urls_file.close()
	
	print('Connecting to VPN...')
	
	if 'Error' in str(connect.set_up_nmcli_connection()):
		print('Connection Refused'); time.sleep(1); flag = 1
			
	if '0 received' in str(connect.ping_connection()):
		print('Connection Timed Out'); time.sleep(1); flag = 1
	
	elif flag == 0:
	
		try:
			
			print('Connection Successful. Current IP: '+ connect.fetch_IPaddr())
			
			# Generate credentials (change 'p.generate_password' number to length of your choice)
			
			username = u.generate_a_username()
			password = p.generate_password(10)		
			email = str(tempmail.create_an_email_address())+'@developermail.com'
			
			write_credentials_to_file(username, password, email)
			
			# Start browser, generate + input and write credentials to file
			# Take a screenshot, crop the screenshot, read the captcha with Tesseract
			# Return the captcha string, and enter it in browser
			
			registration = registration_process()
			
			registration.enter_signup_credentials(username, password, email)
			registration.take_browser_screenshot(browser_screenshot_file_path)
			registration.resize_the_screenshot()
			captcha_result = registration.read_captcha_by_ocr(captcha_screenshot_file_path).strip()
			registration.enter_captcha(captcha_result)
			tempmail.get_confirmation_link_email()
			tempmail.click_confirmation_link()
			registration.delete_all_screenshots(browser_screenshot_file_path, captcha_screenshot_file_path)
			number_of_created_accounts +=1
			registration.close_browser()
		
		except (NoSuchElementException, ElementNotInteractableException):
		
			print('Abuse Detected/IAUM, Closing Browser, Changing VPN...')
			time.sleep(3)
			registration.close_browser()

	connect.delete_nmcli_connection()
	open_vpn.delete_config()
