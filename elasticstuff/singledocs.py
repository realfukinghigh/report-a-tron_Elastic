import json
import requests
import config


class Docs:

	def __init__(self):

		self.headers = {"Content-Type": "application/json"}
		self.sess = requests.Session()
		config_values = config.StaticValues().config_file
		self.url = config_values['elastic_url']

	def getDoc(self, doc_id):

		sender = self.sess.get(self.url + "_doc/" + doc_id, headers=self.headers)
		data = sender.json()

		return data
