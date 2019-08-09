import requests
import json
import config

class Reports:

    def __init__(self):

        self.headers = {"Content-Type": "application/json"}
        self.sess = requests.Session()
        config_values = config.StaticValues().config_file
        self.url = config_values['elastic_url']

    def getTestReport(self, test_id):

        test_report_query = json.dumps({"size": 1000, "query": {"bool": {"filter": {"term": {"issue_stuff.test_id.keyword": "bV17cGwBOST1_FrxlOqt"}}}}})

        test_report_data = self.sess.get(self.url + "_search", headers=self.headers, data=test_report_query)

        return test_report_data.json()['hits']['hits']
