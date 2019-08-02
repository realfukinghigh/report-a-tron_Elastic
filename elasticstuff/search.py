import json
import requests


class Search:

    def __init__(self):

        self.headers = {"Content-Type": "application/json"}
        self.url = "http://192.168.5.131:9200/reportatron/"
        self.sess = requests.Session()

    def search(self, searchTerm):

        if "doc:" in searchTerm:

            queryTerm = searchTerm.split(':')[1]
            sender = self.sess.get(self.url + "_doc/" + queryTerm, headers=self.headers)
            data = sender.json()

            return [data]

        elif "keyword:" in searchTerm:

            queryTerm = searchTerm.split(':')[1]
            body = json.dumps({"size": 10000, "query": {"query_string" : {"fields" : ["asset_stuff.asset_name.keyword", "issue_stuff.issue_title.keyword", "asset_stuff.asset_owner.keyword", "engagement_stuff.engagement_main_contact.keyword", "test_stuff.test_main_contact.keyword", "asset_stuff.asset_type.keyword", "issue_stuff.issue_ra_stuff.issue_ra_owner.keyword"], "query": queryTerm}}})

            sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
            data = sender.json()['hits']['hits']

            return data

        elif "search:" in searchTerm:

            queryTerm = searchTerm.split(':')[1]
            body = json.dumps({"size": 10000, "query": {"query_string" : {"fields" : ["asset_stuff.asset_name", "asset_stuff.asset_notes", "issue_stuff.issue_title", "asset_stuff.asset_owner", "engagement_stuff.engagement_main_contact", "test_stuff.test_main_contact", "asset_stuff.asset_type", "issue_stuff.issue_ra_stuff.issue_ra_owner"], "query": queryTerm}}})

            sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
            data = sender.json()['hits']['hits']

            return data

        else:

            queryTerm = searchTerm
            body = json.dumps({"size": 10000, "query": {"query_string" : {"fields" : ["asset_stuff.asset_name", "asset_stuff.asset_notes", "issue_stuff.issue_title", "asset_stuff.asset_owner", "engagement_stuff.engagement_main_contact", "test_stuff.test_main_contact", "asset_stuff.asset_type", "issue_stuff.issue_ra_stuff.issue_ra_owner"], "query": queryTerm}}})

            sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
            data = sender.json()['hits']['hits']

            return data
