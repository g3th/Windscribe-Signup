import io
import pytesseract
import time
import requests
import os


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from PIL import Image

return_error_message = False

class registration_process:

	def __init__(self):
		
		self.browser = webdriver.Firefox()
		self.browser.set_window_size(100,550)
		self.browser.get('https://windscribe.com/signup')
		self.inputOutput = io.BytesIO()
		self.bSubmit = self.browser.find_element_by_xpath('//*[@id="signup_button"]')
		
	def enter_signup_credentials(self,user, password, email):
	
		time.sleep(2)
		User = self.browser.find_element_by_xpath('//*[@id="username"]')
		User.send_keys(user)
	
		Pass = self.browser.find_element_by_xpath('//*[@id="pass1"]')
		Pass.send_keys(password)
	
		Repeat_Pass = self.browser.find_element_by_xpath('//*[@id="pass2"]')
		Repeat_Pass.send_keys(password)
	
		Email = self.browser.find_element_by_xpath('//*[@id="signup_email"]')
		Email.send_keys(email)	
		self.bSubmit.click()
		time.sleep(2)
	def take_browser_screenshot(self, directory):
				
		scroll_to_captcha_image = self.browser.find_element_by_xpath('//*[@id="captcha_img"]')
		scrolling = ActionChains(self.browser)
		scrolling.move_to_element(scroll_to_captcha_image)
		screenshot = self.browser.save_screenshot(directory)
			
	def resize_the_screenshot(self):
		
		screenshot_image = Image.open(r"config_files/my_screenshot.png")
		width, height = screenshot_image.size
		left = 160; right = 340
		top = 350; bottom = 530		
		captcha_image = screenshot_image.crop((left, top, right, bottom))
		newsize = (400, 400)
		captcha_image = captcha_image.resize(newsize)
		captcha_image.save('config_files/captcha_image.png')
		
	def read_captcha_by_ocr(self, directory):
		
		openImage = Image.open(directory)
		openImage.save(self.inputOutput, "PNG")
		self.inputOutput.seek(0)
		byteImg = self.inputOutput.read()
		dataBytesIO = io.BytesIO(byteImg)
		openImage = Image.open(dataBytesIO)
		captcha = pytesseract.image_to_string(openImage)
		return captcha
		
	def enter_captcha(self, captcha_value):
		return_error_message = False
		captcha_input_box = self.browser.find_element_by_xpath('//*[@id="captcha1"]')
		captcha_input_box.send_keys(captcha_value)
		self.bSubmit.click()
		while True:	
			try:			
				error_message_xpath = self.browser.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/form/div[1]')
				error_message_text = error_message_xpath.text	
				if 'Wrong captcha supplied' in error_message_text:				
					return_error_message = True
					time.sleep(2)
					break				 		
			except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
				break
					
		return return_error_message
	
	def delete_all_screenshots(self, original, cropped):
	
		os.remove(original)
		os.remove(cropped)
		
	def close_browser(self):

		self.browser.close()
	
