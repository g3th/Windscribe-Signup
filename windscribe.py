import servers

from pathlib import Path
from readimage import screenshot, ocr
from generator import password_generator, u_gen
from header import titleHeader

email = 'youremail'
signup = 'https://windscribe.com/signup'
captcha = 'https://windscribe.com/captcha/'


# Change 'p.gen' number to a password length of your choice --->

print('\x1bc'); titleHeader()

p=password_generator(); u=u_gen()
password=p.gen(10); username = u.name()

screenshot(username, password, email)
print(ocr(str(Path(__file__).parent)+'/my_screenshot.png'))


