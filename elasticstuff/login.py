import requests
import json
import bcrypt
from flask_login import UserMixin
import config

class User(UserMixin):
    pass

class Login:

    def __init__(self):

        self.headers = {"Content-Type": "application/json"}
        self.sess = requests.Session()
        config_values = config.StaticValues().config_file
        self.url = config_values['elastic_users']

    def checkUserExists(self, username):

        user_query = json.dumps({"size": 0, "query": {"bool": {"must": {"exists": {"field": str(username)}}}}})

        sender = self.sess.get(self.url + "_search", data=user_query, headers=self.headers)
        if sender.json()['hits']['total']['value'] == 1:
            return True
        else:
            return False

    def createUser(self, username, password):

        hashed_password = self.hashPassword(password)
        body = json.dumps({username: {"password": hashed_password}})

        sender = self.sess.post(self.url + "_doc", data=body, headers=self.headers)

        if sender.status_code != 201:
            raise ReferenceError('asset not created')


    def hashPassword(self, password):

        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(12))
        return hashed_password

    def comparePassword(self, username, password):

        user_query = json.dumps({"query": {"bool": {"must": {"exists": {"field": str(username)}}}}})

        sender = self.sess.get(self.url + "_search", data=user_query, headers=self.headers)

        hashed_password = sender.json()['hits']['hits'][0]['_source'][username]['password']
        password_check = bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))
        return password_check
