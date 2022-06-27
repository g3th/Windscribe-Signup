import os
from random import randint

ovpn = []

with open ('config.py','r') as config:
	for line in config:
		with open ('config.ovpn', 'a+') as ovpn:
			if 'remote 443' in line:
				replace_line = line.replace('remote 443','This is the replacement line')
				ovpn.write(replace_line)
			else:
				ovpn.write(line)
				
config.close()
ovpn.close()

input("Remove: ")

os.remove('config.ovpn')
