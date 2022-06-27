import io
import pytesseract
import time
import requests

from selenium import webdriver
from PIL import Image

def screenshot():
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('
	browser = webdriver.Chrome()
	browser.set_window_size(200,240); browser.get('https://windscribe.com/signup');time.sleep(1)
	User = browser.find_element_by_xpath('//*[@id="generate_username"]'); User.click()
	Pass = browser.find_element_by_xpath('//*[@id="generate_password"]'); Pass.click()
	Mail = browser.find_element_by_xpath('//*[@id="signup_email"]'); Mail.send_keys("myemail@email.com")
	bSubmit = browser.find_element_by_xpath('//*[@id="signup_button"]'); bSubmit.click();time.sleep(1)
	screenshot = browser.save_screenshot('my_screenshot.png');time.sleep(2000)
	#driver.quit()

def ocr(directory):

	inputOutput = io.BytesIO()
	openImage = Image.open(directory)
	openImage.save(inputOutput, "PNG")
	inputOutput.seek(0)
	byteImg = inputOutput.read()
	dataBytesIO = io.BytesIO(byteImg)
	openImage = Image.open(dataBytesIO)
	captcha = pytesseract.image_to_string(openImage)
	return captcha

screenshot()
#screenshot('https://windscribe.com/captcha/view?_CAPTCHA&amp;t=0.10549100+1655141582')


