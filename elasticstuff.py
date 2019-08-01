import psycopg2
import datetime
import os
from psycopg2.extras import RealDictCursor
import json
import requests

headers = {"Content-Type": "application/json"}
url = "http://192.168.130.135:9200/reportatron/"

def getAssets(): 

	body = json.dumps({"size": 10000, "query": {"bool": {"must_not": [{"exists": {"field": "engagement_stuff"}}, {"exists": {"field": "test_stuff"}}, {"exists": {"field": "issue_stuff"}}, {"exists": {"field": "third_party_stuff"}}]}}})
	
	sender = requests.get(url + "_search", data=body, headers=headers)
	data = sender.json()['hits']['hits']
	
	return data
	
def createAsset(_assetName, _assetType, _assetOwner, timenow, _assetNotes, _assetInternetFacing):

	body = json.dumps({"asset_stuff": {"asset_name": _assetName, "asset_type": _assetType, "asset_owner": _assetOwner, "asset_created_on": timenow, "asset_notes": _assetNotes, "asset_internet_facing": _assetInternetFacing}})
	
	sender = requests.post(url + "_doc", data=body, headers=headers)
	if sender.status_code != 201: 
		raise ReferenceError('asset not created')

def createEngagement(asset_id,engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes): 

	if asset_id: 
		requestor = requests.get(url + "_doc/" + asset_id, headers=headers)
		_assetStuff = requestor.json()['_source']['asset_stuff']
		_assetStuff.update({"asset_id": requestor.json()['_id']})
	
		body = json.dumps({"asset_stuff": _assetStuff, "engagement_stuff": {"engagement_form_location": engform_location, "engagement_main_contact": main_contact, "engagement_risk_rating": risk_rating, "engagement_received_on": received_on, "engagement_action_taken": action_taken, "engagement_notes": eng_notes, "engagement_status": "Open"}})
	
	else: 
		body = json.dumps({"engagement_stuff": {"engagement_form_location": engform_location, "engagement_main_contact": main_contact, "engagement_risk_rating": risk_rating, "engagement_received_on": received_on, "engagement_action_taken": action_taken, "engagement_notes": eng_notes, "engagement_status": "Open"}})
	
	sender = requests.post(url + "_doc", data=body, headers=headers)
	if sender.status_code != 201: 
		raise ReferenceError('engagement not created')
	
def getEngagements(): 

	body = json.dumps({"size":10000, "query": {"bool": {"must": {"exists": {"field": "engagement_stuff"}}, "must_not": [{"exists": {"field": "issue_stuff"}}, {"exists": {"field": "test_stuff"}}]}}})

	sender = requests.get(url + "_search", headers=headers, data=body)
	data = sender.json()['hits']['hits']

	return data
	
def getEngagementsForAsset(asset_id): 

	body = json.dumps({"size":10000, "query": {"bool": {"must": {"term": {"asset_stuff.asset_id.keyword": asset_id}}, "must_not": [{"exists": {"field": "issue_stuff"}},{"exists": {"field": "test_stuff"}}]}}})
	
	sender = requests.get(url + "_search", headers=headers, data=body)
	data = sender.json()['hits']['hits']
	
	return data

def createNewTest(eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes):

	sqlCreateNewTest = "INSERT INTO tests(eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlCreateNewTest, (eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
def getOpenEngagements(): 
	
	body = json.dumps({"size":10000, "query": {"bool": {"must": [{"exists": {"field": "engagement_stuff"}}, {"term": {"engagement_stuff.engagement_status.keyword": "Open"}}], "must_not": [{"exists": {"field": "issue_stuff"}}, {"exists": {"field": "test_stuff"}}]}}})
	
	sender = requests.get(url + "_search", headers=headers, data=body)
	data = sender.json()['hits']['hits']
	
	return data
	
def getDocument(doc_id):

	sender = requests.get(url + "_doc/" + doc_id, headers=headers)
	data = sender.json()
	
	return data
	
def updateEngagement(_engID,_engformLocation,_mainContact,_riskRating,_receivedOn,_actionTaken,_engNotes,_engStatus):
	
	body = json.dumps({"doc": {"engagement_stuff" : {"engagement_form_location": _engformLocation, "engagement_main_contact": _mainContact, "engagement_risk_rating": _riskRating, "engagement_received_on": _receivedOn, "engagement_action_taken": _actionTaken, "engagement_notes": _engNotes, "engagement_status": _engStatus}}})
	
	sender = requests.post(url + "_update/" + _engID, headers=headers, data=body)
	print(sender.json())
	if sender.status_code != 200: 
		raise ReferenceError('update failed')
		
def updateAsset(_assetID, _assetName, _assetType, _assetOwner, _assetNotes, _assetInternetFacing): 

	body = json.dumps({"doc": {"asset_stuff" : {"asset_name": _assetName, "asset_type": _assetType, "asset_owner": _assetOwner, "asset_notes": _assetNotes, "asset_internet_facing": _assetInternetFacing}}})
	
	sender = requests.post(url + "_update/" + _assetID, headers=headers, data=body)
	print(sender.json())
	print(sender.status_code)
	if sender.status_code != 200: 
		raise ReferenceError('update failed')

def createNewIssue(eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes):

	sqlCreateNewIssue = "INSERT INTO issues(eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING issue_id"
	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlCreateNewIssue, (eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes,))
		issue_id = cur.fetchall()[0][0]
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
	if risk_rating != 'Info': 
		try: 
			conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
			cur = conn.cursor()
			cur.execute("UPDATE issues SET issue_due_date = CASE WHEN risk_rating LIKE 'Critical' THEN created_on + interval '7 days' WHEN risk_rating LIKE 'High' THEN created_on + interval '30 days' WHEN risk_rating LIKE 'Medium' THEN created_on + interval '60 days' WHEN risk_rating LIKE 'Low' THEN created_on + interval '180 days' END")
			conn.commit()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			raise

	
def getAllAssetTableData():

	sql = "SELECT * FROM assets ORDER BY created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sql)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
def getSingleEngagement(eng_id):

	sqlSingleEng = "SELECT * FROM engagements WHERE eng_id = %s"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlSingleEng, (eng_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getSingleAssetTestData(asset_id):

	sqlTestData = "SELECT * FROM assets WHERE asset_id = %s ORDER BY created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlTestData, (asset_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getAllEngagementData():

	sqlEngagementData = "SELECT DISTINCT on (engagements.eng_id) engagements.*, assets.asset_name, assets.asset_id FROM engagements LEFT JOIN links ON links.link_eng_id=engagements.eng_id LEFT JOIN assets ON links.link_asset_id=assets.asset_id ORDER BY engagements.eng_id DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlEngagementData)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
def getOpenEngagementData():

	sqlOpenEngagementData = "SELECT DISTINCT on (engagements.eng_id) engagements.*, assets.asset_name, assets.asset_id FROM engagements LEFT JOIN links ON links.link_eng_id=engagements.eng_id LEFT JOIN assets ON links.link_asset_id=assets.asset_id WHERE engagements.eng_status NOT LIKE 'Closed' ORDER BY engagements.eng_id"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlOpenEngagementData)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getTestsForEngagement(eng_id):

	sqlEngagementData = "SELECT DISTINCT on (tests.test_id) tests.*, assets.asset_name, assets.asset_id FROM tests LEFT JOIN links ON tests.eng_id=links.link_eng_id LEFT JOIN assets ON assets.asset_id=links.link_asset_id WHERE tests.eng_id = %s ORDER BY tests.test_id"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlEngagementData, (eng_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getAllTestData():

	sqlTestData = "SELECT DISTINCT on (tests.test_id) tests.*, assets.asset_name, assets.asset_id FROM tests LEFT JOIN links on links.link_eng_id=tests.eng_id LEFT JOIN assets ON links.link_asset_id=assets.asset_id ORDER BY tests.test_id DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlTestData)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getTestsForAsset(asset_id):

	sqlTestAssetData = "SELECT DISTINCT on (tests.test_id) tests.*, assets.asset_name, assets.asset_id FROM tests INNER JOIN links ON links.link_eng_id=tests.eng_id INNER JOIN assets ON links.link_asset_id=assets.asset_id WHERE assets.asset_id = %s ORDER BY tests.test_id DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlTestAssetData, (asset_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getIssuesForAsset(asset_id):

	sqlIssueAsset = "SELECT assets.asset_id, assets.asset_name, issues.* FROM issues LEFT JOIN issue_links ON issues.issue_id=issue_links.link_issue_id LEFT JOIN assets ON assets.asset_id=issue_links.link_asset_id WHERE assets.asset_id = %s ORDER BY issues.created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlIssueAsset, (asset_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getIssuesForEngagement(eng_id):

	sqlIssueEng = "SELECT * FROM issues WHERE eng_id = %s ORDER BY created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlIssueEng, (eng_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getIssuesForTest(test_id):

	sqlIssueTest = "SELECT DISTINCT on (issues.issue_id) issues.*, assets.asset_name, assets.asset_id FROM issues LEFT JOIN issue_links ON issue_links.link_issue_id=issues.issue_id LEFT JOIN assets ON issue_links.link_asset_id=assets.asset_id WHERE issues.test_id = %s ORDER BY issues.issue_id"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlIssueTest, (test_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getAllIssueData():

	sqlIssue = "SELECT issues.*, assets.asset_name, assets.asset_id FROM issues LEFT JOIN issue_links ON issue_links.link_issue_id=issues.issue_id LEFT JOIN assets ON issue_links.link_asset_id=assets.asset_id ORDER BY issues.issue_id DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlIssue)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def updateSingleIssue(issueTitle,riskRating,riskImpact,riskLikelihood,location,issueStatus,description,remediation,issueDetails,issueNotes,issueRADate,issueRAOwner,issueRAExpiry,issueRANotes,issueID):

	if issueRADate != "None": 
		sqlIssueUpdate = "UPDATE issues SET issue_title = %s, risk_rating = %s, risk_impact = %s, risk_likelihood = %s, issue_location = %s, issue_status = %s, issue_description = %s, remediation = %s, issue_details = %s, issue_notes = %s, issue_ra_date = %s, issue_ra_owner = %s, issue_ra_expiry, issue_ra_notes = %s WHERE issue_id = %s"
		try:
			conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
			cur = conn.cursor()
			cur.execute(sqlIssueUpdate, (issueTitle,riskRating,riskImpact,riskLikelihood,location,issueStatus,description,remediation,issueDetails,issueNotes,issueRADate,issueRAOwner,issueRAExpiry,issueRANotes,issueID,))
			conn.commit()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			raise
	
	else: 
		sqlIssueUpdate = "UPDATE issues SET issue_title = %s, risk_rating = %s, risk_impact = %s, risk_likelihood = %s, issue_location = %s, issue_status = %s, issue_description = %s, remediation = %s, issue_details = %s, issue_notes = %s, issue_ra_owner = %s, issue_ra_notes = %s WHERE issue_id = %s"
		try:
			conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
			cur = conn.cursor()
			cur.execute(sqlIssueUpdate, (issueTitle,riskRating,riskImpact,riskLikelihood,location,issueStatus,description,remediation,issueDetails,issueNotes,issueRAOwner,issueRANotes,issueID,))
			conn.commit()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			raise

def getSingleIssue(issue_id):

	sqlSingleIssue = "SELECT * FROM issues WHERE issue_id = %s"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlSingleIssue, (issue_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getTestDataForReport(test_id):

	#sqlTestData = "SELECT tests.* from tests INNER JOIN issues ON issues.test_id=tests.test_id WHERE issues.test_id = %s LIMIT 1"
	sqlTestData = "SELECT * from tests WHERE test_id = %s"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlTestData, (test_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getAssetIdFromTitle(asset_name):

	sqlAssetID = "SELECT asset_id FROM assets WHERE asset_name LIKE %s"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlAssetID, (asset_name,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
def getAssetIdFromSearch(asset_name):

	sqlAssetSearch = "SELECT * FROM assets WHERE asset_name ~* %s"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlAssetSearch, (asset_name,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def countEngagementsForAsset(asset_id):

	sqlCountEng = "SELECT COUNT(eng_id) FROM engagements WHERE asset_id = %s"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlCountEng, (asset_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise


def getIssuesForAssetReport(asset_id, status_open, status_closed, status_RA):

	sqlGetAssetReportIssues = "SELECT * FROM issues WHERE asset_id = %s AND(issue_status LIKE %s OR issue_status LIKE %s OR issue_status LIKE %s)"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlGetAssetReportIssues, (asset_id, status_open, status_closed, status_RA,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
def getAllThirdPartyData():

	sqlGetTPData = "SELECT * FROM tp_info"

	try:
		conn = psycopg2.connect("dbname=third_party_inventory user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlGetTPData)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
def getSingleThirdPartyData(tp_id):

	sqlGetTPData = "SELECT * FROM tp_info WHERE tp_id = %s"

	try:
		conn = psycopg2.connect("dbname=third_party_inventory user=webapp password=<password>")
		cur = conn.cursor(cursor_factory=RealDictCursor)
		cur.execute(sqlGetTPData, (tp_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def updateThirdParty(tp_id,tp_name,tp_address,tp_service,tp_description,tp_contacts,bus_owner,bus_dept,tp_risk,remote_access,review_date,rereview_date,tp_notes):

	sqlUpdateThirdParty = "UPDATE tp_info SET tp_name = %s, tp_address = %s, tp_service = %s, tp_description = %s, tp_contacts = %s, bus_owner = %s, bus_dept = %s, tp_risk = %s, remote_access = %s, review_date = %s, rereview_date = %s, tp_notes = %s WHERE tp_id = %s"
	try:
		conn = psycopg2.connect("dbname=third_party_inventory user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlUpdateThirdParty, (tp_name,tp_address,tp_service,tp_description,tp_contacts,bus_owner,bus_dept,tp_risk,remote_access,review_date,rereview_date,tp_notes,tp_id,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
def createThirdParty(tp_name,tp_address,tp_service,tp_description,tp_contacts,bus_owner,bus_dept,tp_risk,remote_access,review_date,rereview_date,tp_notes):

	sqlCreateThirdParty = "INSERT INTO tp_info (tp_name,tp_address,tp_service,tp_description,tp_contacts,bus_owner,bus_dept,tp_risk,remote_access,review_date,rereview_date,tp_notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	try:
		conn = psycopg2.connect("dbname=third_party_inventory user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlCreateThirdParty, (tp_name,tp_address,tp_service,tp_description,tp_contacts,bus_owner,bus_dept,tp_risk,remote_access,review_date,rereview_date,tp_notes,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise