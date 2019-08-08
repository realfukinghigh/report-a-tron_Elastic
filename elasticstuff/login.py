import json
import requests
import bcrypt

class Login:

    def __init__(self):

        self.headers = {"Content-Type": "application/json"}
        self.url = "http://192.168.196.129:9200/reportatron_users/"
        self.sess = requests.Session()

    def loginCheck(self, username, password):

        body = json.dumps({"query": {"bool": {"filter": {"term": {"username.keyword": username}}}}})
        data = self.sess.get(self.url + "_search", headers=self.headers, data=body).json()
        hashed_password = data['hits']['hits'][0]['_source']['password']

        is_logged_in = bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))
        password = ""
        return is_logged_in
