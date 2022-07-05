import time
from selenium import webdriver

page = 'https://windscribe.com/signup'




class windscribe_errors:

	def __init__(self):

		self.browser = webdriver.Chrome()
		self.browser.set_window_size(600,600)
		self.browser.get(page)
		
	def signup_process(self):

		username_generation_button = self.browser.find_element_by_xpath('//*[@id="generate_username"]')
		password_generation_button = self.browser.find_element_by_xpath('//*[@id="generate_password"]')
		submit_button = self.browser.find_element_by_xpath('//*[@id="signup_button"]')
		continue_signup_button = self.browser.find_element_by_xpath('//*[@id="body_wrap"]/div[4]/div/ul/li[1]/a')
		captcha_box = self.browser.find_element_by_xpath('//*[@id="captcha1"]')

		username_generation_button.click()
		time.sleep(1)
		password_generation_button.click()
		time.sleep(1)
		submit_button.click()
		time.sleep(3)
		continue_signup_button.click()
		time.sleep(3)
		captcha_box.send_keys('somegarbagevalue')
		time.sleep(1)
		submit_button.click()
		time.sleep(3)

	def error_checking(self):

		while True:	
			try:			
				error_message_xpath = self.browser.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/form/div[1]')
				error_message_text = error_message_xpath.text
				if 'Wrong captcha supplied' in error_message_text:				
					print('Tesseract read it wrong, restarting...')
					return_error_message = True
					time.sleep(2)
					break				 		
			except ElementNotInteractableException:
				break
					
		return return_error_message
		
		
errors = windscribe_errors()

errors.signup_process()

print(errors.error_checking())
