import io
import pytesseract
import subprocess

from pathlib import Path
from PIL import Image
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

def read_captcha(directory):

	inputOutput = io.BytesIO()
	openImage = Image.open(directory)
	openImage.save(inputOutput, "PNG")
	inputOutput.seek(0)
	byteImg = inputOutput.read()
	dataBytesIO = io.BytesIO(byteImg)
	openImage = Image.open(dataBytesIO)
	captcha = pytesseract.image_to_string(openImage)
	
	return captcha

def resize_the_screenshot():
	screenshot_image = Image.open(r"my_screenshot.png")
	width, height = screenshot_image.size
	left = 160
	top = 350
	right = 300
	bottom = 420
	captcha_image = screenshot_image.crop((left, top, right, bottom))
	newsize = (400, 400)
	captcha_image = captcha_image.resize(newsize)
	captcha_image.save('captcha_image.png')

resize_the_screenshot()
captcha = read_captcha('captcha_image.png').strip()

print(captcha)

