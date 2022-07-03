import servers
import time
import os

from pathlib import Path
from readimage import get_captcha
from generator import password_generator, username_generator, create_and_store_a_mailbox, write_credentials_to_file, check_email
from header import titleHeader

page = 'https://www.vpngate.net/en/'

print('\x1bc')

file_path = str(Path(__file__).parent)
p=password_generator()
u=username_generator()

#open_vpn = servers.download_ovpn_config()
#connect = servers.connect_to_vpn()
tempmail = create_and_store_a_mailbox()

# Create a file of available VPNs at VPNGate
# Please comment these out if VPNGate is down, as you will need to use your own VPN/Proxies
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

configuration_number = 0

# Download Open VPN Configuration - Check Each VPN - Write Valid VPNs to file

while configuration_number < links_list:

	print('\x1bc')
	titleHeader()
	
	with open('config_files/openvpn_config_url_list','r') as urls_file:
		page_link = page + urls_file.readlines()[1]
		
	url = servers.get_ovpn_configuration_link(page_link)
	print(url)
	servers.download_config(url)
	
	print('Connecting to VPN...')
	
	if 'Error' in str(connect.set_up_nmcli_connection()):
		print('Connection Refused')
			
	if '0 received' in str(connect.ping_connection()):
		print('Connection Timed Out')
			
	else:
		print('Connection Successful. Current IP: '+ connect.fetch_IPaddr())
		with open('config_files/valid_vpn_connections','a') as valid_vpngate_connections:
			valid_vpngate_connections.write(url)
		valid_vpngate_connections.close()
		
	configuration_number +=1
	time.sleep(2)
	
	connect.delete_nmcli_connection()
	open_vpn.delete_config()
	
# Generate credentials (change 'p.generate_password' number to length of your choice)

password=p.generate_password(10)
username = u.generate_a_username()

temp_mailbox_path = file_path +'/temp_mailboxes'
credentials_path = file_path +'/credentials'
credentials_list = [username,":",password]

while True:

	if os.path.exists(temp_mailbox_path):
		break
		
	else:
		tempmail.write_mailbox_to_file()
		break

while True:

	if os.path.exists(credentials_path):
		break
		
	else:
		write_credentials_to_file(credentials_list)
		break
		
read_email_from_file = open('config_files/temp_mailboxes','r')
email = read_email_from_file.readline().split('"')[1]

with open('config_files/created_accounts','a') as accounts:
	accounts.write(username+":"+password+" --- "+email+"\n")
accounts.close()

captcha = get_captcha()
captcha.enter_signup_credentials(username, password, email)
captcha.take_browser_screenshot('config_files/my_screenshot.png')
captcha.resize_the_screenshot()
captcha_result = captcha.read_captcha_by_ocr('config_files/captcha_image.png').strip()
captcha.enter_captcha(captcha_result)


#read_email_from_file.close()
#check_email()
