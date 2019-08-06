from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import singledocs, engagements

docConnection = singledocs.Docs()
engagementConnection = engagements.Engagements()

def engagements():
	asset_name = request.args.get('asset_name')
	asset_id = request.args.get('asset_id')
	if asset_name:
		return render_template("engagements.html", asset_name=asset_name, asset_id=asset_id)
	else:
		return render_template("engagements.html")

def createengagement():
	asset_id = request.form['asset_id']
	engagement_form_location = request.form['engagement_form_location']
	engagement_main_contact = request.form['engagement_main_contact']
	engagement_risk_rating = request.form['engagement_risk_rating']
	engagement_received_on = request.form['engagement_received_on']
	engagement_action_taken = request.form['engagement_action_taken']
	engagement_notes = request.form['engagement_notes']
	if asset_id:
		try:
			timenow = datetime.datetime.now().isoformat().split(".")[0]
			engagementConnection.createEngagement(asset_id,engagement_form_location,engagement_main_contact,engagement_risk_rating,engagement_received_on,engagement_action_taken,engagement_notes)
			return redirect(url_for("viewengagements"))
		except:
			return redirect(url_for("error"))

	else:
		try:
			timenow = datetime.datetime.now().isoformat().split(".")[0]
			engagementConnection.createEngagement(None,engagement_form_location,engagement_main_contact,engagement_risk_rating,engagement_received_on,engagement_action_taken,engagement_notes)
			return redirect(url_for("viewengagements"))
		except:
			return redirect(url_for("error"))

def openengagements():
	data = engagementConnection.getOpenEngagements()
	return render_template('viewengagements.html', data=data)

def viewengagements():
	asset_id = request.args.get('asset_id')
	asset_name = request.args.get('asset_name')
	if asset_id:
		data = engagementConnection.getEngagementsForAsset(asset_id)
		return render_template('viewengagements.html', data=data, asset_name=asset_name)
	else:
		data = engagementConnection.getEngagements()
		return render_template('viewengagements.html', data=data)

def updateengagement():
	engagement_id = request.args.get('engagement_id')
	data = docConnection.getDoc(engagement_id)
	return render_template('updateengagement.html', data=data)

def updateengagementapi():
	engagement_id = request.form['engagement_id']
	engagement_form_location = request.form['engagement_form_location']
	engagement_main_contact = request.form['engagement_main_contact']
	engagement_risk_rating = request.form['engagement_risk_rating']
	engagement_received_on = request.form['engagement_received_on']
	engagement_action_taken = request.form['engagement_action_taken']
	engagement_notes = request.form['engagement_notes']
	_engStatus = request.form['engStatus']
	try:
		engagementConnection.updateengagementapi(engagement_id,engagement_form_location,engagement_main_contact,engagement_risk_rating,engagement_received_on,engagement_action_taken,engagement_notes,_engStatus)
		return redirect(url_for("viewengagements"))
	except:
		return redirect(url_for("error"))
