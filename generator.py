import requests

from bs4 import BeautifulSoup as bs
from random import randint

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
	
		self.adjective = 'https://randomword.com/adjective'
		self.noun = 'https://randomword.com/noun'
		
	def generate_a_username(self):
		
		fetch_adjective = requests.get(self.adjective)
		fetch_noun = requests.get(self.noun)
		soup_adjective = bs(fetch_adjective.text,'html.parser')
		soup_noun = bs(fetch_noun.text,'html.parser')
		adjective = soup_adjective.find('div',{'id':'random_word'})
		noun = soup_noun.find('div',{'id':'random_word'})
		
		return adjective.text.capitalize() + noun.text.capitalize()
										
def write_credentials_to_file(username, password, email):

	with open('config_files/created_accounts','a') as accounts:
		accounts.write(username+":"+password+" --- "+email+"\n")
	accounts.close()

