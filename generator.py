#!/usr/bin/python3
#secure password generator

import requests
from random import randint


class password_generator():

	def __init__(self):                                 
		self.num=randint(0,9)                          
		self.sym="{@}#1!'*-=}["
		self.dig="abcdefghijklmnopqrstuvwxyz"
	
	def gen(self, p_len):
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


class u_gen():

	def __init__(self):
		suffix=randint(1980,2022)
		self.user=str(suffix)

	def name(self):
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
