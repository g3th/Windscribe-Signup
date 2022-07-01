import io
import pytesseract
import time
import requests

from selenium import webdriver
from PIL import Image

def screenshot(user,password,email):
	
	browser = webdriver.Chrome()
	browser.set_window_size(100,100); browser.get('https://windscribe.com/signup');time.sleep(1)
	User = browser.find_element_by_xpath('//*[@id="username"]'); User.send_keys(user)
	Pass = browser.find_element_by_xpath('//*[@id="pass1"]'); Pass.send_keys(password)
	Repeat_Pass = browser.find_element_by_xpath('//*[@id="pass2"]');Repeat_Pass.send_keys(password)
	Email = browser.find_element_by_xpath('//*[@id="signup_email"]');Email.send_keys(email)
	bSubmit = browser.find_element_by_xpath('//*[@id="signup_button"]')
	bSubmit.click();time.sleep(4)
	screenshot = browser.save_screenshot('my_screenshot.png');time.sleep(2)


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
