import servers
import time
import os
import shutil

from bs4 import BeautifulSoup as soup
from selenium import webdriver
from random import randint
from pathlib import Path
from readimage import get_captcha
from generator import password_generator, username_generator, write_credentials_to_file
from header import titleHeader
from email_confirmation import confirmation_email

page = 'https://www.vpngate.net/en/'

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
		links_list = len(existing_urls.readlines())-1
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
		page_link = page + urls_file.readlines()[randint(0,links_list-1)]
		
	url = servers.get_ovpn_configuration_link(page_link)
	servers.download_config(url)
	urls_file.close()
	
	print('Connecting to VPN...')
	
	if 'Error' in str(connect.set_up_nmcli_connection()):
		print('Connection Refused'); time.sleep(1);flag = 1
			
	if '0 received' in str(connect.ping_connection()):
		print('Connection Timed Out'); time.sleep(1);flag = 1
	
	elif flag == 0:
		print('Connection Successful. Current IP: '+ connect.fetch_IPaddr())
		
		# Generate credentials (change 'p.generate_password' number to length of your choice)

		password=p.generate_password(10)
		username = u.generate_a_username()

		credentials_path = file_path +'/credentials'
		credentials_list = [username,":",password]		
		
		email = str(tempmail.create_an_email_address())+'@developermail.com'
		write_credentials_to_file(username, password, email)
		
		# Start browser, generate + input and write credentials to file
		# Take a screenshot, crop the screenshot, read the captcha with Tesseract
		# Return the captcha string, and enter it in browser
		
		captcha = get_captcha()
		captcha.enter_signup_credentials(username, password, email)
		
		try:
			abuse = soup.find('div',{'class':'content_message error'})
			if 'Abuse detected' in abuse:
				captcha.close_browser_on_error()
				break
		except:
			captcha.take_browser_screenshot('config_files/my_screenshot.png')
			captcha.resize_the_screenshot()
			captcha_result = captcha.read_captcha_by_ocr('config_files/captcha_image.png').strip()
			captcha.enter_captcha(captcha_result)
			tempmail.get_confirmation_link_email()
			tempmail.click_confirmation_link()

			number_of_created_accounts +=1
		connect.delete_nmcli_connection()
		open_vpn.delete_config()
