import json
import requests


class Tests: 

	def __init__(self): 
	
		self.headers = {"Content-Type": "application/json"}
		self.url = "http://192.168.5.131:9200/reportatron/"
		self.sess = requests.Session()
		
	def getTests(self): 

		body = json.dumps({"size":10000, "query": {"bool": {"must": {"exists": {"field": "test_stuff"}}, "must_not": [{"exists": {"field": "issue_stuff"}}]}}})

		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
		data = sender.json()['hits']['hits']

		return data
		
	def createTest(self, engagement_id, test_type, test_exec_summary, test_base_location, test_limitations, test_main_contact, test_created_on, test_date, test_notes): 

		if engagement_id: 
			requestor = self.sess.get(self.url + "_doc/" + engagement_id, headers=self.headers)
			_engagementStuff = requestor.json()['_source']['engagement_stuff']
			print(_engagementStuff)
			
			if _engagementStuff.get('asset_id'): 
				requestor = self.sess.get(self.url + "_doc/" + _engagementStuff['asset_id'], headers = self.headers)
				_assetStuff = requestor.json()['_source']['asset_stuff']
			
				body = json.dumps({"asset_stuff": _assetStuff, "engagement_stuff": _engagementStuff, "test_stuff": {"engagement_id": engagement_id, "test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_created_on": test_created_on, "test_date": test_date, "test_notes": test_notes}})

			else: 
				body = json.dumps({"engagement_stuff": _engagementStuff, "test_stuff": {"engagement_id": engagement_id, "test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_created_on": test_created_on, "test_date": test_date, "test_notes": test_notes}})
		
		else: 
			body = json.dumps({"test_stuff": {"test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_created_on": test_created_on, "test_date": test_date, "test_notes": test_notes}})
			print(body)
		
		sender = self.sess.post(self.url + "_doc", data=body, headers=self.headers)
		#if sender.status_code != 201: 
		#	raise ReferenceError('test not created')