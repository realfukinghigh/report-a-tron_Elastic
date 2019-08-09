from flask import Flask, render_template, request, redirect, url_for
from elasticstuff import search
from webhandlers import assetsflask, engagementsflask, testsflask, issuesflask, thirdpartyflask, servicesflask, loginflask, statsflask, reportsflask
from waitress import serve
import config


app = Flask(__name__)
config_values = config.StaticValues().config_file
app.config.from_object(config_values['config_type'])

searchConnection = search.Search()

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/createasset")
def createasset():
	return assetsflask.createasset()

@app.route("/error")
def error():
	return render_template('error.html')

@app.route("/complete")
def complete():
	return render_template('complete.html')

@app.route("/gethtmlreport")
def gethtmlreport():
	return render_template('convert_md.html')

@app.route("/viewassets")
def viewassets():
	return assetsflask.viewassets()

@app.route("/report")
def report():
	return render_template('report.html')

@app.route("/createassetapi", methods=['POST'])
def createassetapi():
	return assetsflask.createassetapi()

@app.route("/updateasset")
def updateasset():
	return assetsflask.updateasset()

@app.route("/updateassetapi", methods=['POST'])
def updateassetapi():
	return assetsflask.updateassetapi()

@app.route("/engagements", methods=['GET'])
def engagements():
	return engagementsflask.engagements()

@app.route("/createengagement", methods=['POST'])
def createengagement():
	return engagementsflask.createengagement()

@app.route("/openengagements")
def openengagements():
	return engagementsflask.openengagements()

@app.route("/viewengagements")
def viewengagements():
	return engagementsflask.viewengagements()

@app.route("/updateengagement")
def updateengagement():
	return engagementsflask.updateengagement()

@app.route("/updateengagementapi", methods=['POST'])
def updateengagementapi():
	return engagementsflask.updateengagementapi()

@app.route("/createtest", methods=['GET'])
def createtest():
	return testsflask.createtest()

@app.route("/createtestapi", methods=['POST'])
def createtestapi():
	return testsflask.createtestapi()

@app.route("/viewtests", methods=['GET'])
def viewtests():
	return testsflask.viewtests()

@app.route("/updatetest")
def updatetest():
	return testsflask.updatetest()

@app.route("/updatetestapi", methods=['POST'])
def updatetestapi():
	return testsflask.updatetestapi()

@app.route("/viewissues", methods=['GET'])
def viewissues():
	return issuesflask.viewissues()

@app.route("/createissue", methods=['GET'])
def createissue():
	return issuesflask.createissue()

@app.route("/createissueapi", methods=['POST'])
def createissueapi():
	return issuesflask.createissueapi()

@app.route("/updateissue", methods=['GET'])
def updateissue():
	return issuesflask.updateissue()

@app.route("/updateissueapi", methods=['POST'])
def updateissueapi():
	return issuesflask.updateissueapi()

@app.route("/linkissue", methods=['GET'])
def linkissue():
	return issuesflask.linkissue()

@app.route("/issuelinkapi", methods=['POST'])
def issuelinkapi():
	return issuesflask.issuelinkapi()

@app.route("/testreport", methods=['GET'])
def testreport():
	return reportsflask.testReport()

@app.route("/stats")
def stats():
	return render_template('stats.html')

@app.route("/viewstats")
def viewstats():
	return statsflask.viewstats()

@app.route("/search")
def search():
	searchTerm = request.args.get('searchTerm')
	data = searchConnection.search(searchTerm)
	return render_template('searchresults.html', data=data)

@app.route("/viewthirdparty")
def viewthirdparty():
	return thirdpartyflask.viewthirdparty()

@app.route("/createthirdparty")
def createthirdparty():
	return render_template('createthirdparty.html')

@app.route("/updatethirdparty")
def updatethirdparty():
	return thirdpartyflask.updatethirdparty()

@app.route("/updatethirdpartyapi", methods=['POST'])
def updatethirdpartyapi():
	return thirdpartyflask.updatethirdpartyapi()

@app.route('/viewservices')
def viewservices():
	return servicesflask.viewservices()

@app.route('/viewservicedetail')
def viewservicedetail():
	service_id = request.args.get('service_id')
	return servicesflask.viewservicedetail(service_id)

@app.route('/createservice')
def createservice():
	return servicesflask.createservice()

@app.route('/createserviceapi', methods=['POST'])
def createserviceapi():
	return servicesflask.createserviceapi()

@app.route('/updateservice')
def updateservice():
	service_id = request.args.get('service_id')
	return servicesflask.updateservice(service_id)

@app.route('/updateserviceapi', methods=['POST'])
def updateserviceapi():
	return servicesflask.updateserviceapi()

if __name__ == "__main__":
	serve(app, host=config_values['server_ip'], port=int(config_values['server_port']))
