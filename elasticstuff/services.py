import requests
import json
import config

class Services:

    def __init__(self):

        self.headers = {"Content-Type": "application/json"}
        self.sess = requests.Session()
        config_values = config.StaticValues().config_file
        self.url = config_values['elastic_url']

    def createService(self, service_name, service_owner, service_has_assets):

        body = json.dumps({"service_stuff": {"service_name": service_name, "service_owner": service_owner, "service_has_assets": service_has_assets}})
        self.sess.post(self.url + "_doc", headers=self.headers, data=body)

    def getServices(self):

        body = json.dumps({"size": 10000, "query": {"bool": {"must": {"exists": {"field": "service_stuff"}}}}})
        data = self.sess.get(self.url + "_search", headers=self.headers, data=body)

        return data.json()['hits']['hits']

    def getServiceDetail(self, service_id):

        data = self.sess.get(self.url + "_doc/" + service_id, headers=self.headers).json()

        asset_list = []

        for asset_id in data['_source']['service_stuff']['service_has_assets']:
            asset_data = self.sess.get(self.url + "_doc/" + asset_id, headers=self.headers)
            asset_list.append(asset_data.json()['_source']['asset_stuff'])

        data.update({"asset_stuff": asset_list})

        return data

    def updateService(self, service_id, service_name, service_owner, service_has_assets):

        body = json.dumps({"doc": {"service_stuff" : {"service_name": service_name, "service_owner": service_owner, "service_has_assets": service_has_assets}}})

        data = self.sess.post(self.url + "_update/" + service_id, headers=self.headers, data=body)
        return data
