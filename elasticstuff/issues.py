import json
import requests

class Issues:

    def __init__(self):

        self.headers = {"Content-Type": "application/json"}
        self.url = "http://192.168.5.131:9200/reportatron/"
        self.sess = requests.Session()

    def getIssues(self):

        body = json.dumps({"size":10000, "query": {"bool": {"must": {"exists": {"field": "issue_stuff"}}}}})
        sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
        data = sender.json()['hits']['hits']

        return data

    def createNewIssue(self, test_id, issue_title, issue_location, issue_description, issue_remediation, issue_risk_rating, issue_risk_impact, issue_risk_likelihood, issue_status, issue_details, issue_notes, timenow):

        if test_id:
            requestor = self.sess.get(self.url + "_doc/" + test_id, headers=self.headers)
            _testStuff = requestor.json()['_source']['test_stuff']

            if _testStuff.get('engagement_id'):
                requestor = self.sess.get(self.url + "_doc/" + _testStuff['engagement_id'], headers = self.headers)
                _engagementStuff = requestor.json()['_source']['engagement_stuff']
                body = json.dumps({"engagement_stuff": _engagementStuff, "test_stuff": _testStuff, "issue_stuff": {"issue_title": issue_title, "issue_location": issue_location, "issue_description": issue_description, "issue_remediation": issue_remediation, "issue_risk_rating": issue_risk_rating, "issue_risk_impact": issue_risk_impact, "issue_risk_likelihood": issue_risk_likelihood, "issue_status": issue_status, "issue_details": issue_details, "issue_notes": issue_notes, "issue_created_on": timenow}})

                if _engagementStuff.get('asset_id'):
                    requestor = self.sess.get(self.url + "_doc/" + _engagementStuff['asset_id'], headers = self.headers)
                    _assetStuff = requestor.json()['_source']['asset_stuff']
                    body = json.dumps({"asset_stuff": _assetStuff, "engagement_stuff": _engagementStuff, "test_stuff": _testStuff, "issue_stuff": {"issue_title": issue_title, "issue_location": issue_location, "issue_description": issue_description, "issue_remediation": issue_remediation, "issue_risk_rating": issue_risk_rating, "issue_risk_impact": issue_risk_impact, "issue_risk_likelihood": issue_risk_likelihood, "issue_status": issue_status, "issue_details": issue_details, "issue_notes": issue_notes, "issue_created_on": timenow}})

            else:
                body = json.dumps({"test_stuff": _testStuff, "issue_stuff": {"issue_title": issue_title, "issue_location": issue_location, "issue_description": issue_description, "issue_remediation": issue_remediation, "issue_risk_rating": issue_risk_rating, "issue_risk_impact": issue_risk_impact, "issue_risk_likelihood": issue_risk_likelihood, "issue_status": issue_status, "issue_details": issue_details, "issue_notes": issue_notes, "issue_created_on": timenow}})

        else:
            body = json.dumps({"issue_stuff": {"issue_title": issue_title, "issue_location": issue_location, "issue_description": issue_description, "issue_remediation": issue_remediation, "issue_risk_rating": issue_risk_rating, "issue_risk_impact": issue_risk_impact, "issue_risk_likelihood": issue_risk_likelihood, "issue_status": issue_status, "issue_details": issue_details, "issue_notes": issue_notes, "issue_created_on": timenow}})

        sender = self.sess.post(self.url + "_doc", data=body, headers=self.headers)
        if sender.status_code != 201:
            raise ReferenceError('test not created')

    def updateIssue(self, issue_id, issue_title, issue_risk_rating, issue_risk_impact, issue_risk_likelihood, issue_location, issue_status, issue_description, issue_remediation, issue_details, issue_notes, issue_ra_date, issue_ra_owner, issue_ra_expiry, issue_ra_notes):

        body = json.dumps({"doc": {"issue_stuff": {"issue_title": issue_title, "issue_location": issue_location, "issue_description": issue_description, "issue_remediation": issue_remediation, "issue_risk_rating": issue_risk_rating, "issue_risk_impact": issue_risk_impact, "issue_risk_likelihood": issue_risk_likelihood, "issue_status": issue_status, "issue_details": issue_details, "issue_notes": issue_notes, "issue_ra_stuff": {"issue_ra_date": issue_ra_date, "issue_ra_owner": issue_ra_owner, "issue_ra_expiry": issue_ra_expiry, "issue_ra_notes": issue_ra_notes}}}})

        sender = self.sess.post(self.url + "_update/" + issue_id, headers=self.headers, data=body)

        if sender.status_code != 200:
            raise ReferenceError('update failed')
