import servers

from pathlib import Path
from readimage import screenshot, ocr
from generator import password_generator, u_gen
from header import titleHeader

email = 'youremail'
signup = 'https://windscribe.com/signup'
captcha = 'https://windscribe.com/captcha/'

# Change 'p.gen' number to a password length of your choice --->

print('\x1bc')

titleHeader()
p=password_generator()
u=u_gen()
password=p.gen(10)
username = u.name()
open_vpn = servers.download_ovpn_config()
connect = servers.connect_to_vpn()

print('Connecting to VPN: ' + open_vpn.get_ovpn_configuration_link().split('=')[3].split('&')[0] + " on " + open_vpn.get_ovpn_configuration_link().split('&')[3].replace('=',':'))

while True:

	open_vpn.download_config()
	connect.set_up_nmcli_connection()
	error_checking = str(connect.set_up_nmcli_connection())
	ping_packet_loss_check = str(connect.set_up_nmcli_connection()[1])
		
	if 'Error' in error_checking:
		print('Connection Refused')
		connect.delete_connection()
		
	elif '0 received' in ping_packet_loss_check:
		print('Connection Timed Out')
		connect.delete_connection()
	else:
		print('Connection is Working')
		break

