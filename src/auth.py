import hashlib
import json
import os

class Auth(object):
	
	status = False
	source = ""
	username = ""
	password = ""
	
	def __init__(self, username=None, password=None):
		""" Constructor """
		self.__get_source()
		if username != "" and password != "":
			self.username = username
			self.password = password
			user_data = self.get_user()
			if len(user_data) != 0:
				user_data = user_data.pop()
				usr_salt = user_data['salt']
				usr_pass = user_data['pass']
				pss_salted = hashlib.sha512( password + usr_salt ).hexdigest()
				if pss_salted == usr_pass:
					self.status = True
					print 'entre'

	def __get_source(self):
		current_path = os.path.dirname(os.path.realpath(__file__))
		self.source = current_path+"/../data/users.json"
		
	def get_user(self):
		data = json.load(open(self.source, "r"))
		return [row for row in data if row['user'] == self.username]
	
	def get_name_by_user(self, user):
		data = json.load(open(self.source, "r"))
		data_set = [row for row in data if row['user'] == user]
		return data_set[0]['name']
		
	def get_name_by_role(self, user):
		data = json.load(open(self.source, "r"))
		data_set = [row for row in data if row['user'] == user]
		return data_set[0]['role']


	def get_users(self):
		return json.load(open(self.source, "r"))
