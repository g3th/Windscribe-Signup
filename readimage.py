import io
import pytesseract
import time
from selenium import webdriver
from PIL import Image

def screenshot(url):

	DRIVER = 'chromedriver'
	driver = webdriver.Chrome(DRIVER)
	driver.get('https://windscribe.com/captcha/'+url);time.sleep(3)
	screenshot = driver.save_screenshot('my_screenshot.png')
	driver.quit()

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


