from flask import Flask, render_template, request, redirect, url_for
import random
import json
import datetime
import requests
import markdown
import configparser
import elasticstuffa
from elasticstuff import assets, singledocs, engagements, tests, search, thirdparty
from webhandlers import assetsflask, engagementsflask, testsflask, issuesflask, thirdpartyflask
#import reportWriter
#import theStatMachine as stat

assetConnection = assets.Assets()
docConnection = singledocs.Docs()
engagementConnection = engagements.Engagements()
testConnection = tests.Tests()
searchConnection = search.Search()

app = Flask(__name__)
@app.route("/")
def main():
	return render_template('index.html')

@app.route("/newapp")
def newapp():
	return assetsflask.newapp()

@app.route("/error")
def error():
	return render_template('error.html')

@app.route("/complete")
def complete():
	return render_template('complete.html')

@app.route("/gethtmlreport")
def gethtmlreport():
	return render_template('convert_md.html')

@app.route("/thedata")
def thedata():
	return assetsflask.thedata()

@app.route("/report")
def report():
	return render_template('report.html')

@app.route("/createapp", methods=['POST'])
def createapp():
	return assetsflask.createapp()

@app.route("/updateasset")
def updateasset():
	return assetsflask.updateasset()

@app.route("/updateassetapi", methods=['POST'])
def updateassetapi():
	return assetsflask.updateassetapi()

@app.route("/engagements", methods=['GET'])
def engagements():
	return engagementsflask.engagements()

@app.route("/newengagement", methods=['POST'])
def newengagement():
	return engagementsflask.newengagement()

@app.route("/openengagements")
def openengagements():
	return engagementsflask.openengagements()

@app.route("/viewengagements")
def viewengagements():
	return engagementsflask.viewengagements()

@app.route("/updateEng")
def updateEng():
	return engagementsflask.updateEng()

@app.route("/updateengagement", methods=['POST'])
def updateengagement():
	return engagementsflask.updateengagement()

@app.route("/newtest", methods=['GET'])
def newtest():
	return testsflask.newtest()

@app.route("/createtest", methods=['POST'])
def createtest():
	return testsflask.createtest()

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

@app.route("/createnewissue", methods=['GET'])
def createnewissue():
	return issuesflask.createnewissue()

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
#	asset_id = request.form['asset_id']
#	_issueID = request.form['issueID']
#	try:
#		dbstuff.createAssetIssueLink(asset_id, _issueID)
#		return redirect(url_for("viewissues"))
#	except:
#		return redirect(url_for("error"))



@app.route("/testreport", methods=['GET'])
def testreport():
	test_id = request.args.get('test_id')
	asset_id = request.args.get('asset_id')
	testData = dbstuff.getTestDataForReport(test_id)
	issueData = dbstuff.getIssuesForTest(test_id)
	if asset_id:
		asset_name = dbstuff.getSingleAssetTestData(asset_id)[0]['asset_name']
	else:
		asset_name = "None"
	reportWriter.writeTestReport(issueData, asset_name, testData)
	return gethtmlreport()

@app.route("/adhocreport", methods=['GET'])
def adhocreport():
	return render_template('adhocreport.html')

@app.route("/writeadhocreport", methods=['POST'])
def writeadhocreport():
	asset_name = request.form['asset_name']
	_issuesOpen = request.form.get('issuesOpen')
	if _issuesOpen:
		_issuesOpen = "Open"
	_issuesClosed = request.form.get('issuesClosed')
	if _issuesClosed:
		_issuesClosed = "Closed"
	_issuesRA = request.form.get('issuesRA')
	if _issuesRA:
		_issuesRA = "Risk Accepted"
	print(_issuesOpen, _issuesClosed, _issuesRA)
	_reportType = request.form['reportType']

	asset_id = dbstuff.getasset_idFromTitle(asset_name)[0]
	if _reportType == "testReport":
		pass
	elif _reportType == "engagementReport":
		pass
	elif _reportType == "assetReport":
		try:
			issueData = dbstuff.getIssuesForAsset(asset_id)
			print(issueData)
			engCount = dbstuff.countEngagementsForAsset(asset_id)
			print(engCount)
			testData = dbstuff.getTestsForAsset(asset_id)
			print(testData)
			reportWriter.writeAssetReport(issueData, engCount, testData)
			return gethtmlreport()
		except:
			return render_template('error.html')

@app.route("/stats")
def stats():
	return render_template('stats.html')

@app.route("/viewstats", methods=['POST'])
def viewstats():

	_startDate = request.form['startDate']
	_endDate = request.form['endDate']

	getStats = stat.ReportatronStats()
	data = getStats.getAllTheStats(_startDate, _endDate)

	getWhitehat = stat.GetWhitehatData()
	vulnData = getWhitehat.groupVulns()
	processWh = stat.ProcessGroup(vulnData)
	otherData = processWh.getGroupStats()

	data.update(otherData)
	return render_template('viewstats.html', data=data)

@app.route("/search")
def search():
	searchTerm = request.args.get('searchTerm')
	data = searchConnection.search(searchTerm)
	return render_template('searchresults.html', data=data)


@app.route("/viewthirdparty")
def viewthirdparty():
	return thirdpartyflask.viewthirdparty()
#	data = dbstuff.getAllThirdPartyData()
#	return render_template('viewthirdparty.html', data=data)

@app.route("/createthirdparty")
def createthirdparty():
	return render_template('createthirdparty.html')

@app.route("/updatethirdparty")
def updatethirdparty():
	_tpID = request.args.get('tpID')

	data = dbstuff.getSingleThirdPartyData(_tpID)
	return render_template('updatethirdparty.html', data=data)

@app.route("/updatetp", methods=['POST'])
def updatetp():
	_tpID = request.form['tpID']
	_tpName = request.form['tpName']
	_tpAddress = request.form['tpAddress']
	_tpService = request.form['tpService']
	_tpDescription = request.form['tpDescription']
	_tpContacts = request.form['tpContacts']
	_busOwner = request.form['busOwner']
	_busDept = request.form['busDept']
	_tpRisk = request.form['tpRisk']
	_remoteAccess = request.form['remoteAccess']
	_reviewDate = request.form['reviewDate']
	_reReviewDate = request.form['reReviewDate']
	_tpNotes = request.form['tpNotes']

	try:
		dbstuff.updateThirdParty(_tpID,_tpName,_tpAddress,_tpService,_tpDescription,_tpContacts,_busOwner,_busDept,_tpRisk,_remoteAccess,_reviewDate,_reReviewDate,_tpNotes)
	except Exception as error:
		print(error)
		return redirect(url_for("error"))
	return redirect(url_for("viewthirdparty"))

@app.route("/createtp", methods=['POST'])
def createtp():
	_tpName = request.form['tpName']
	_tpAddress = request.form['tpAddress']
	_tpService = request.form['tpService']
	_tpDescription = request.form['tpDescription']
	_tpContacts = request.form['tpContacts']
	_busOwner = request.form['busOwner']
	_busDept = request.form['busDept']
	_tpRisk = request.form['tpRisk']
	_remoteAccess = request.form['remoteAccess']
	_reviewDate = request.form['reviewDate']
	_reReviewDate = request.form['reReviewDate']
	_tpNotes = request.form['tpNotes']

	try:
		dbstuff.createThirdParty(_tpName,_tpAddress,_tpService,_tpDescription,_tpContacts,_busOwner,_busDept,_tpRisk,_remoteAccess,_reviewDate,_reReviewDate,_tpNotes)
	except Exception as error:
		print(error)
		return redirect(url_for("error"))
	return redirect(url_for("viewthirdparty"))

if __name__ == "__main__":
	#config = configparser.ConfigParser()
	#config.read('default.conf')
	#hostIP = config['DEFAULT']['host']
	app.run()
