from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import singledocs, issues

docConnection = singledocs.Docs()
issueConnection = issues.Issues()

def viewissues():
	engagement_id = request.args.get('engagement_id')
	asset_id = request.args.get('asset_id')
	test_id = request.args.get('test_id')
	asset_name = request.args.get('asset_name')
	if test_id:
		data = dbstuff.getIssuesForTest(test_id)
		return render_template('viewissues.html', data=data)
	if asset_id:
		data = dbstuff.getIssuesForAsset(asset_id)
		return render_template('viewissues.html', data=data, asset_name=asset_name)
	else:
		data = issueConnection.getIssues()
		return render_template('viewissues.html', data=data)

def createnewissue():
	asset_id = request.args.get('asset_id')
	engagement_id = request.args.get('engagement_id')
	test_id = request.args.get('test_id')
	return render_template("createnewissue.html", asset_id=asset_id, engagement_id=engagement_id, test_id=test_id)

def createissueapi():
    asset_id = request.form['asset_id']
    engagement_id = request.form['engagement_id']
    test_id = request.form['test_id']
    issue_title = request.form['issue_title']
    issue_location = request.form['issue_location']
    issue_description = request.form['issue_description']
    issue_remediation = request.form['issue_remediation']
    issue_risk_rating = request.form['issue_risk_rating']
    issue_risk_impact = request.form['issue_risk_impact']
    issue_risk_likelihood = request.form['issue_risk_likelihood']
    issue_status = request.form['issue_status']
    issue_details = request.form['issue_details']
    issue_notes = request.form['issue_notes']

    try:
        timenow = datetime.datetime.now().isoformat().split(".")[0]
        issueConnection.createNewIssue(test_id, issue_title, issue_location, issue_description, issue_remediation, issue_risk_rating, issue_risk_impact, issue_risk_likelihood, issue_status, issue_details, issue_notes, timenow)

    except Exception as error:
        return redirect(url_for("error"))

    return redirect(url_for("createnewissue", asset_id=asset_id, engagement_id=engagement_id, test_id=test_id))

def updateissue():
	issue_id = request.args.get('issue_id')
	try:
		data = docConnection.getDoc(issue_id)
		return render_template("updateissue.html", data=data)
	except:
		return redirect(url_for("error"))

def updateissueapi():
	issue_id = request.form['issue_id']
	issue_status = request.form['issue_status']
	issue_title = request.form['issue_title']
	issue_risk_rating = request.form['issue_risk_rating']
	issue_risk_impact = request.form['issue_risk_impact']
	issue_risk_likelihood = request.form['issue_risk_likelihood']
	issue_location = request.form['issue_location']
	issue_description = request.form['issue_description']
	issue_remediation = request.form['issue_remediation']
	issue_details = request.form['issue_details']
	issue_notes = request.form['issue_notes']
	issue_ra_date = request.form['issue_ra_date']
	issue_ra_owner = request.form['issue_ra_owner']
	issue_ra_expiry = request.form['issue_ra_expiry']
	issue_ra_notes = request.form['issue_ra_notes']
	try:
		issueConnection.updateIssue(issue_id, issue_title, issue_risk_rating, issue_risk_impact, issue_risk_likelihood, issue_location, issue_status, issue_description, issue_remediation, issue_details, issue_notes, issue_ra_date, issue_ra_owner, issue_ra_expiry, issue_ra_notes)
		return redirect(url_for("viewissues"))
	except:
		return redirect(url_for("error"))
