import json
import requests


class Docs:

	def __init__(self):

		self.headers = {"Content-Type": "application/json"}
		self.url = "http://192.168.130.135:9200/reportatron/"
		self.sess = requests.Session()

	def getDoc(self, doc_id):

		sender = self.sess.get(self.url + "_doc/" + doc_id, headers=self.headers)
		data = sender.json()

		return data
