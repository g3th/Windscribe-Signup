import requests
import shlex
import subprocess

from readimage import screenshot, ocr
from servers import pickACard
from generator import password_generator, u_gen
from header import titleHeader

email = 'youremail' ; signup = 'https://windscribe.com/signup'; captcha = 'https://windscribe.com/captcha/'
#page = 'https://res.windscribe.com/res/init'

# Change 'p.gen' number to a password length of your choice --->

print('\x1bc'); titleHeader()

p=password_generator(); u=u_gen()
password=p.gen(10); username = u.name()

payload = {'signup': '1','username':username,'password':password,'password2': password,'email': '','voucher_code': '','captcha': '','robert_status': '1','unlimited_plan': '0'}

with requests.session() as windscribe:
	
	# Your Ipvanish proxy credentials (not the same as login!) --->

	 
	myip = windscribe.get('http://httpbin.org/ip')
	print('\033[38;5;236mUsername: \033[38;5;242m'+username+" \033[38;5;236m| Password: \033[38;5;242m"+password+"\033[38;5;236m | "+ "IP ----> \033[38;5;242m", myip.text.split('"')[3],"\n")
	#getHeaders = windscribe.post(signup); heads = getHeaders.headers
	#print(heads['user-agent'])
	post = windscribe.post(signup,data=payload)
	print(post.text)
	preCaptcha = post.text.split('/')[2].strip('"}')
	screenshot(preCaptcha)
	#subprocess.run(shlex.split('wget --output-file=view.png "'+'https://windscribe.com/captcha/'+preCaptcha+'"'),shell=False)	
	#subprocess.run('
	#print(postCaptcha) one day...
	
windscribe.close()
