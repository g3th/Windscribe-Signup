from selenium import webdriver
import requests
from random import randint

list_of_proxies = []

with requests.session() as proxies:

	fetch_proxy_list = proxies.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=10000&country=all",timeout=5)

	list_of_proxies = list(fetch_proxy_list.text)

print(list_of_proxies)

'''
proxy= '100.100.100.100:8080'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % proxy)
chrome = webdriver.Chrome(chrome_options = chrome_options)
chrome.get('https://www.google.com')'''
