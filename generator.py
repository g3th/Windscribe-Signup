#!/usr/bin/python3
#secure password generator

import requests
import os
from random import randint
from pathlib import Path

temp_mail_api_endpoint ='https://www.1secmail.com/api/v1/'

class password_generator():

	def __init__(self):                                 
		self.num=randint(0,9)                          
		self.sym="{@}#1!'*-=}["
		self.dig="abcdefghijklmnopqrstuvwxyz"
	
	def generate_password(self, p_len):
		passw=[];password='';flag=0
		while len(passw)<p_len:
			sy=randint(0,11);di=randint(0,25)
			s=self.sym[sy];d=self.dig[di]
			randomize=[self.num,s,d]
			r=randint(0,2)
			passgen=randomize[r]
			if flag ==0:
				try:
					if passgen.isalpha():
						passgen = passgen.upper(); flag =1
				except:
					pass	
			passw.append(passgen)
			passw=list(dict.fromkeys(passw))
		for char in passw:
			password=password+str(char)
		return password


class username_generator():

	def __init__(self):
		suffix=randint(1980,2022)
		self.user=str(suffix)

	def generate_a_username(self):
		page='https://api.namefake.com/'
		while True:		
			with requests.session() as name:
				post = requests.get(page)
				element = post.json()
				name = element['name'].replace(" ","_").replace("'","")
			if len(name) > 15:
				pass
			else:
				break
		return str(name + self.user)

class create_and_store_a_mailbox:
	
	def __init__(self):
		
		self.temp_mail_api_endpoint ='https://www.1secmail.com/api/v1/'
		self.created_mailbox = requests.get(temp_mail_api_endpoint, params = {'action':'genRandomMailbox','count':'1'})
				
	def write_mailbox_to_file(self):
		
		with open('temp_mailboxes','a') as mailboxes:		
			self.mailbox = str(self.created_mailbox.text)
			mailboxes.write(self.mailbox+"\n")
										
def check_email():

	mailboxes_list = []
	
	with open('temp_mailboxes','r') as fetch_mailboxes:
		for lines in fetch_mailboxes:
			mailboxes_list.append(lines)
	fetch_mailboxes.close()
	
	for box in mailboxes_list:
		fetch_email_message_id = requests.get(temp_mail_api_endpoint, params = {'action':'getMessages','login':box.split('"')[1].split("@")[0] ,'domain': box.split('"')[1].split("@")[1]}).json()
			
	email_message_id = fetch_email_message_id[0]['id']
	
	get_email_message = requests.get(temp_mail_api_endpoint, params = {'action':'readMessage','login':box.split('"')[1].split("@")[0] ,'domain': box.split('"')[1].split("@")[1], 'id':email_message_id}).json()
	
	print(get_email_message['textBody'])	

def write_credentials_to_file(credentials_list):

	with open('credentials','a') as credentials:
		for lines in credentials_list:
			credentials.write(lines)
	credentials.close()
	
