import json
import requests


class Assets:

	def __init__(self):

		self.headers = {"Content-Type": "application/json"}
		self.url = "http://192.168.130.135:9200/reportatron/"
		self.sess = requests.Session()

	def getAssets(self):

		body = json.dumps({"size": 10000, "query": {"bool": {"must_not": [{"exists": {"field": "engagement_stuff"}}, {"exists": {"field": "test_stuff"}}, {"exists": {"field": "issue_stuff"}}, {"exists": {"field": "third_party_stuff"}}]}}})

		sender = self.sess.get(self.url + "_search", data=body, headers=self.headers)
		data = sender.json()['hits']['hits']

		return data

	def createAsset(self, asset_name, asset_type, asset_owner, timenow, asset_notes, asset_internet_facing):

		body = json.dumps({"asset_stuff": {"asset_name": asset_name, "asset_type": asset_type, "asset_owner": asset_owner, "asset_created_on": timenow, "asset_notes": asset_notes, "asset_internet_facing": asset_internet_facing}})

		sender = self.sess.post(self.url + "_doc", data=body, headers=self.headers)

		if sender.status_code != 201:
			raise ReferenceError('asset not created')

	def updateAsset(self, asset_id, asset_name, asset_type, asset_owner, asset_notes, asset_internet_facing):

		body = json.dumps({"doc": {"asset_stuff" : {"asset_name": asset_name, "asset_type": asset_type, "asset_owner": asset_owner, "asset_notes": asset_notes, "asset_internet_facing": asset_internet_facing}}})

		sender = self.sess.post(self.url + "_update/" + asset_id, headers=self.headers, data=body)

		if sender.status_code != 200:
			raise ReferenceError('update failed')
