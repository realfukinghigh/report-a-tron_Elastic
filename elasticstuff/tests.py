import json
import requests
import config


class Tests:

	def __init__(self):

		config_values = config.StaticValues().config_file
		self.url = config_values['elastic_url']
		self.headers = {"Content-Type": "application/json", "Authorization": "Basic " + config_values['reportatron_service_user']}
		self.headers = {"Content-Type": "application/json"}
		self.sess = requests.Session()

	def getTests(self):

		body = json.dumps({"size":10000, "query": {"bool": {"must": {"exists": {"field": "test_stuff"}}, "must_not": [{"exists": {"field": "issue_stuff"}}]}}})
		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
		data = sender.json()['hits']['hits']

		return data

	def createtestapi(self, engagement_id, test_type, test_exec_summary, test_base_location, test_limitations, test_main_contact, test_created_on, test_date, test_notes):

		if engagement_id:
			requestor = self.sess.get(self.url + "_doc/" + engagement_id, headers=self.headers)
			_engagementStuff = requestor.json()['_source']['engagement_stuff']

			if _engagementStuff.get('asset_id'):
				requestor = self.sess.get(self.url + "_doc/" + _engagementStuff['asset_id'], headers = self.headers)
				_assetStuff = requestor.json()['_source']['asset_stuff']
				body = json.dumps({"asset_stuff": _assetStuff, "engagement_stuff": _engagementStuff, "test_stuff": {"asset_id": _engagementStuff['asset_id'], "engagement_id": engagement_id, "test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_created_on": test_created_on, "test_date": test_date, "test_notes": test_notes}})

			else:
				body = json.dumps({"engagement_stuff": _engagementStuff, "test_stuff": {"engagement_id": engagement_id, "test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_created_on": test_created_on, "test_date": test_date, "test_notes": test_notes}})

		else:
			body = json.dumps({"test_stuff": {"test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_created_on": test_created_on, "test_date": test_date, "test_notes": test_notes}})

		sender = self.sess.post(self.url + "_doc", data=body, headers=self.headers)
		if sender.status_code != 201:
			raise ReferenceError('test not created')

	def getTestsForEngagement(self, engagement_id):

		body = json.dumps({"size":10000, "query": {"bool": {"must": [{"term": {"test_stuff.engagement_id.keyword": engagement_id}},{"exists": {"field": "engagement_stuff"}}], "must_not": [{"exists": {"field": "issue_stuff"}}]}}})
		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
		data = sender.json()['hits']['hits']

		return data

	def getTestsForAsset(self, asset_id):

		body = json.dumps({"size":10000, "query": {"bool": {"must": [{"term": {"test_stuff.asset_id.keyword": asset_id}},{"exists": {"field": "test_stuff"}}], "must_not": [{"exists": {"field": "issue_stuff"}}]}}})
		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
		data = sender.json()['hits']['hits']

		return data

	def updateTest(self, test_id, test_type, test_exec_summary, test_base_location, test_limitations, test_main_contact, test_date, test_notes):

		body = json.dumps({"doc": {"test_stuff": {"test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_date": test_date, "test_notes": test_notes}}})

		sender = self.sess.post(self.url + "_update/" + test_id, headers=self.headers, data=body)

		if sender.status_code != 200:
			raise ReferenceError('update failed')
