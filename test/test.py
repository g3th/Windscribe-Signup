
import subprocess

from pathlib import Path

def time_out():

	while True:

		nmcli_start = subprocess.run ((b), shell = False, stderr = subprocess.PIPE)
		if 'Error' in str(nmcli_start.stderr):
			print('Refused')
		else:
			break
			
def string_test():
	page ='https://www.vpngate.net/common/openvpn_download.aspx?sid=1656540301538&udp=1&host=vpn656988361.opengw.net&port=1341&hid=15681914&/vpngate_vpn656988361.opengw.net_udp_1341.ovpn'

	print(page.split('=')[3].split('&')[0])
	print(page.split('&')[3])
	
def test_list_because_strager_banned_me_from_shlex():

	ovpn_config = ['nmcli','connection','import','type','openvpn','file', str(Path(__file__).parents[1])+'/config.ovpn']
	print(ovpn_config)
	nmcli_add_vpn = subprocess.run (ovpn_config, shell = False)



