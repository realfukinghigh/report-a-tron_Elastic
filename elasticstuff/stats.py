import json
import requests
import datetime
import calendar
import config

class Stats:

	def __init__(self):

		config_values = config.StaticValues().config_file
		self.url = config_values['elastic_url']
		self.headers = {"Content-Type": "application/json", "Authorization": "Basic " + config_values['reportatron_service_user']}
		self.sess = requests.Session()

	def getReportatronStats(self):

		engagements_by_month = self.engagementStats()
		issues_by_month = self.issueStats()
		issues_by_type = self.issueTypeStats()
		internet_issues = self.internetFacingStats()
		internet_basics = self.internetFacingBasics()
		third_party_basics = self.thirdPartyBasics()

		return {"engagements_by_month": engagements_by_month, "issues_by_month": issues_by_month, "issues_by_type": issues_by_type, "internet_issues": internet_issues, "internet_basics": internet_basics, "third_party_basics": third_party_basics}


	def engagementStats(self):

		engagement_query = json.dumps({"size": 0, "query": {"bool": {"must_not": [{"exists": {"field": "issue_stuff.issue_title"}}, {"exists": {"field": "test_stuff.test_type"}}], "filter": {"range": {"engagement_stuff.engagement_received_on": {"gte": "2019-01-01"}}}}}, "aggs": {"engagements_by_month": {"date_histogram": {"field": "engagement_stuff.engagement_received_on", "calendar_interval": "month"}, "aggs": {"engagement_type": {"terms": {"field": "asset_stuff.asset_type.keyword"}}}}}})

		engagements_by_month_list = []
		asset_type_dict = {}
		engagements_by_month = self.sess.get(self.url + "_search", headers=self.headers, data=engagement_query)

		for date in engagements_by_month.json()['aggregations']['engagements_by_month']['buckets']:
			month = date['key_as_string'].split('-')[1]
			calendar_month = calendar.month_name[int(month)]
			for asset_type in date['engagement_type']['buckets']:

				asset_type_dict.update({asset_type['key']: asset_type['doc_count']})

			engagements_by_month_list.append({"month": calendar_month, "number": date['doc_count'], "asset_types": asset_type_dict})
			asset_type_dict = {}

		open_engagements_query = json.dumps({"size": 0, "query": {"bool": {"must_not": [{"exists": {"field": "issue_stuff"}}, {"exists": {"field": "test_stuff"}}]}}, "aggs": {"engagement_status": {"terms": {"field": "engagement_stuff.engagement_status.keyword", "size": 10000}}}})

		open_engagements = self.sess.get(self.url + "_search", headers=self.headers, data=open_engagements_query)
		open_engagements = open_engagements.json()['aggregations']['engagement_status']['buckets']

		return {"buckets": engagements_by_month_list, "open_engagements": open_engagements}

	def issueStats(self):

		issues_query = json.dumps({"size": 0, "query": {"bool": {"must": [{"exists": {"field": "issue_stuff.issue_title"}}], "filter": {"range": {"issue_stuff.issue_created_on": {"gte": "2019-01-01"}}}}}, "aggs": {"issues_by_month": {"date_histogram": {"field": "issue_stuff.issue_created_on", "calendar_interval": "month"}, "aggs": {"issue_rating": {"terms": {"field": "issue_stuff.issue_risk_rating.keyword"}}}}}})

		issues_by_month_list = []
		issues_type_dict = {}

		issues_by_month = self.sess.get(self.url + "_search", headers=self.headers, data=issues_query)
		for date in issues_by_month.json()['aggregations']['issues_by_month']['buckets']:
			month = date['key_as_string'].split('-')[1]
			calendar_month = calendar.month_name[int(month)]
			for risk_rating in date['issue_rating']['buckets']:

				issues_type_dict.update({risk_rating['key']: risk_rating['doc_count']})

			issues_by_month_list.append({"month": calendar_month, "number": date['doc_count'], "issue_risk_rating": issues_type_dict})
			issues_type_dict = {}

		issues_by_month = {"buckets": issues_by_month_list}

		return issues_by_month

	def issueTypeStats(self):

		issues_by_type_query = json.dumps({"size": 0, "query": {"bool": {"filter": [{"term": {"issue_stuff.issue_status.keyword": "Open"}}]}}, "aggs": {"issues_by_type": {"terms": {"field": "asset_stuff.asset_type.keyword"}, "aggs": {"issues_rating": {"terms": {"field":"issue_stuff.issue_risk_rating.keyword"}}}}}})

		issues_by_type = self.sess.get(self.url + "_search", headers=self.headers, data=issues_by_type_query)

		issue_rating = {}
		issue_type = []

		for type in issues_by_type.json()['aggregations']['issues_by_type']['buckets']:
			for rating in type['issues_rating']['buckets']:

				issue_rating.update({rating['key']: rating['doc_count']})

			issue_type.append({"type": type['key'], "issues": issue_rating})
			issue_rating = {}

		issues_by_type = {"buckets": issue_type}

		return issues_by_type

	def internetFacingStats(self):

		internet_query = json.dumps({"size": 0, "query": {"bool": {"filter": [{"term": {"issue_stuff.issue_status.keyword": "Open"}}, {"term": {"asset_stuff.asset_internet_facing.keyword": "1"}}]}}, "aggs": {"internet_facing_apps": {"terms": {"field": "issue_stuff.issue_risk_rating.keyword"}}}})

		internet_issues = self.sess.get(self.url + "_search", headers=self.headers, data=internet_query)

		internet_issues_dict = {}
		for bucket in internet_issues.json()['aggregations']['internet_facing_apps']['buckets']:
			internet_issues_dict.update({bucket['key']: bucket['doc_count']})

		return internet_issues_dict

	def internetFacingBasics(self):

		internet_basics_query = json.dumps({"size": 0, "query": {"bool": {"must_not": {"exists": {"field": "issue_stuff.issue_title"}}, "filter": [{"term": {"asset_stuff.asset_internet_facing.keyword": "1"}}]}}})

		internet_facing_apps = self.sess.get(self.url + "_search", headers=self.headers, data=internet_basics_query)
		internet_facing_apps = internet_facing_apps.json()['hits']['total']['value']

		internet_basics_query = json.dumps({"size": 0, "query": {"bool": {"must_not": {"exists": {"field": "issue_stuff.issue_title"}}, "filter": [{"term": {"test_stuff.test_type.keyword": "Application Security Test"}}, {"term": {"asset_stuff.asset_internet_facing.keyword": "1"}}]}}})

		internet_tests = self.sess.get(self.url + "_search", headers=self.headers, data=internet_basics_query)
		internet_tests = internet_tests.json()['hits']['total']['value']

		return {"number_internet_facing_apps": str(internet_facing_apps), "number_of_internet_facing_tests": str(internet_tests)}

	def thirdPartyBasics(self):

		tp_basics_query = json.dumps({"size": 0, "query": {"bool": {"must_not": [{"exists": {"field": "issue_stuff.issue_title"}}, {"exists": {"field": "test_stuff.test_type"}}, {"exists": {"field": "engagement_stuff.engagement_form_location"}}], "filter": [{"term": {"asset_stuff.asset_type.keyword": "Third Party"}}]}}})

		no_third_party = self.sess.get(self.url + "_search", headers=self.headers, data=tp_basics_query)
		no_third_party = no_third_party.json()['hits']['total']['value']

		tp_basics_query = json.dumps({"size": 0, "query": {"bool": {"must_not": {"exists": {"field": "issue_stuff.issue_title"}}, "filter": [{"term": {"test_stuff.test_type.keyword": "Third Party Assessment"}}]}}})

		no_third_party_tests = self.sess.get(self.url + "_search", headers=self.headers, data=tp_basics_query)
		no_third_party_tests = no_third_party_tests.json()['hits']['total']['value']

		return {"number_of_third_parties": no_third_party, "number_third_party_tests": no_third_party_tests}
