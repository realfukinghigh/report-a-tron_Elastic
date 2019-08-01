from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import singledocs, engagements

docConnection = singledocs.Docs()
engagementConnection = engagements.Engagements()

def engagements():
	_assetName = request.args.get('assetName')
	_assetID = request.args.get('assetID')
	if _assetName:
		return render_template("engagements.html", assetName=_assetName, assetID=_assetID)
	else:
		return render_template("engagements.html")

def newengagement():
	_assetID = request.form['assetID']
	_engformLocation = request.form['engformLocation']
	_mainContact = request.form['mainContact']
	_riskRating = request.form['riskRating']
	_receivedOn = request.form['receivedOn']
	_actionTaken = request.form['actionTaken']
	_engNotes = request.form['engNotes']
	if _assetID:
		try:
			timenow = datetime.datetime.now().isoformat().split(".")[0]
			engagementConnection.createEngagement(_assetID,_engformLocation,_mainContact,_riskRating,_receivedOn,_actionTaken,_engNotes)
			return redirect(url_for("viewengagements"))
		except:
			return redirect(url_for("error"))

	else:
		try:
			timenow = datetime.datetime.now().isoformat().split(".")[0]
			engagementConnection.createEngagement(None,_engformLocation,_mainContact,_riskRating,_receivedOn,_actionTaken,_engNotes)
			return redirect(url_for("viewengagements"))
		except:
			return redirect(url_for("error"))

def openengagements():
	data = engagementConnection.getOpenEngagements()
	return render_template('viewengagements.html', data=data)

def viewengagements():
	assetID = request.args.get('assetID')
	assetName = request.args.get('assetName')
	if assetID:
		data = engagementConnection.getEngagementsForAsset(assetID)
		return render_template('viewengagements.html', data=data, assetName=assetName)
	else:
		data = engagementConnection.getEngagements()
		return render_template('viewengagements.html', data=data)

def updateEng():
	_engID = request.args.get('engID')
	data = docConnection.getDoc(_engID)
	return render_template('updateeng.html', data=data)

def updateengagement():
	_engID = request.form['engId']
	_engformLocation = request.form['engformLocation']
	_mainContact = request.form['mainContact']
	_riskRating = request.form['riskRating']
	_receivedOn = request.form['receivedOn']
	_actionTaken = request.form['actionTaken']
	_engNotes = request.form['engNotes']
	_engStatus = request.form['engStatus']
	try:
		engagementConnection.updateEngagement(_engID,_engformLocation,_mainContact,_riskRating,_receivedOn,_actionTaken,_engNotes,_engStatus)
		return redirect(url_for("viewengagements"))
	except:
		return redirect(url_for("error"))
