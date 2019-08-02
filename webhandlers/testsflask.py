from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import singledocs, tests

docConnection = singledocs.Docs()
testConnection = tests.Tests()

def newtest():
	asset_id = request.args.get('asset_id')
	engagement_id = request.args.get('engagement_id')
	return render_template('newtest.html', asset_id=asset_id, engagement_id=engagement_id)

def createtest():
	engagement_id = request.form['engagement_id']
	test_type = request.form['test_type']
	test_exec_summary = request.form['test_exec_summary']
	test_base_location = request.form['test_base_location']
	test_limitations = request.form['test_limitations']
	test_main_contact = request.form['test_main_contact']
	test_date = request.form['test_date']
	test_notes = request.form['test_notes']
	try:
		timenow = datetime.datetime.now().isoformat().split(".")[0]

		if engagement_id:
			testConnection.createTest(engagement_id,test_type,test_exec_summary,test_base_location,test_limitations,test_main_contact,timenow,test_date,test_notes)
		else:
			testConnection.createTest(None,test_type,test_exec_summary,test_base_location,test_limitations,test_main_contact,timenow,test_date,test_notes)

		return redirect(url_for("viewtests"))
	except:
		return redirect(url_for("error"))

def viewtests():
	engagement_id = request.args.get('engagement_id')
	asset_id = request.args.get('asset_id')
	if engagement_id:
		data = testConnection.getTestsForEngagement(engagement_id)
		return render_template('viewtests.html', data=data)
	if asset_id:
		data = testConnection.getTestsForAsset(asset_id)
		return render_template('viewtests.html', data=data)
	else:
		data = testConnection.getTests()
		return render_template('viewtests.html', data=data)

def updatetest():
	test_id = request.args.get('test_id')
	data = docConnection.getDoc(test_id)
	return render_template('updatetest.html', data=data)

def updatetestapi():
	test_id = request.form['test_id']
	test_type = request.form['test_type']
	test_exec_summary = request.form['test_exec_summary']
	test_base_location = request.form['test_base_location']
	test_limitations = request.form['test_limitations']
	engagement_main_contact = request.form['engagement_main_contact']
	test_date = request.form['test_date']
	test_notes = request.form['test_notes']
	try:
		testConnection.updateTest(test_id,test_type,test_exec_summary,test_base_location,test_limitations,engagement_main_contact,test_date,test_notes)
		return redirect(url_for("viewtests"))
	except:
		return redirect(url_for("error"))
