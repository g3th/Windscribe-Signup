import io
import pytesseract
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from PIL import Image

class registration_process:

	def __init__(self):

		self.browser_options = Options()
		self.browser_options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.browser = webdriver.Chrome(options=self.browser_options)
		self.browser.set_window_size(100,550)
		self.browser.get('https://windscribe.com/signup')
		self.inputOutput = io.BytesIO()
		self.bSubmit = self.browser.find_element(By.XPATH,'//*[@id="signup_button"]')
		
	def enter_signup_credentials(self,user, password, email):
		User = self.browser.find_element(By.XPATH,'//*[@id="username"]')
		User.send_keys(user)
		Pass = self.browser.find_element(By.XPATH,'//*[@id="pass1"]')
		Pass.send_keys(password)
		Repeat_Pass = self.browser.find_element(By.XPATH,'//*[@id="pass2"]')
		Repeat_Pass.send_keys(password)
		Email = self.browser.find_element(By.XPATH,'//*[@id="signup_email"]')
		Email.send_keys(email)
		self.bSubmit.click()
		if self.browser.find_elements(By.XPATH,'//*[@id="signupform"]/div[1]'):
			abuse_detected = self.browser.find_element(By.XPATH,'//*[@id="signupform"]/div[1]').text
			if 'Abuse' in abuse_detected:
				print("Cloudflare anti-abuse measure.\n Please change your VPN, or restart using OVPN connections.")
				time.sleep(3)
		time.sleep(2)
	def take_browser_screenshot(self, directory):
		scroll_to_captcha_image = self.browser.find_element(By.XPATH,'//*[@id="captcha2_img"]')
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
		captcha_input_box = self.browser.find_element(By.XPATH,'/html/body/div[1]/div[3]/div/div/form/div[2]/input[7]')
		captcha_input_box.send_keys(captcha_value)
		time.sleep(2)
		self.bSubmit.click()
		print("Submitting captcha")
		time.sleep(3)
		try:
			if self.browser.find_elements(By.XPATH,'/html/body/div[1]/div[3]/div/div/form/div[1]'):
				error_message_text = self.browser.find_element(By.XPATH,'/html/body/div[1]/div[3]/div/div/form/div[1]').text
				if 'Wrong captcha supplied' in error_message_text:
					return_error_message = True
					time.sleep(2)
		except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
			print("Captcha Error")
					
		return return_error_message
	
	def delete_all_screenshots(self, original, cropped):
	
		os.remove(original)
		os.remove(cropped)
		
	def close_browser(self):

		self.browser.close()
	
