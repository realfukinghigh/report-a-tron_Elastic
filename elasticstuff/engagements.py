import json
import requests


class Engagements:

	def __init__(self):

		self.headers = {"Content-Type": "application/json"}
		self.url = "http://192.168.5.131:9200/reportatron/"
		self.sess = requests.Session()

	def getEngagements(self):

		body = json.dumps({"size":10000, "query": {"bool": {"must": {"exists": {"field": "engagement_stuff"}}, "must_not": [{"exists": {"field": "issue_stuff"}}, {"exists": {"field": "test_stuff"}}]}}})

		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
		data = sender.json()['hits']['hits']

		return data

	def createEngagement(self, asset_id, engagement_form_location, engagement_main_contact, engagement_risk_rating, engagement_received_on, engagement_action_taken,  engagement_notes):

		if asset_id:
			requestor = self.sess.get(self.url + "_doc/" + asset_id, headers=self.headers)
			_assetStuff = requestor.json()['_source']['asset_stuff']

			body = json.dumps({"asset_stuff": _assetStuff, "engagement_stuff": {"asset_id": requestor.json()['_id'], "engagement_form_location": engagement_form_location, "engagement_main_contact": engagement_main_contact, "engagement_risk_rating": engagement_risk_rating, "engagement_received_on": engagement_received_on, "engagement_action_taken": engagement_action_taken, "engagement_notes": engagement_notes, "engagement_status": "Open"}})

		else:
			body = json.dumps({"engagement_stuff": {"engagement_form_location": engagement_form_location, "engagement_main_contact": engagement_main_contact, "engagement_risk_rating": engagement_risk_rating, "engagement_received_on": engagement_received_on, "engagement_action_taken": engagement_action_taken, "engagement_notes": engagement_notes, "engagement_status": "Open"}})

		sender = self.sess.post(self.url + "_doc", data=body, headers=self.headers)
		if sender.status_code != 201:
			raise ReferenceError('engagement not created')

	def getEngagementsForAsset(self, asset_id):

		body = json.dumps({"size":10000, "query": {"bool": {"must": {"term": {"engagement_stuff.asset_id.keyword": asset_id}}, "must_not": [{"exists": {"field": "issue_stuff"}},{"exists": {"field": "test_stuff"}}]}}})

		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
		data = sender.json()['hits']['hits']

		return data

	def updateEngagement(self, engagement_id, engagement_form_location, engagement_main_contact, engagement_risk_rating, engagement_received_on, engagement_action_taken,  engagement_notes, engagement_status):

		body = json.dumps({"doc": {"engagement_stuff": {"engagement_form_location": engagement_form_location, "engagement_main_contact": engagement_main_contact, "engagement_risk_rating": engagement_risk_rating, "engagement_received_on": engagement_received_on, "engagement_action_taken": engagement_action_taken, "engagement_notes": engagement_notes, "engagement_status": engagement_status}}})

		sender = self.sess.post(self.url + "_update/" + engagement_id, headers=self.headers, data=body)

		if sender.status_code != 200:
			raise ReferenceError('update failed')

	def getOpenEngagements(self):

		body = json.dumps({"size":10000, "query": {"bool": {"must": [{"exists": {"field": "engagement_stuff"}}, {"term": {"engagement_stuff.engagement_status.keyword": "Open"}}], "must_not": [{"exists": {"field": "issue_stuff"}}, {"exists": {"field": "test_stuff"}}]}}})

		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
		data = sender.json()['hits']['hits']

		return data
