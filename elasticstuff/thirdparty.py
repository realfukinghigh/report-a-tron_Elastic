import json
import requests

class Thirdparty:

    def __init__(self):

        self.headers = {"Content-Type": "application/json"}
		self.url = "http://192.168.5.131:9200/reportatron/"
		self.sess = requests.Session()

    def createThirdParty(self, asset_id, asset_name, asset_type, asset_owner, timenow, asset_notes, asset_internet_facing):

        body = json.dumps({"doc": {"third_party_stuff": {"third_party_name": asset_name, "third_party_owner": asset_owner,}}})
		sender = self.sess.post(self.url + "_update/" + asset_id, headers=self.headers, data=body)

		if sender.status_code != 200:
			raise ReferenceError('update failed')

    def getThirdParty(self):

        body = json.dumps({"size": 10000, "query": {"bool": {"must_not": [{"exists": {"field": "engagement_stuff"}}, {"exists": {"field": "test_stuff"}}, {"exists": {"field": "issue_stuff"}}], "must": {"exists": {"field": "third_party_stuff"}}}}})

		sender = self.sess.get(self.url + "_search", data=body, headers=self.headers)
		data = sender.json()['hits']['hits']

		return data
