import requests
import shlex
import subprocess
from header import titleHeader
username = 'yourusername'
password = 'yourpassword'
email = 'youremail' #some temp-email api?

signup = 'https://windscribe.com/signup'
#page = 'https://res.windscribe.com/res/init'

# Your own credentials here --->

payload = {'signup': '1','username':username,'password':password,'password2': password,'email': email,'voucher_code': '','captcha': '','robert_status': '1','unlimited_plan': '0'}

print('\x1bc')

titleHeader()

print('-'*60)

with requests.session() as windscribe:
	
	# Your Ipvanish proxy credentials (not the same as login!) --->

	tor = {'http':'socks5h://user:pass@tor.socks.ipvanish.com:1080'}
	myip = windscribe.get('http://httpbin.org/ip', proxies = tor)
	print(myip.text)
	getHeaders = windscribe.get(signup); heads = getHeaders.headers
	post = windscribe.post(signup, data=payload)
	
	print(postCaptcha) #one day...
	
windscribe.close()
