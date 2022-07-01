import servers
import time
import os

from pathlib import Path
from readimage import screenshot, ocr
from generator import password_generator, username_generator, create_and_store_a_mailbox, write_credentials_to_file, check_email
from header import titleHeader

# Change 'p.gen' number to a password length of your choice --->

print('\x1bc')

file_path = str(Path(__file__).parent)

titleHeader()
p=password_generator()
u=username_generator()
open_vpn = servers.download_ovpn_config()
connect = servers.connect_to_vpn()
tempmail = create_and_store_a_mailbox()

while True:

	if os.path.exists(file_path + "/config.ovpn"):
		break
	else:
		open_vpn.download_config()
		print('Connecting to VPN...')
		if 'Error' in str(connect.set_up_nmcli_connection()):
			print('Connection Refused')
			connect.delete_nmcli_connection()
			open_vpn.delete_config()
		
	
		if '0 received' in str(connect.ping_connection()):
			print('Connection Timed Out')
			connect.delete_nmcli_connection()
			open_vpn.delete_config()

		else:
			print('Connection Successful. Current IP: '+ connect.fetch_IPaddr())
			break

password=p.generate_password(10)
username = u.generate_a_username()
email = read_email_from_file.readline().split('"')[1]
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

read_email_from_file = open('temp_mailboxes','r')
read_email_from_file.close()
check_email()

screenshot(username, password, email)

