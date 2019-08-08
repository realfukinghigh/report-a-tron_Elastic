import requests
import json

class Reports:

    def __init__(self):

        self.headers = {"Content-Type": "application/json"}
        self.url = "http://192.168.196.129:9200/reportatron/"
        self.sess = requests.Session()

    def getTestReport(self, test_id):

        test_report_query = json.dumps({"size": 1000, "query": {"bool": {"filter": {"term": {"issue_stuff.test_id.keyword": "bV17cGwBOST1_FrxlOqt"}}}}})

        test_report_data = self.sess.get(self.url + "_search", headers=self.headers, data=test_report_query)

        return test_report_data.json()['hits']['hits']
