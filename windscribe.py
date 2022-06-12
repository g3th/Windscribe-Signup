import requests
import shlex
import subprocess

from generator import password_generator
from generator import u_gen
from header import titleHeader

email = 'youremail' #some temp-email api?

signup = 'https://windscribe.com/signup'
#page = 'https://res.windscribe.com/res/init'

# Your own credentials here --->

print('\x1bc')

titleHeader()

print('-'*60)

p=password_generator(); u=u_gen()
password=p.gen(10); username = u.name()


payload = {'signup': '1','username':username,'password':password,'password2': password,'email': '','voucher_code': '','captcha': '','robert_status': '1','unlimited_plan': '0'}

with requests.session() as windscribe:
	
	# Your Ipvanish proxy credentials (not the same as login!) --->

	tor = {'http':'socks5h://user:pass@tor.socks.ipvanish.com:1080'}
	myip = windscribe.get('http://httpbin.org/ip', proxies = tor)
	print(myip.text)
	getHeaders = windscribe.get(signup); heads = getHeaders.headers
	post = windscribe.post(signup, data=payload)
	
	print(postCaptcha) #one day...
	
windscribe.close()
