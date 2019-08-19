import json
import requests
import config


class Assets:

	def __init__(self):

		config_values = config.StaticValues().config_file
		self.url = config_values['elastic_url']
		self.headers = {"Content-Type": "application/json", "Authorization": "Basic " + config_values['reportatron_service_user']}
		self.sess = requests.Session()

	def getAssets(self):

		body = json.dumps({"size": 10000, "query": {"bool": {"must_not": [{"exists": {"field": "engagement_stuff"}}, {"exists": {"field": "test_stuff"}}, {"exists": {"field": "issue_stuff"}}], "must": {"exists": {"field": "asset_stuff"}}}}})

		sender = self.sess.get(self.url + "_search", data=body, headers=self.headers)
		data = sender.json()['hits']['hits']

		return data

	def createAsset(self, asset_name, asset_type, asset_owner, timenow, asset_notes, asset_internet_facing):

		body = json.dumps({"asset_stuff": {"asset_name": asset_name, "asset_type": asset_type, "asset_owner": asset_owner, "asset_created_on": timenow, "asset_notes": asset_notes, "asset_internet_facing": asset_internet_facing}})

		sender = self.sess.post(self.url + "_doc", data=body, headers=self.headers)

		if sender.status_code != 201:
			raise ReferenceError('asset not created')

		return sender.json()['_id']

	def updateAsset(self, asset_id, asset_name, asset_type, asset_owner, asset_notes, asset_internet_facing):

		body = json.dumps({"doc": {"asset_stuff" : {"asset_name": asset_name, "asset_type": asset_type, "asset_owner": asset_owner, "asset_notes": asset_notes, "asset_internet_facing": asset_internet_facing}}})

		sender = self.sess.post(self.url + "_update/" + asset_id, headers=self.headers, data=body)

		if sender.status_code != 200:
			raise ReferenceError('update failed')
