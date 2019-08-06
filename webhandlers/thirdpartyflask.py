from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import singledocs, thirdparty

docConnection = singledocs.Docs()
tpConnection = thirdparty.Thirdparty()

def viewthirdparty():
	data = tpConnection.getThirdParty()
	return render_template('viewthirdparty.html', data=data)

def updatethirdparty():
	asset_id = request.args.get('asset_id')

	data = docConnection.getDoc(asset_id)
	return render_template('updatethirdparty.html', data=data)

def updatethirdpartyapi():
	asset_id = request.form['asset_id']
	asset_name = request.form['asset_name']
	third_party_address = request.form['third_party_address']
	third_party_service = request.form['third_party_service']
	asset_notes = request.form['asset_notes']
	third_party_contact = request.form['third_party_contact']
	asset_owner = request.form['asset_owner']
	third_party_business_department = request.form['third_party_business_department']
	third_party_risk_rating = request.form['third_party_risk_rating']
	third_party_remote_access = request.form['third_party_remote_access']
	third_party_review_date = request.form['third_party_review_date']
	third_party_rereview_date = request.form['third_party_rereview_date']
	third_party_notes = request.form['third_party_notes']

	try:
		tpConnection.updateThirdParty(asset_id, asset_name, third_party_address, third_party_service, third_party_contact, asset_owner, third_party_business_department, third_party_risk_rating, third_party_remote_access, third_party_review_date, third_party_rereview_date, third_party_notes)

	except Exception as error:
		return redirect(url_for("error"))

	return redirect(url_for("viewthirdparty"))
