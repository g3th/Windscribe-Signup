import io
import pytesseract
import time
import requests

from selenium import webdriver
from PIL import Image

def screenshot(user,password,email):
	chrome_options = webdriver.ChromeOptions()
	browser = webdriver.Chrome()
	browser.set_window_size(200,740); browser.get('https://windscribe.com/signup');time.sleep(1)
	User = browser.find_element_by_xpath('//*[@id="username"]'); User.send_keys(user)
	Pass = browser.find_element_by_xpath('//*[@id="pass1"]'); Pass.send_keys(password)
	Mail = browser.find_element_by_xpath('//*[@id="pass2"]'); Mail.send_keys(email)
	bSubmit = browser.find_element_by_xpath('//*[@id="signup_button"]')
	bSubmit.click();time.sleep(4)
	screenshot = browser.save_screenshot('my_screenshot.png');time.sleep(2)
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




